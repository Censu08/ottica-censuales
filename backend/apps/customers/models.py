from django.db import models
from django.contrib.auth.models import User
from apps.common.models import TimeStampedModel
from apps.stores.models import Store

class Customer(TimeStampedModel):
    """Estensione del modello User per clienti"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    
    # Informazioni aggiuntive
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    
    # Store preferenza
    preferred_store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Marketing preferences
    newsletter_subscribed = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=False)
    
    # Dati medici (per ricette)
    medical_notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

class Address(TimeStampedModel):
    """Indirizzi clienti"""
    ADDRESS_TYPES = [
        ('billing', 'Fatturazione'),
        ('shipping', 'Spedizione'),
        ('both', 'Entrambi'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    
    # Dati indirizzo
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=100, blank=True)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='Italia')
    phone = models.CharField(max_length=20, blank=True)
    
    # Flags
    is_default = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'addresses'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"