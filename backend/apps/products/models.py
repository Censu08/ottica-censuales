from django.db import models
from apps.common.models import TimeStampedModel

class Category(TimeStampedModel):
    """Categorie prodotti gerarchiche"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name

class Brand(TimeStampedModel):
    """Marchi prodotti"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'brands'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    """Modello prodotto base - generalizzato per ottica"""
    # Identificativi
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    # Relazioni
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    
    # Prezzi
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Attributi specifici ottica (JSON per flessibilità)
    optical_attributes = models.JSONField(default=dict, blank=True)
    # Esempi: {"lens_type": "progressive", "material": "titanium", "gender": "unisex"}
    
    # Immagini
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_prescription_required = models.BooleanField(default=False)
    requires_measurement = models.BooleanField(default=False)
    
    # Dimensioni/peso per spedizioni
    weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    dimensions = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category', 'brand']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.brand.name} - {self.name}"

class ProductImage(TimeStampedModel):
    """Immagini aggiuntive prodotto"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'product_images'
        ordering = ['sort_order']

class ProductVariant(TimeStampedModel):
    """Varianti prodotto (colori, taglie, gradazioni)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    
    # Attributi variante
    attributes = models.JSONField(default=dict)
    # Esempi: {"color": "black", "size": "M", "lens_power": "+2.50"}
    
    # Prezzi specifici variante
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Immagine specifica variante
    image = models.ImageField(upload_to='variants/', null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'product_variants'
        unique_together = ['product', 'attributes']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"