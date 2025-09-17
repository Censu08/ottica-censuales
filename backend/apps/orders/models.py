from django.db import models
from apps.common.models import TimeStampedModel
from apps.customers.models import Customer, Address
from apps.stores.models import Store
from apps.products.models import Product, ProductVariant

class Order(TimeStampedModel):
    """Modello ordine principale"""
    ORDER_STATUS_CHOICES = [
        ('draft', 'Bozza'),
        ('pending', 'In attesa'),
        ('confirmed', 'Confermato'),
        ('processing', 'In lavorazione'),
        ('ready', 'Pronto'),
        ('shipped', 'Spedito'),
        ('delivered', 'Consegnato'),
        ('cancelled', 'Annullato'),
        ('refunded', 'Rimborsato'),
    ]
    
    FULFILLMENT_CHOICES = [
        ('pickup', 'Ritiro in negozio'),
        ('delivery', 'Consegna a domicilio'),
        ('shipping', 'Spedizione'),
    ]
    
    # Identificativo
    order_number = models.CharField(max_length=20, unique=True)
    
    # Cliente e store
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    
    # Indirizzi
    billing_address = models.ForeignKey(
        Address, 
        on_delete=models.PROTECT, 
        related_name='billing_orders'
    )
    shipping_address = models.ForeignKey(
        Address, 
        on_delete=models.PROTECT, 
        related_name='shipping_orders',
        null=True, 
        blank=True
    )
    
    # Status e fulfillment
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    fulfillment_method = models.CharField(max_length=20, choices=FULFILLMENT_CHOICES)
    
    # Prezzi
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Date importanti
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Note
    customer_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    
    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['customer', 'status']),
            models.Index(fields=['store', 'status']),
        ]
    
    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(TimeStampedModel):
    """Elementi dell'ordine"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    
    # Quantità e prezzi
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Personalizzazioni specifiche ottica (ricette, misurazioni)
    customizations = models.JSONField(default=dict, blank=True)
    # Esempi: {"prescription": {...}, "pd_measurement": 62, "lens_options": [...]}
    
    # Note specifiche item
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

class PrescriptionUpload(TimeStampedModel):
    """Upload ricette mediche per ordini"""
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='prescriptions')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    # File ricetta
    prescription_file = models.FileField(upload_to='prescriptions/')
    original_filename = models.CharField(max_length=200)
    
    # Dati ricetta (se digitalizzati)
    prescription_data = models.JSONField(default=dict, blank=True)
    
    # Validazione
    is_validated = models.BooleanField(default=False)
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    validation_notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'prescription_uploads'
    
    def __str__(self):
        return f"Prescription for {self.customer} - {self.original_filename}"
