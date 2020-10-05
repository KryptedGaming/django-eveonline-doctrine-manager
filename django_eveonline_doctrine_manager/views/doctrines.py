from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django_eveonline_doctrine_manager.models import EveDoctrine
from django_eveonline_doctrine_manager.forms import EveDoctrineForm
from django.urls import reverse_lazy
"""
Doctrine CRUD
"""
class DoctrineListView(ListView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_list.html'
    model = EveDoctrine 


class DoctrineCreate(FormView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_form.html'
    form_class = EveDoctrineForm
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-doctrines-list')


class DoctrineUpdate(FormView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/doctrines/doctrine_form.html'
    form_class = EveDoctrineForm
    success_url = reverse_lazy(
        'django-eveonline-doctrine-manager-doctrines-list')
