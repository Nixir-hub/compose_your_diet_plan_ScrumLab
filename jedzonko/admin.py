from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Recipe)
admin.site.register(Plan)
admin.site.register(DayName)
admin.site.register(RecipePlan)
admin.site.register(Page)