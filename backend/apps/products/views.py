from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Prefetch
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductListSerializer, ProductDetailSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet per categorie prodotti"""
    queryset = Category.objects.filter(is_active=True).order_by('sort_order', 'name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet per brands"""
    queryset = Brand.objects.filter(is_active=True).order_by('name')
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet per prodotti con ricerca avanzata"""
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'brand__slug', 'is_prescription_required']
    search_fields = ['name', 'description', 'sku', 'brand__name']
    ordering_fields = ['name', 'base_price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        ).prefetch_related(
            'images', 'variants'
        )
        
        # Filtro per attributi ottici
        optical_filters = self.request.query_params.dict()
        for key, value in optical_filters.items():
            if key.startswith('optical_'):
                attr_name = key.replace('optical_', '')
                queryset = queryset.filter(
                    optical_attributes__contains={attr_name: value}
                )
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Prodotti in evidenza"""
        featured_products = self.get_queryset()[:8]
        serializer = ProductListSerializer(featured_products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search_suggestions(self, request):
        """Suggerimenti per ricerca"""
        query = request.query_params.get('q', '').strip()
        if len(query) < 2:
            return Response([])
        
        suggestions = []
        
        # Prodotti
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(sku__icontains=query),
            is_active=True
        ).select_related('brand')[:5]
        
        for product in products:
            suggestions.append({
                'type': 'product',
                'title': product.name,
                'subtitle': product.brand.name,
                'url': f'/prodotti/{product.slug}',
                'image': product.main_image.url if product.main_image else None
            })
        
        # Brands
        brands = Brand.objects.filter(
            name__icontains=query,
            is_active=True
        )[:3]
        
        for brand in brands:
            suggestions.append({
                'type': 'brand',
                'title': brand.name,
                'url': f'/prodotti?brand={brand.slug}',
                'image': brand.logo.url if brand.logo else None
            })
        
        return Response(suggestions)