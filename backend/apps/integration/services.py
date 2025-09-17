import logging
import requests
from typing import Dict, List, Any, Optional
from django.utils import timezone
from decimal import Decimal
from .models import IntegrationLog, ExternalSystemConfig
from apps.products.models import Product, Brand, Category
from apps.inventory.models import StoreInventory, InventoryMovement
from apps.stores.models import Store
from apps.orders.models import Order

logger = logging.getLogger(__name__)

class BaseIntegrationService:
    """Classe base per servizi di integrazione"""
    
    def __init__(self, system_name: str):
        try:
            self.config = ExternalSystemConfig.objects.get(
                name=system_name, 
                is_active=True
            )
        except ExternalSystemConfig.DoesNotExist:
            raise ValueError(f"Sistema esterno '{system_name}' non configurato")
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Effettua richiesta HTTP al sistema esterno"""
        url = f"{self.config.endpoint_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        # Autenticazione
        if self.config.api_key:
            headers['Authorization'] = f"Bearer {self.config.api_key}"
        
        auth = None
        if self.config.username and self.config.password:
            auth = (self.config.username, self.config.password)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                auth=auth,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"Errore richiesta {method} {url}: {e}")
            raise
    
    def _log_operation(self, operation_type: str, **kwargs) -> IntegrationLog:
        """Crea log operazione"""
        return IntegrationLog.objects.create(
            operation_type=operation_type,
            started_at=timezone.now(),
            **kwargs
        )
    
    def _update_log(self, log: IntegrationLog, status: str, **kwargs):
        """Aggiorna log operazione"""
        log.status = status
        log.completed_at = timezone.now()
        
        for field, value in kwargs.items():
            setattr(log, field, value)
        
        log.save()

class GestionaleIntegrationService(BaseIntegrationService):
    """Servizio integrazione con gestionale aziendale"""
    
    def sync_products(self) -> IntegrationLog:
        """Sincronizza prodotti dal gestionale"""
        log = self._log_operation('sync_products', status='running')
        
        try:
            # Recupera prodotti dal gestionale
            response = self._make_request('GET', '/api/products')
            products_data = response.get('products', [])
            
            log.records_processed = len(products_data)
            success_count = 0
            failed_count = 0
            messages = []
            
            for product_data in products_data:
                try:
                    # Mappa dati prodotto
                    mapped_data = self._map_product_data(product_data)
                    
                    # Crea o aggiorna prodotto
                    product, created = Product.objects.update_or_create(
                        sku=mapped_data['sku'],
                        defaults=mapped_data
                    )
                    
                    action = "creato" if created else "aggiornato"
                    messages.append(f"Prodotto {product.sku} {action}")
                    success_count += 1
                    
                except Exception as e:
                    error_msg = f"Errore prodotto {product_data.get('sku', 'N/A')}: {str(e)}"
                    messages.append(error_msg)
                    logger.error(error_msg)
                    failed_count += 1
            
            self._update_log(
                log, 'completed',
                records_success=success_count,
                records_failed=failed_count,
                log_messages='\n'.join(messages)
            )
            
        except Exception as e:
            self._update_log(
                log, 'failed',
                error_details=str(e)
            )
            logger.error(f"Errore sync prodotti: {e}")
        
        return log
    
    def sync_inventory(self, store_id: Optional[int] = None) -> IntegrationLog:
        """Sincronizza inventario dal gestionale"""
        log = self._log_operation('sync_inventory', parameters={'store_id': store_id}, status='running')
        
        try:
            # Parametri richiesta
            params = {}
            if store_id:
                params['store_id'] = store_id
            
            # Recupera inventario dal gestionale
            response = self._make_request('GET', '/api/inventory', params)
            inventory_data = response.get('inventory', [])
            
            log.records_processed = len(inventory_data)
            success_count = 0
            failed_count = 0
            messages = []
            
            for inv_data in inventory_data:
                try:
                    # Trova prodotto e store
                    product = Product.objects.get(sku=inv_data['product_sku'])
                    store = Store.objects.get(slug=inv_data['store_slug'])
                    
                    # Aggiorna o crea inventario
                    inventory, created = StoreInventory.objects.update_or_create(
                        store=store,
                        product=product,
                        defaults={
                            'quantity': inv_data.get('quantity', 0),
                            'store_price': Decimal(str(inv_data.get('price', product.base_price))),
                            'is_online_available': inv_data.get('online_available', True),
                            'last_restocked': timezone.now()
                        }
                    )
                    
                    # Log movimento se necessario
                    if not created and inventory.quantity != inv_data.get('quantity', 0):
                        InventoryMovement.objects.create(
                            store=store,
                            product=product,
                            movement_type='adjustment',
                            quantity_change=inv_data.get('quantity', 0) - inventory.quantity,
                            quantity_after=inv_data.get('quantity', 0),
                            reference_id='sync_gestionale',
                            notes=f'Sincronizzazione automatica da gestionale'
                        )
                    
                    action = "creato" if created else "aggiornato"
                    messages.append(f"Inventario {store.name} - {product.sku} {action}")
                    success_count += 1
                    
                except (Product.DoesNotExist, Store.DoesNotExist) as e:
                    error_msg = f"Errore inventario {inv_data.get('product_sku', 'N/A')}: {str(e)}"
                    messages.append(error_msg)
                    failed_count += 1
                
                except Exception as e:
                    error_msg = f"Errore inventario {inv_data.get('product_sku', 'N/A')}: {str(e)}"
                    messages.append(error_msg)
                    logger.error(error_msg)
                    failed_count += 1
            
            self._update_log(
                log, 'completed',
                records_success=success_count,
                records_failed=failed_count,
                log_messages='\n'.join(messages)
            )
            
        except Exception as e:
            self._update_log(
                log, 'failed',
                error_details=str(e)
            )
            logger.error(f"Errore sync inventario: {e}")
        
        return log
    
    def export_orders(self, date_from: str = None, date_to: str = None) -> IntegrationLog:
        """Esporta ordini verso gestionale"""
        log = self._log_operation(
            'export_orders', 
            parameters={'date_from': date_from, 'date_to': date_to},
            status='running'
        )
        
        try:
            # Filtra ordini da esportare
            orders_query = Order.objects.filter(
                status__in=['confirmed', 'processing']
            ).select_related('customer', 'store').prefetch_related('items__product')
            
            if date_from:
                orders_query = orders_query.filter(created_at__gte=date_from)
            if date_to:
                orders_query = orders_query.filter(created_at__lte=date_to)
            
            orders = list(orders_query)
            log.records_processed = len(orders)
            
            success_count = 0
            failed_count = 0
            messages = []
            
            for order in orders:
                try:
                    # Mappa ordine per gestionale
                    order_data = self._map_order_data(order)
                    
                    # Invia al gestionale
                    response = self._make_request('POST', '/api/orders', order_data)
                    
                    # Aggiorna stato ordine se necessario
                    if response.get('success'):
                        external_id = response.get('order_id')
                        # Qui potresti salvare l'ID esterno in un campo dell'ordine
                        messages.append(f"Ordine {order.order_number} esportato (ID: {external_id})")
                        success_count += 1
                    
                except Exception as e:
                    error_msg = f"Errore export ordine {order.order_number}: {str(e)}"
                    messages.append(error_msg)
                    logger.error(error_msg)
                    failed_count += 1
            
            self._update_log(
                log, 'completed',
                records_success=success_count,
                records_failed=failed_count,
                log_messages='\n'.join(messages)
            )
            
        except Exception as e:
            self._update_log(
                log, 'failed',
                error_details=str(e)
            )
            logger.error(f"Errore export ordini: {e}")
        
        return log
    
    def _map_product_data(self, external_data: Dict) -> Dict:
        """Mappa dati prodotto dal formato gestionale al formato interno"""
        # Trova o crea categoria
        category_name = external_data.get('category', 'Senza Categoria')
        category, _ = Category.objects.get_or_create(
            name=category_name,
            defaults={'slug': category_name.lower().replace(' ', '-')}
        )
        
        # Trova o crea brand
        brand_name = external_data.get('brand', 'Generico')
        brand, _ = Brand.objects.get_or_create(
            name=brand_name,
            defaults={'slug': brand_name.lower().replace(' ', '-')}
        )
        
        return {
            'sku': external_data['sku'],
            'name': external_data['name'],
            'slug': external_data['name'].lower().replace(' ', '-'),
            'description': external_data.get('description', ''),
            'short_description': external_data.get('short_description', ''),
            'category': category,
            'brand': brand,
            'base_price': Decimal(str(external_data.get('price', 0))),
            'cost_price': Decimal(str(external_data.get('cost_price', 0))),
            'optical_attributes': external_data.get('attributes', {}),
            'is_active': external_data.get('active', True),
            'weight': external_data.get('weight'),
        }
    
    def _map_order_data(self, order: Order) -> Dict:
        """Mappa ordine dal formato interno al formato gestionale"""
        return {
            'order_number': order.order_number,
            'customer': {
                'email': order.customer.user.email,
                'first_name': order.customer.user.first_name,
                'last_name': order.customer.user.last_name,
                'phone': order.customer.phone,
            },
            'store_code': order.store.slug,
            'status': order.status,
            'fulfillment_method': order.fulfillment_method,
            'billing_address': {
                'first_name': order.billing_address.first_name,
                'last_name': order.billing_address.last_name,
                'address': order.billing_address.address_line_1,
                'city': order.billing_address.city,
                'postal_code': order.billing_address.postal_code,
                'phone': order.billing_address.phone,
            },
            'items': [
                {
                    'sku': item.product.sku,
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'unit_price': str(item.unit_price),
                    'total_price': str(item.total_price),
                    'customizations': item.customizations,
                }
                for item in order.items.all()
            ],
            'totals': {
                'subtotal': str(order.subtotal),
                'tax_amount': str(order.tax_amount),
                'shipping_amount': str(order.shipping_amount),
                'total_amount': str(order.total_amount),
            },
            'created_at': order.created_at.isoformat(),
        }