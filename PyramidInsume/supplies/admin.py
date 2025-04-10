from django.contrib import admin
from .models import Insumo

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_disponible', 'precio_unitario', 'esta_publicado', 'creado_por', 'fecha_creacion')
    list_filter = ('esta_publicado', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('creado_por', 'fecha_creacion')

    def save_model(self, request, obj, form, change):
        # Solo permitir que el administrador cree insumos
        if not change and request.user.user_type != 1:
            raise PermissionError("Solo el administrador puede crear insumos.")
        if not obj.creado_por:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
