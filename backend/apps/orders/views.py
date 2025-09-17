from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet per ordini clienti"""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'fulfillment_method', 'store']
    ordering = ['-created_at']

    def get_queryset(self):
        # I clienti vedono solo i propri ordini
        return Order.objects.filter(
            customer=self.request.user.customer_profile
        ).select_related('store', 'customer').prefetch_related('items__product')

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderListSerializer

    def perform_create(self, serializer):
        # Associa l'ordine al cliente corrente
        serializer.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annulla ordine (se possibile)"""
        order = self.get_object()
        
        if order.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Ordine non annullabile'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        return Response({'message': 'Ordine annullato'})