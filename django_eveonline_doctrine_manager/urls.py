from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django_eveonline_doctrine_manager.views import old as views
from django_eveonline_doctrine_manager.views import doctrines

urlpatterns = []

# Doctrines
urlpatterns += [
    path('doctrines/', views.view_doctrines,
         name="django-eveonline-doctrine-manager-doctrines-list"),
    path('doctrines/create/', doctrines.DoctrineCreate.as_view(),
         name="django-eveonline-doctrine-manager-doctrines-create"),
    path('doctrines/list/', doctrines.DoctrineListView.as_view(),
         name="django-eveonline-doctrine-manager-doctrines-list"),
    path('doctrines/<doctrine_id>/', views.view_doctrine,
         name="django-eveonline-doctrine-manager-doctrines-view"),
]

# Fittings
urlpatterns += [
    path('fittings/', views.view_fittings,
         name="django-eveonline-doctrine-manager-fittings-list"),
    path('api/fittings/skillcheck/', views.fittings_skill_check,
         name="django-eveonline-doctrine-manager-fittings-skill-check")
]

# Skillplans
urlpatterns += [

]

# SRP
urlpatterns += [

]

# Seeding 
urlpatterns += [

]
