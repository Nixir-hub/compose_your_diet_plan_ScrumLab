from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    method = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")

    def __str__(self):
        return self.name


class DayName(models.Model):
    name = models.CharField(max_length=16)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

      
class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day_name_id = models.ForeignKey(DayName, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.meal_name


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.title
