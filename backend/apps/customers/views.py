from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer, Address
from .serializers import CustomerSerializer, AddressSerializer

class CustomerProfileViewSet(viewsets.ModelViewSet):
    """ViewSet per profilo cliente"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        # Cliente vede solo il proprio profilo
        return Customer.objects.filter(user=self.request.user)

    def get_object(self):
        # Ritorna sempre il profilo del cliente corrente
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        return customer

class AddressViewSet(viewsets.ModelViewSet):
    """ViewSet per indirizzi cliente"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        # Cliente vede solo i propri indirizzi
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        return Address.objects.filter(customer=customer)

    def perform_create(self, serializer):
        customer, created = Customer.objects.get_or_create(user=self.request.user)
        serializer.save(customer=customer)
