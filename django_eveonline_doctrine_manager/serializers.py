from rest_framework import serializers
from .models import EveFitting
# Serializers define the API representation.


class EveFittingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EveFitting
        fields = ['name', 'fitting', 'ship_id', 'ship_name']
