from rest_framework import serializers
from .models import StoreInventory, InventoryMovement
from apps.stores.models import Store
from apps.products.models import Product

class StoreInventorySerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    available_quantity = serializers.ReadOnlyField()
    
    class Meta:
        model = StoreInventory
        fields = [
            'id', 'store', 'store_name', 'product', 'product_name', 'product_sku',
            'variant', 'quantity', 'reserved_quantity', 'available_quantity',
            'minimum_stock', 'store_price', 'is_online_available', 'last_restocked'
        ]

class InventoryMovementSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = InventoryMovement
        fields = [
            'id', 'store', 'store_name', 'product', 'product_name',
            'variant', 'movement_type', 'quantity_change', 'quantity_after',
            'reference_id', 'notes', 'user', 'user_name', 'created_at'
        ]