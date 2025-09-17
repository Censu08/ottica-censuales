from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import IntegrationLog, ExternalSystemConfig
from .tasks import sync_products_task, sync_inventory_task, export_orders_task
from .serializers import IntegrationLogSerializer

class IntegrationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet per log integrazione (solo lettura)"""
    queryset = IntegrationLog.objects.all()
    serializer_class = IntegrationLogSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation_type', 'status']
    ordering = ['-created_at']

@action(detail=False, methods=['post'])
def trigger_sync_products(self, request):
    """Trigger manuale sync prodotti"""
    task = sync_products_task.delay()
    return Response({
        'message': 'Sincronizzazione prodotti avviata',
        'task_id': task.id
    })

@action(detail=False, methods=['post'])
def trigger_sync_inventory(self, request):
    """Trigger manuale sync inventario"""
    store_id = request.data.get('store_id')
    task = sync_inventory_task.delay(store_id)
    return Response({
        'message': 'Sincronizzazione inventario avviata',
        'task_id': task.id
    })

@action(detail=False, methods=['post'])
def trigger_export_orders(self, request):
    """Trigger manuale export ordini"""
    date_from = request.data.get('date_from')
    date_to = request.data.get('date_to')
    task = export_orders_task.delay(date_from, date_to)
    return Response({
        'message': 'Esportazione ordini avviata',
        'task_id': task.id
    })