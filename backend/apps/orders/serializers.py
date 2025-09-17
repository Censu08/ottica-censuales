from rest_framework import serializers
from .models import Order, OrderItem, PrescriptionUpload
from apps.customers.serializers import AddressSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.main_image', read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_image',
            'variant', 'variant_name', 'quantity', 'unit_price', 
            'total_price', 'customizations', 'notes'
        ]

class OrderListSerializer(serializers.ModelSerializer):
    """Serializer per lista ordini (ottimizzato)"""
    store_name = serializers.CharField(source='store.name', read_only=True)
    items_count = serializers.IntegerField(source='items.count', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'store_name', 'status', 
            'fulfillment_method', 'total_amount', 'items_count',
            'created_at', 'estimated_delivery'
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer per dettaglio ordine completo"""
    items = OrderItemSerializer(many=True, read_only=True)
    billing_address = AddressSerializer(read_only=True)
    shipping_address = AddressSerializer(read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'store', 'store_name',
            'billing_address', 'shipping_address', 'status', 'fulfillment_method',
            'subtotal', 'tax_amount', 'shipping_amount', 'discount_amount', 'total_amount',
            'estimated_delivery', 'delivered_at', 'customer_notes', 'tracking_number',
            'items', 'created_at', 'updated_at'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer per creazione ordine"""
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'store', 'billing_address', 'shipping_address', 
            'fulfillment_method', 'customer_notes', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = self.context['request'].user.customer_profile
        
        # Genera order number
        import uuid
        order_number = f"OC{uuid.uuid4().hex[:8].upper()}"
        
        # Calcola totali
        subtotal = sum(item['quantity'] * item['unit_price'] for item in items_data)
        tax_amount = subtotal * 0.22  # IVA 22%
        total_amount = subtotal + tax_amount
        
        order = Order.objects.create(
            order_number=order_number,
            customer=customer,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            **validated_data
        )
        
        # Crea order items
        for item_data in items_data:
            item_data['total_price'] = item_data['quantity'] * item_data['unit_price']
            OrderItem.objects.create(order=order, **item_data)
        
        return order