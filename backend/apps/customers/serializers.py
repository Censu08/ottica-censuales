from rest_framework import serializers
from .models import Customer, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'type', 'first_name', 'last_name', 'company',
            'address_line_1', 'address_line_2', 'city', 'province',
            'postal_code', 'country', 'phone', 'is_default'
        ]

class CustomerSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    addresses = AddressSerializer(many=True, read_only=True)
    preferred_store_name = serializers.CharField(source='preferred_store.name', read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'user_info', 'phone', 'birth_date', 'gender',
            'preferred_store', 'preferred_store_name', 'newsletter_subscribed',
            'sms_notifications', 'addresses'
        ]
        
    def get_user_info(self, obj):
        return {
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'full_name': obj.user.get_full_name(),
        }