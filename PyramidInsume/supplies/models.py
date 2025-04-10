from django.db import models
from django.conf import settings

class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad_disponible = models.PositiveIntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    esta_publicado = models.BooleanField(default=False)  # Disponible para venta
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'user_type': 1},  # Solo administradores pueden crear
        related_name='insumos_creados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'insumos_insumo'
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'

    def __str__(self):
        return self.nombre
    