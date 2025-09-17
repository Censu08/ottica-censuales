from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F
from .models import StoreInventory, InventoryMovement
from .serializers import StoreInventorySerializer, InventoryMovementSerializer

class StoreInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet per inventario stores"""
    serializer_class = StoreInventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'product', 'is_online_available']
    ordering = ['store__name', 'product__name']

    def get_queryset(self):
        return StoreInventory.objects.select_related(
            'store', 'product', 'variant'
        ).filter(is_online_available=True)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Prodotti con stock basso"""
        low_stock_items = self.get_queryset().filter(
            quantity__lte=F('minimum_stock')
        )
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def availability_summary(self, request):
        """Riassunto disponibilità per prodotto"""
        store_id = request.query_params.get('store_id')
        product_id = request.query_params.get('product_id')
        
        queryset = self.get_queryset()
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
            
        summary = queryset.aggregate(
            total_quantity=Sum('quantity'),
            total_reserved=Sum('reserved_quantity'),
            total_available=Sum(F('quantity') - F('reserved_quantity'))
        )
        
        return Response(summary)

class InventoryMovementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet per movimenti inventario (solo lettura)"""
    serializer_class = InventoryMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'product', 'movement_type']
    ordering = ['-created_at']

    def get_queryset(self):
        return InventoryMovement.objects.select_related(
            'store', 'product', 'variant', 'user'
        )