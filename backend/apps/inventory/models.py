# backend/apps/inventory/models.py
from django.db import models
from django.contrib.auth.models import User
from apps.common.models import TimeStampedModel
from apps.stores.models import Store
from apps.products.models import Product, ProductVariant


class StoreInventory(TimeStampedModel):
    """Inventario per singolo store"""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)

    # Quantità
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)  # Per ordini in corso
    minimum_stock = models.PositiveIntegerField(default=0)

    # Prezzi specifici store
    store_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Disponibilità online
    is_online_available = models.BooleanField(default=True)

    # Tracking movimento stock
    last_restocked = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'store_inventory'
        unique_together = ['store', 'product', 'variant']
        indexes = [
            models.Index(fields=['store', 'product']),
            models.Index(fields=['quantity']),
            models.Index(fields=['is_online_available']),
        ]

    def __str__(self):
        return f"{self.store.name} - {self.product.name} ({self.quantity})"

    @property
    def available_quantity(self):
        return max(0, self.quantity - self.reserved_quantity)


class InventoryMovement(TimeStampedModel):
    """Log movimenti inventario"""
    MOVEMENT_TYPES = [
        ('restock', 'Rifornimento'),
        ('sale', 'Vendita'),
        ('return', 'Reso'),
        ('adjustment', 'Correzione'),
        ('transfer', 'Trasferimento'),
        ('damage', 'Danno/Perdita'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)

    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity_change = models.IntegerField()  # Può essere negativo
    quantity_after = models.PositiveIntegerField()

    # Riferimenti
    reference_id = models.CharField(max_length=100, blank=True)  # Order ID, etc.
    notes = models.TextField(blank=True)

    # Chi ha fatto il movimento
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'inventory_movements'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} ({self.quantity_change:+d})"