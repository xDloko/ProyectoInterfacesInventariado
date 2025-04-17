from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from supplies.models import Insumo
from .models import Venta  # Asumiendo que ya creaste este modelo
from django.utils import timezone

# Dashboard principal
class DashboardView(TemplateView):
    template_name = 'sales/sales_dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


# Registrar venta - solo vendedores
@login_required
def registrar_venta(request):
    if not request.user.is_vendedor:
        messages.error(request, "No tienes permiso para realizar ventas.")
        return redirect('sales_dashboard')

    insumos_disponibles = Insumo.objects.filter(esta_publicado=True, cantidad_disponible__gt=0)

    if request.method == 'POST':
        insumo_id = request.POST.get('insumo_id')
        cantidad = int(request.POST.get('cantidad'))

        insumo = get_object_or_404(Insumo, id=insumo_id)

        if cantidad > insumo.cantidad_disponible:
            messages.error(request, "La cantidad solicitada excede la disponibilidad.")
        else:
            Venta.objects.create(
                insumo=insumo,
                vendedor=request.user,
                cantidad_vendida=cantidad,
                fecha_venta=timezone.now()
            )
            insumo.cantidad_disponible -= cantidad
            insumo.save()
            messages.success(request, f"Venta registrada: {cantidad} unidades de {insumo.nombre}.")
            return redirect('registrar_venta')

    return render(request, 'sales/registrar_venta.html', {
        'insumos': insumos_disponibles
    })
