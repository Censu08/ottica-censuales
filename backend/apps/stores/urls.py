from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.StoreViewSet, basename='stores')

urlpatterns = [
    path('', include(router.urls)),
    path('map-data/', views.stores_map_data, name='stores-map-data'),
]