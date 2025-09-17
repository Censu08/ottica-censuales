# backend/apps/products/models.py
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
    PRODUCT_TYPES = [
        ('glasses', 'Occhiali da Vista'),
        ('sunglasses', 'Occhiali da Sole'),
        ('contact_lenses', 'Lenti a Contatto'),
        ('accessories', 'Accessori'),
    ]

    # Identificativi
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=300, blank=True)

    # Categorizzazione
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)

    # Prezzi
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Immagini
    main_image = models.ImageField(upload_to='products/', null=True, blank=True)

    # SEO e metadata
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Specifiche tecniche prodotto ottica (JSON per flessibilità)
    specifications = models.JSONField(default=dict, blank=True)
    # Esempio: {"frame_material": "acetato", "lens_type": "progressiva", "protection": "UV400"}

    # Weight per spedizioni
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['category', 'brand']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

    @property
    def current_price(self):
        """Ritorna il prezzo attuale (sale_price se disponibile, altrimenti price)"""
        return self.sale_price if self.sale_price else self.price


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

    def __str__(self):
        return f"{self.product.name} - {self.name}"