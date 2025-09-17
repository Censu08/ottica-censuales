from django.db import models
from apps.common.models import TimeStampedModel

class IntegrationLog(TimeStampedModel):
    """Log delle operazioni di integrazione"""
    OPERATION_TYPES = [
        ('sync_products', 'Sincronizzazione Prodotti'),
        ('sync_inventory', 'Sincronizzazione Inventario'),
        ('export_orders', 'Esportazione Ordini'),
        ('import_customers', 'Importazione Clienti'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'In attesa'),
        ('running', 'In esecuzione'),
        ('completed', 'Completato'),
        ('failed', 'Fallito'),
        ('partial', 'Completato parzialmente'),
    ]
    
    operation_type = models.CharField(max_length=50, choices=OPERATION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Parametri operazione
    parameters = models.JSONField(default=dict, blank=True)
    
    # Risultati
    records_processed = models.PositiveIntegerField(default=0)
    records_success = models.PositiveIntegerField(default=0)
    records_failed = models.PositiveIntegerField(default=0)
    
    # Log dettagliato
    log_messages = models.TextField(blank=True)
    error_details = models.TextField(blank=True)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'integration_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.operation_type} - {self.status} ({self.created_at})"

class ExternalSystemConfig(models.Model):
    """Configurazione sistemi esterni"""
    name = models.CharField(max_length=100, unique=True)
    system_type = models.CharField(max_length=50)  # 'gestionale', 'crm', 'pos', etc.
    
    # Configurazione connessione
    endpoint_url = models.URLField(blank=True)
    api_key = models.CharField(max_length=500, blank=True)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=500, blank=True)  # Encrypted in production
    
    # Configurazione avanzata
    config_data = models.JSONField(default=dict, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'external_system_configs'
    
    def __str__(self):
        return f"{self.name} ({self.system_type})"