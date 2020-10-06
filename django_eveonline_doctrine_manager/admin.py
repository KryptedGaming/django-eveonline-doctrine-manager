from django.contrib import admin
from django import forms
from .models import *

admin.site.register(EveDoctrineRole)
admin.site.register(EveDoctrineManagerTag)
admin.site.register(EveDoctrineCategory)
admin.site.register(EveFitting)
admin.site.register(EveSkillPlan)