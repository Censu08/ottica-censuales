from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .utils import validate_italian_postal_code, validate_italian_phone

def validate_sku(value):
    """Valida formato SKU"""
    import re
    if not re.match(r'^[A-Z0-9\-]{6,20}$', value):
        raise ValidationError(_('SKU deve contenere solo lettere maiuscole, numeri e trattini (6-20 caratteri)'))

def validate_postal_code(value):
    """Valida CAP italiano"""
    if not validate_italian_postal_code(value):
        raise ValidationError(_('Inserire un CAP valido (5 cifre)'))

def validate_phone_number(value):
    """Valida numero di telefono italiano"""
    if not validate_italian_phone(value):
        raise ValidationError(_('Inserire un numero di telefono italiano valido'))

def validate_positive_decimal(value):
    """Valida che il decimale sia positivo"""
    if value < 0:
        raise ValidationError(_('Il valore deve essere positivo'))