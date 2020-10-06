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

    path('doctrines/create/', doctrines.DoctrineCreateView.as_view(),
         name="django-eveonline-doctrine-manager-doctrines-create"),
    path('doctrines/', doctrines.DoctrineListView.as_view(),
         name="django-eveonline-doctrine-manager-doctrines-list"),
    path('doctrines/view/<int:id>/', doctrines.DoctrineDetailView.as_view(),
         name="django-eveonline-doctrine-manager-doctrines-detail"),
    path('doctrines/update/<int:id>/', doctrines.DoctrineUpdateView.as_view(),
         name="django-eveonline-doctrine-manager-doctrines-update"),
    path('doctrines/delete/<int:id>/', doctrines.DoctrineDeleteView.as_view(),
         name="django-eveonline-doctrine-manager-doctrines-delete"),
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
