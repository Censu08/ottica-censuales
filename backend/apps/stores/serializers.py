from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            'id', 'name', 'slug', 'address', 'city', 'province', 
            'postal_code', 'phone', 'email', 'is_active',
            'accepts_online_orders', 'delivery_available', 
            'pickup_available', 'opening_hours'
        ]
        read_only_fields = ['id', 'slug']