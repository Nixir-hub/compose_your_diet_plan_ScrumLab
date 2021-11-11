from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404
from random import shuffle
from .models import *
from django.core.paginator import Paginator


class IndexView(View):
    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class DashboardView(View):
    def get(self, request):
        plan = Plan.objects.order_by('-created').first()
        recipe_plans = RecipePlan.objects.filter(plan_id=plan.id).all()
        return render(request, "dashboard.html", dict(
            recipes_count=Recipe.objects.all().count(),
            plans_count=Plan.objects.all().count(),
            day_names=DayName.objects.all().order_by('order'),
            last_added_plan=plan,
            recipe_plans=recipe_plans
        ))


class MainPage(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        array = []
        for recipe in recipes:
            array.append(recipe.id)
        shuffle(array)
        try:
            about = '/' + Page.objects.get(title='o aplikacji').slug
            contact = '/' + Page.objects.get(title='kontakt').slug
        except:
            about = "#about"
            contact = "#contact"
        try:
            recipe1 = Recipe.objects.get(id=array[0])
            recipe2 = Recipe.objects.get(id=array[1])
            recipe3 = Recipe.objects.get(id=array[2])
            resp = {
                "recipe1": recipe1,
                "recipe2": recipe2,
                "recipe3": recipe3,
                "about": about,
                "contact": contact,
            }
        except IndexError:
            empty = {
                "name": "Nie ma przepisów!",
                "description": "Wprowadź minimum 3 przepisy do bazy danych."
            }
            resp = {
                "recipe1": empty,
                "recipe2": empty,
                "recipe3": empty,
                "about": about,
                "contact": contact,
            }
        return render(request, 'index.html', resp)


class ContactView(View):
    def get(self, request):
        try:
            contact = Page.objects.get(title='kontakt')
        except:
            contact = "#contact"
        description = contact.description.split('\r\n')
        title = contact.title.upper()
        return render(request, 'contact.html', {
            'title': title,
            'contact': description
        })


class AboutView(View):
    def get(self, request):
        try:
            about = Page.objects.get(title='o aplikacji')
        except:
            about = "#about"
        slug= about.slug
        description = about.description.split('\r\n')
        title = about.title.upper()
        return render(request, slug + '.html', {
            'title': title,
            'contact': description
        })


class RecipeListView(View):
    def get(self, request):
        recipeList = Recipe.objects.all().order_by("-votes", "-created")
        paginator = Paginator(recipeList, 50)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        ctx = dict(page_obj=page_obj)
        if 'delete' in request.GET:
            recipe_id = request.GET['delete']
            recipe_plans = RecipePlan.objects.filter(recipe_id_id=recipe_id).distinct('plan_id')
            ctx['recipe_plans'] = recipe_plans
            if not recipe_plans:
                Recipe.objects.get(pk=recipe_id).delete()
            else:
                ctx['delete_error'] = True
        return render(request, 'app-recipes.html', ctx)


class PlanListView(View):
    def get(self, request):
        plan_list = Plan.objects.all().order_by('name')
        paginator = Paginator(plan_list, 50)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, 'app-schedules.html', {'plans': plans})


class RecipeAddView(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        method = request.POST.get('method')
        ingredients = request.POST.get('ingredients')
        Recipe.objects.create(
            name=name,
            ingredients=ingredients,
            description=description,
            preparation_time=preparation_time,
            method=method
        )
        return redirect("/recipe/list")


class PlanAddView(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        plan_name = request.POST.get('planName')
        plan_description = request.POST.get('planDescription')
        new_plan = Plan.objects.create(name=plan_name, description=plan_description)
        plan_id = new_plan.pk
        return redirect(f'/plan/{plan_id}')


class PlanAddRecipeView(View):
    def get(self, request):
        if request.GET.get("plan_id"):
            plan_id = request.GET.get("plan_id")
        else:
            plan_id = 1
        context = {'plans': Plan.objects.all().order_by("name"),
                   'recipes': Recipe.objects.all().order_by("name"),
                   'dayNames': DayName.objects.all().order_by("order"),
                   'plan_id': int(plan_id)
                   }
        return render(request, 'app-schedules-meal-recipe.html', context)

    def post(self, request):
        """
        Add Recipe to Plan, or display alert
        :param request: takes values of inputs and make RecipePlan object from them
        :return: redirect to site with plan details
        """
        plan = request.POST.get("choosePlan")
        meal_name = request.POST.get("meal_name")
        order = request.POST.get("order")
        recipe = request.POST.get("recipe")
        day = request.POST.get("day")
        recipe_plan = RecipePlan.objects.create(plan_id=Plan.objects.get(id=int(plan)),
                                               meal_name=meal_name,
                                               order=int(order),
                                               recipe_id=Recipe.objects.get(id=int(recipe)),
                                               day_name_id=DayName.objects.get(id=int(day)))
        recipe_plan.save()
        return redirect(f"/plan/{int(plan)}")


class RecipeView(View):
    """
    View at /recipe/<id> showing recipe details

    Should the button disappear or stop working after voting?

    """

    def get(self, request, id):
        """
        Renders view
        :param id: recipe id passed in URL
        :return: rendered page
        """
        recipe = Recipe.objects.get(pk=id)
        listOfIngredients = recipe.ingredients.rstrip('\n').split('\n')
        listOfMethods = recipe.method.rstrip('\n').split('\n')
        context = {
            'recipe': recipe,
            'listOfIngredients': listOfIngredients,
            'listOfMethods': listOfMethods,
        }
        return render(request, 'app-recipe-details.html', context)

    def post(self, request, id):
        """
        Increases vote number of recipe passed as id in url

        Probably no need to use try-catch as we are sure the object we vote on exists in database.
        Otherwise the page wouldn't load.

        :param id: recipe id passed in URL
        :return: redirects to recipe details
        """
        recipe = Recipe.objects.get(pk=id)
        recipe.votes += 1 if request.POST['action'] == 'like' else -1

        recipe.save()
        return redirect(f'/recipe/{id}')


class RecipeModifyView(View):
    """
    Allows editing existing recipes and saves the result as another, new recipe.
    """
    def get(self, request, id):
        """
        Renders editing page.
        :param request:
        :param id: id of modified Recipe
        :return: returns rendered View
        """
        try:
            context = {
                'id': id,
                'recipe': Recipe.objects.get(pk=id)
            }
            return render(request, 'app-edit-recipe.html', context)
        except Recipe.DoesNotExist:
            raise Http404("Recipe does not exist")

    def post(self, request, id):
        """
        Handles form sent requesting changes to recipe.
        If any input is empty - returns "alert"
        :param request:
        :param id: id of modified Recipe
        :return: New recipe object, saved to db
        """
        name = request.POST.get('name')
        description = request.POST.get('description')
        time = request.POST.get('time')
        method = request.POST.get('method')
        ingredients = request.POST.get('ingredients')
        Recipe.objects.create(
            name=name,
            description=description,
            preparation_time=time,
            method=method,
            ingredients=ingredients
        )
        return redirect('/recipe/list/')


class PlanModifyView(View):
    """
    Allows editing existing plans and saves the result as another, new plan.
    """
    def get(self, request, id):
        """
        Renders editing page.
        :param request:
        :param id: id of modified Plan
        :return: returns rendered View
        """
        try:
            context = {
                'id': id,
                'plan': Plan.objects.get(pk=id)
            }
            return render(request, 'app-edit-schedules.html', context)
        except Plan.DoesNotExist:
            raise Http404("Plan does not exist")

    def post(self, request, id):
        """
        Handles form sent requesting changes to plan.
        If any input is empty - returns "alert"
        :param request:
        :param id: id of modified Plan
        :return: New plan object, saved to db
        """
        name = request.POST.get('name')
        description = request.POST.get('description')
        if  request.POST.get('new') =='':
            Plan.objects.create(
                name=name,
                description=description,
            )
        if request.POST.get('modify') == '':
            plan = Plan.objects.get(pk=id)
            plan.name = name
            plan.description = description
            plan.save()

        return redirect('/plan/list/')


class PlanView(View):
    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        if 'delete' in request.GET:
            RecipePlan.objects.get(pk=request.GET['delete']).delete()
        return render(request, 'app-details-schedules.html', dict(
            plan=plan,
            day_names=DayName.objects.all().order_by('order'),
            recipe_plans=RecipePlan.objects.filter(plan_id=plan).all(),
            plan_id=id
        ))
    def post(self, request, id):
        return render(request, 'app-details-schedules.html', dict(plan_id=id))
