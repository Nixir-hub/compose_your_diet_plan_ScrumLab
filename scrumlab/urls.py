"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('contact/', ContactView.as_view()),
    path('main/', DashboardView.as_view()),
    path('', MainPage.as_view()),
    path('recipe/list/', RecipeListView.as_view()),
    path('plan/list/', PlanListView.as_view()),
    path('recipe/add', RecipeAddView.as_view()),
    path('plan/add/', PlanAddView.as_view()),
    path('plan/add-recipe/', PlanAddRecipeView.as_view()),
    path('recipe/<int:id>/', RecipeView.as_view()),
    path('recipe/modify/<int:id>/', RecipeModifyView.as_view()),
    path('plan/modify/<int:id>/', PlanModifyView.as_view()),
    path('plan/<int:id>', PlanView.as_view()),
    path('about/', AboutView.as_view()),
]
