from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'logs', views.IntegrationLogViewSet, basename='integration-logs')

urlpatterns = [
    path('', include(router.urls)),
]