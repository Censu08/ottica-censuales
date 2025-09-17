from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductVariant
from apps.inventory.models import StoreInventory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent', 'sort_order']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'description', 'website']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'sort_order']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'name', 'attributes', 'price_adjustment', 'image', 'is_active']

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer per lista prodotti (ottimizzato)"""
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    main_image = serializers.ImageField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'slug', 'short_description', 
            'category', 'brand', 'base_price', 'main_image', 'is_active'
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer per dettaglio prodotto completo"""
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    availability = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'slug', 'description', 'short_description',
            'category', 'brand', 'base_price', 'optical_attributes',
            'main_image', 'images', 'variants', 'meta_title', 'meta_description',
            'is_active', 'is_prescription_required', 'requires_measurement',
            'weight', 'dimensions', 'availability', 'created_at'
        ]
    
    def get_availability(self, obj):
        """Ritorna disponibilità per store"""
        request = self.context.get('request')
        store_id = request.query_params.get('store_id') if request else None
        
        if store_id:
            try:
                inventory = StoreInventory.objects.get(
                    store_id=store_id, 
                    product=obj, 
                    is_online_available=True
                )
                return {
                    'available': inventory.available_quantity > 0,
                    'quantity': inventory.available_quantity,
                    'store_price': inventory.store_price or obj.base_price
                }
            except StoreInventory.DoesNotExist:
                return {'available': False, 'quantity': 0}
        
        # Ritorna disponibilità totale se nessun store specificato
        total_quantity = StoreInventory.objects.filter(
            product=obj, 
            is_online_available=True
        ).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
        
        return {
            'available': total_quantity > 0,
            'total_quantity': total_quantity
        }