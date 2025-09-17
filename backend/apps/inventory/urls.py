from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'store-inventory', views.StoreInventoryViewSet, basename='store-inventory')
router.register(r'movements', views.InventoryMovementViewSet, basename='inventory-movements')

urlpatterns = [
    path('', include(router.urls)),
]