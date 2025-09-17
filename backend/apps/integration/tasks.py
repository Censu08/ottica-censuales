from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from .services import GestionaleIntegrationService

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3)
def sync_products_task(self):
    """Task per sincronizzazione prodotti"""
    try:
        service = GestionaleIntegrationService('gestionale_principale')
        log = service.sync_products()
        
        logger.info(f"Sync prodotti completato. Processed: {log.records_processed}, Success: {log.records_success}, Failed: {log.records_failed}")
        
        return {
            'status': log.status,
            'processed': log.records_processed,
            'success': log.records_success,
            'failed': log.records_failed
        }
        
    except Exception as exc:
        logger.error(f"Errore sync prodotti: {exc}")
        self.retry(countdown=300, exc=exc)  # Retry dopo 5 minuti

@shared_task(bind=True, max_retries=3)
def sync_inventory_task(self, store_id=None):
    """Task per sincronizzazione inventario"""
    try:
        service = GestionaleIntegrationService('gestionale_principale')
        log = service.sync_inventory(store_id)
        
        logger.info(f"Sync inventario completato. Processed: {log.records_processed}, Success: {log.records_success}, Failed: {log.records_failed}")
        
        return {
            'status': log.status,
            'processed': log.records_processed,
            'success': log.records_success,
            'failed': log.records_failed
        }
        
    except Exception as exc:
        logger.error(f"Errore sync inventario: {exc}")
        self.retry(countdown=300, exc=exc)

@shared_task(bind=True, max_retries=3)
def export_orders_task(self, date_from=None, date_to=None):
    """Task per esportazione ordini"""
    try:
        service = GestionaleIntegrationService('gestionale_principale')
        log = service.export_orders(date_from, date_to)
        
        logger.info(f"Export ordini completato. Processed: {log.records_processed}, Success: {log.records_success}, Failed: {log.records_failed}")
        
        return {
            'status': log.status,
            'processed': log.records_processed,
            'success': log.records_success,
            'failed': log.records_failed
        }
        
    except Exception as exc:
        logger.error(f"Errore export ordini: {exc}")
        self.retry(countdown=300, exc=exc)

@shared_task
def daily_sync_products():
    """Task automatico giornaliero sync prodotti"""
    return sync_products_task.delay()

@shared_task  
def hourly_sync_inventory():
    """Task automatico orario sync inventario"""
    return sync_inventory_task.delay()

@shared_task
def daily_export_orders():
    """Task automatico giornaliero export ordini"""
    yesterday = (timezone.now() - timezone.timedelta(days=1)).strftime('%Y-%m-%d')
    return export_orders_task.delay(date_from=yesterday)