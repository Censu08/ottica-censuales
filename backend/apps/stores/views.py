from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Store
from .serializers import StoreSerializer


class StoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.filter(is_active=True)
    serializer_class = StoreSerializer


@api_view(['GET'])
def stores_map_data(request):
    stores = Store.objects.filter(
        is_active=True,
        latitude__isnull=False,
        longitude__isnull=False
    )
    serializer = StoreSerializer(stores, many=True)

    return Response({
        'stores': serializer.data,
        'map_config': {
            'center': {'lat': 38.1157, 'lng': 13.3613},
            'zoom': 12
        }
    })