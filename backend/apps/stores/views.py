from rest_framework import viewsets, permissions
from .models import Store
from .serializers import StoreSerializer

class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet per visualizzazione stores"""
    queryset = Store.objects.filter(is_active=True, accepts_online_orders=True)
    serializer_class = StoreSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'