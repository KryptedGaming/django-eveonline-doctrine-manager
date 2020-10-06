from django import forms
from django_eveonline_doctrine_manager.models import EveDoctrineManagerTag, EveDoctrineCategory

class EveDoctrineForm(forms.Form):
    name = forms.CharField(max_length=32, required=True)
    description = forms.Textarea()
    tags = forms.ModelMultipleChoiceField(
        queryset=EveDoctrineManagerTag.objects.all(),
        required=False)
    category = forms.ModelChoiceField(
        queryset=EveDoctrineCategory.objects.all(),
        required=False)
