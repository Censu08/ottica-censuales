"""Configurazione task periodici Celery Beat"""
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # Sincronizzazione prodotti ogni giorno alle 2:00
    'daily-sync-products': {
        'task': 'apps.integration.tasks.daily_sync_products',
        'schedule': crontab(hour=2, minute=0),
    },
    
    # Sincronizzazione inventario ogni ora
    'hourly-sync-inventory': {
        'task': 'apps.integration.tasks.hourly_sync_inventory',
        'schedule': crontab(minute=0),  # Ogni ora al minuto 0
    },
    
    # Export ordini ogni giorno alle 3:00
    'daily-export-orders': {
        'task': 'apps.integration.tasks.daily_export_orders',
        'schedule': crontab(hour=3, minute=0),
    },
    
    # Calcolo metriche giornaliere alle 1:00
    'daily-calculate-metrics': {
        'task': 'apps.analytics.tasks.calculate_daily_metrics',
        'schedule': crontab(hour=1, minute=0),
    },
    
    # Pulizia log vecchi ogni domenica alle 4:00
    'weekly-cleanup-logs': {
        'task': 'apps.integration.tasks.cleanup_old_logs',
        'schedule': crontab(hour=4, minute=0, day_of_week=0),
    },
}
