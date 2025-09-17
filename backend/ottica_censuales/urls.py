from django.contrib import admin
from django.urls import path, include
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
    path('api/stores/', include('apps.stores.urls')),

    # Test endpoints
    path('api/test/', api_test, name='api_test'),
    path('health/', health_check, name='health_check'),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)