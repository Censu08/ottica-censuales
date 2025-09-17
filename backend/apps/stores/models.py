from django.db import models
from apps.common.models import TimeStampedModel

class Store(TimeStampedModel):
    """Modello per i negozi fisici Censuales"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Gestione manager/staff
    manager = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='managed_stores'
    )
    
    # Settings operativi
    is_active = models.BooleanField(default=True)
    accepts_online_orders = models.BooleanField(default=True)
    delivery_available = models.BooleanField(default=False)
    pickup_available = models.BooleanField(default=True)
    
    # Orari (JSON field per flessibilità)
    opening_hours = models.JSONField(default=dict, blank=True)
    
    # Coordinate per geolocalizzazione
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        db_table = 'stores'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.city})"