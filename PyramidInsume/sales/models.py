
# sales/models.py

from django.db import models
from django.conf import settings
from supplies.models import Insumo

class Venta(models.Model):

    CIUDAD_CHOICES = (
        ('BOG', 'Bogotá'),
        ('MED', 'Medellín'),
        ('CAL', 'Cali'),
        ('BQU', 'Barranquilla'),
        ('CTG', 'Cartagena'),
        ('JAM', 'Jamundí'),
        ('PST', 'Pasto'),
        ('CUN', 'Cúcuta'),
        ('BAY', 'Bucaramanga'),
        ('SAM', 'Santa Marta'),
        ('PER', 'Pereira'),
        ('SAN', 'Santander de Quilichao'),
        ('TUN', 'Tunja'),
        ('OTR', 'Otra'),
    )

    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cantidad_vendida = models.PositiveIntegerField()
    fecha_venta = models.DateTimeField(auto_now_add=True)
    ciudad = models.CharField(
        max_length=3,  # Longitud suficiente para almacenar el código de ciudad
        choices=CIUDAD_CHOICES,
        blank=True,
        null=True,
        verbose_name=('Ciudad')
    )

    class Meta:
        db_table = 'ventas_venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"{self.insumo.nombre} vendido por {self.vendedor.email} - {self.fecha_venta.strftime('%d/%m/%Y')}"
    
    @property
    def total_venta(self):
        return self.insumo.precio_unitario * self.cantidad_vendida
