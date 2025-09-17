import uuid
import hashlib
from decimal import Decimal
from typing import Dict, Any, Optional
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import io

def generate_sku() -> str:
    """Genera un SKU univoco"""
    return f"OC{uuid.uuid4().hex[:8].upper()}"

def generate_order_number() -> str:
    """Genera numero ordine univoco"""
    return f"ORD{uuid.uuid4().hex[:10].upper()}"

def calculate_tax(amount: Decimal, rate: Decimal = Decimal('0.22')) -> Decimal:
    """Calcola tasse (IVA italiana 22% default)"""
    return (amount * rate).quantize(Decimal('0.01'))

def format_currency(amount: Decimal, currency: str = 'EUR') -> str:
    """Formatta importo in valuta"""
    if currency == 'EUR':
        return f"€ {amount:.2f}"
    return f"{amount:.2f} {currency}"

def slugify_italian(text: str) -> str:
    """Crea slug compatibile con caratteri italiani"""
    import re
    from django.utils.text import slugify
    
    # Sostituzioni specifiche per l'italiano
    replacements = {
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
        text = text.replace(old.upper(), new.upper())
    
    return slugify(text)

def resize_image(image_file, max_width: int = 800, max_height: int = 800, quality: int = 85) -> ContentFile:
    """Ridimensiona immagine mantenendo aspect ratio"""
    try:
        # Apri immagine
        image = Image.open(image_file)
        
        # Converti in RGB se necessario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Calcola dimensioni mantenendo aspect ratio
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Salva in memoria
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return ContentFile(output.read())
    
    except Exception as e:
        logger.error(f"Errore ridimensionamento immagine: {e}")
        return image_file

def validate_italian_postal_code(code: str) -> bool:
    """Valida CAP italiano (5 cifre)"""
    import re
    return bool(re.match(r'^\d{5}$', code))

def validate_italian_phone(phone: str) -> bool:
    """Valida numero telefono italiano"""
    import re
    # Formato: +39 xxx xxx xxxx o 3xx xxx xxxx
    patterns = [
        r'^\+39\s?\d{3}\s?\d{3}\s?\d{4}$',
        r'^3\d{2}\s?\d{3}\s?\d{4}$',
        r'^0\d{1,4}\s?\d{6,8}$'
    ]
    
    cleaned_phone = phone.replace(' ', '').replace('-', '')
    return any(re.match(pattern, cleaned_phone) for pattern in patterns)
