from django.db import models
from apps.common.models import TimeStampedModel

class SalesMetrics(models.Model):
    """Metriche vendite aggregate per performance"""
    date = models.DateField()
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, null=True, blank=True)
    
    # Metriche ordini
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Metriche prodotti
    products_sold = models.PositiveIntegerField(default=0)
    top_category = models.CharField(max_length=100, blank=True)
    top_brand = models.CharField(max_length=100, blank=True)
    
    # Metriche clienti
    new_customers = models.PositiveIntegerField(default=0)
    returning_customers = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sales_metrics'
        unique_together = ['date', 'store']
        ordering = ['-date']