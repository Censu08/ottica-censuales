from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profile', views.CustomerProfileViewSet, basename='customer-profile')
router.register(r'addresses', views.AddressViewSet, basename='addresses')

urlpatterns = [
    path('', include(router.urls)),
]