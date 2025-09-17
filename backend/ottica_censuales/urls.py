from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def api_test(request):
    """Vista di test per verificare che l'API funzioni"""
    return JsonResponse({
        'message': 'API di Ottica Censuales funziona!',
        'status': 'ok',
        'debug': settings.DEBUG
    })


def health_check(request):
    """Health check per verificare lo stato del servizio"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'ottica_censuales_backend'
    })


urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Test endpoints
    path('api/test/', api_test, name='api_test'),
    path('health/', health_check, name='health_check'),

    # Commentiamo temporaneamente le app URLs finché non le creiamo
    # path('api/v1/auth/', include('apps.authentication.urls')),
    # path('api/v1/stores/', include('apps.stores.urls')),
    # path('api/v1/products/', include('apps.products.urls')),
    # path('api/v1/inventory/', include('apps.inventory.urls')),
    # path('api/v1/orders/', include('apps.orders.urls')),
    # path('api/v1/customers/', include('apps.customers.urls')),
    # path('api/v1/analytics/', include('apps.analytics.urls')),
    # path('api/v1/integration/', include('apps.integration.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)