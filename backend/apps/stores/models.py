from django.db import models
from django.contrib.auth.models import User
from apps.common.models import TimeStampedModel


class Store(TimeStampedModel):
    """Modello per i negozi fisici Censuales"""
    name = models.CharField(max_length=200, verbose_name="Nome Negozio")
    slug = models.SlugField(unique=True)
    address = models.TextField(verbose_name="Indirizzo Completo")
    city = models.CharField(max_length=100, default="Palermo")
    province = models.CharField(max_length=50, default="PA")
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, verbose_name="Telefono")
    email = models.EmailField(blank=True)

    # Ottico di riferimento (persona fisica)
    optician_name = models.CharField(
        max_length=200,
        verbose_name="Ottico di Riferimento",
        help_text="Nome completo dell'ottico di riferimento"
    )

    # Manager del sistema (utente Django)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_stores',
        verbose_name="Manager Sistema"
    )

    # Settings operativi
    is_active = models.BooleanField(default=True, verbose_name="Attivo")
    accepts_online_orders = models.BooleanField(default=True)
    delivery_available = models.BooleanField(default=False)
    pickup_available = models.BooleanField(default=True)

    # Orari (JSON field per flessibilità)
    opening_hours = models.JSONField(
        default=dict,
        blank=True,
        help_text="Formato: {'monday': {'open': '09:00', 'close': '19:00', 'closed': False}, ...}"
    )

    # Coordinate per geolocalizzazione
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Latitudine"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Longitudine"
    )

    # Informazioni aggiuntive
    description = models.TextField(
        blank=True,
        verbose_name="Descrizione",
        help_text="Breve descrizione del negozio"
    )

    class Meta:
        db_table = 'stores'
        ordering = ['name']
        verbose_name = "Negozio"
        verbose_name_plural = "Negozi"

    def __str__(self):
        return f"{self.name} - {self.optician_name}"

    @property
    def formatted_address(self):
        """Ritorna l'indirizzo formattato per la visualizzazione"""
        return f"{self.address}, {self.city} ({self.province}) {self.postal_code}"