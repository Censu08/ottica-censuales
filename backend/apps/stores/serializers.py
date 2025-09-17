from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    """Serializer per la lista dei negozi"""
    formatted_address = serializers.ReadOnlyField()
    formatted_opening_hours = serializers.ReadOnlyField()

    class Meta:
        model = Store
        fields = [
            'id',
            'name',
            'address',
            'formatted_address',
            'city',
            'phone',
            'email',
            'optician_name',
            'opening_hours',
            'formatted_opening_hours',
            'latitude',
            'longitude',
            'description',
            'is_active'
        ]


class StoreMapSerializer(serializers.ModelSerializer):
    """Serializer ottimizzato per la mappa (solo dati essenziali)"""

    class Meta:
        model = Store
        fields = [
            'id',
            'name',
            'address',
            'phone',
            'latitude',
            'longitude',
            'optician_name'
        ]