"""
Admin routes
"""

from django.contrib import admin
from home.models import Person, Department, State


# Register your models here.
admin.site.register(Person)
admin.site.register(Department)
admin.site.register(State)