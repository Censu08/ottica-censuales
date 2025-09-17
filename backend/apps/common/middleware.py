import logging
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger(__name__)

class APILoggingMiddleware(MiddlewareMixin):
    """Middleware per logging delle API requests"""
    
    def process_request(self, request):
        if request.path.startswith('/api/'):
            logger.info(f"API Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")
    
    def process_response(self, request, response):
        if request.path.startswith('/api/'):
            logger.info(f"API Response: {response.status_code} for {request.method} {request.path}")
        return response

class RateLimitMiddleware(MiddlewareMixin):
    """Middleware per rate limiting delle API"""
    
    def process_request(self, request):
        if not request.path.startswith('/api/'):
            return None
        
        # Estrai IP client
        client_ip = self.get_client_ip(request)
        
        # Chiave cache per rate limiting
        cache_key = f"rate_limit_{client_ip}"
        
        # Controlla rate limit (100 requests per minuto)
        current_count = cache.get(cache_key, 0)
        
        if current_count >= 100:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JsonResponse(
                {"error": "Rate limit exceeded"}, 
                status=429
            )
        
        # Incrementa counter
        cache.set(cache_key, current_count + 1, 60)  # 60 secondi
        
        return None
    
    def get_client_ip(self, request):
        """Estrae l'IP del client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip