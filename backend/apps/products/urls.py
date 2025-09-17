from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'brands', views.BrandViewSet, basename='brands')
router.register(r'', views.ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]


