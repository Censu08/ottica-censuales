from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.customers.models import Customer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # Crea profilo customer
        Customer.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('Account disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    customer_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'customer_profile']
        read_only_fields = ['id', 'username']
    
    def get_customer_profile(self, obj):
        try:
            customer = obj.customer_profile
            return {
                'phone': customer.phone,
                'preferred_store': customer.preferred_store.name if customer.preferred_store else None,
                'newsletter_subscribed': customer.newsletter_subscribed,
            }
        except Customer.DoesNotExist:
            return None