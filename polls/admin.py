from django.contrib import admin
from .models import Person
# Register your models here.


class PersonConfig(admin.ModelAdmin):

    list_display = ['firstName','lastName']

admin.site.register(Person,PersonConfig)