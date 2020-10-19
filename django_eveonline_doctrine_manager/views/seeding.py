from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django_eveonline_doctrine_manager.models import EveFittingMarketRule
from django_eveonline_connector.tasks import update_character_contracts

class FittingMarketRuleListView(ListView):
    template_name = 'django_eveonline_doctrine_manager/adminlte/fittings/fitting_market_rules.html'
    model = EveFittingMarketRule

def update_stock(request):
    tokens = request.user.eve_tokens.all()
    characters = [token.evecharacter for token in tokens]
    for character in characters:
        update_character_contracts(character.external_id)
    return redirect('django-eveonline-doctrine-manager-fittings-market')
