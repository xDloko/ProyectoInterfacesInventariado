from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from supplies.models import Insumo
from .models import Venta  # Asumiendo que ya creaste este modelo
from .forms import VentaForm  # Import the VentaForm class
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import defaultdict



class SalesList(ListView):
    model = Venta
    template_name = 'sales/sales_list.html'
    context_object_name = 'ventas'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return Venta.objects.select_related('insumo', 'vendedor')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ventas = self.get_queryset()

        context['total_ventas'] = ventas.aggregate(total=Sum('cantidad_vendida'))['total'] or 0
        context['total_dinero'] = sum(v.total_venta for v in ventas)

        context['ventas_por_insumo'] = (
            ventas.values('insumo__nombre')
            .annotate(total=Sum('cantidad_vendida'))
            .order_by('-total')[:5]
        )

        context['ventas_por_vendedor'] = (
            ventas.values('vendedor__email')
            .annotate(total=Sum('cantidad_vendida'))
            .order_by('-total')[:10]
        )


        ventas_mensuales = defaultdict(int)
        for venta in ventas:
            mes = venta.fecha_venta.strftime('%Y-%m')  # Formato: 2025-05
            ventas_mensuales[mes] += venta.cantidad_vendida

        context['ventas_mensuales'] = [
            {'mes': k, 'total': v} for k, v in sorted(ventas_mensuales.items())
        ]

        dinero_mensual = defaultdict(float)
        for venta in ventas:
            mes = venta.fecha_venta.strftime('%Y-%m')
            dinero_mensual[mes] += float(venta.total_venta)

        context['dinero_mensual'] = [
            {'mes': k, 'total': v} for k, v in sorted(dinero_mensual.items())
        ]

        return context
    


@method_decorator(login_required, name='dispatch')
class VentaCreateView(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'sales/sales_form.html'
    success_url = reverse_lazy('venta_create')  # redirige a sí misma

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        venta = form.save(commit=False)
        venta.vendedor = self.request.user
        venta.save()

        # Actualizar el stock del insumo
        venta.insumo.cantidad_disponible -= venta.cantidad_vendida
        venta.insumo.save()

        messages.success(self.request, f"Venta registrada: {venta.cantidad_vendida} unidades de {venta.insumo.nombre}.")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_vendedor and not request.user.is_administrador:
            messages.error(request, "No tienes permiso para realizar ventas.")
            return redirect('sales_list')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class VentaUpdateView(UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = 'sales/sales_form.html'
    success_url = reverse_lazy('sales_list')  # ajusta según tus rutas

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        venta = form.save(commit=False)
        venta_anterior = Venta.objects.get(pk=venta.pk)
        insumo = venta.insumo

        diferencia = venta.cantidad_vendida - venta_anterior.cantidad_vendida

        if diferencia != 0:
            # Actualizar la cantidad disponible del insumo
            insumo.cantidad_disponible -= diferencia
            insumo.save()

        venta.save()
        messages.success(self.request, f"Venta actualizada: {venta.cantidad_vendida} unidades de {venta.insumo.nombre}.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar la venta.")
        return super().form_invalid(form)


class VentaDeleteView(DeleteView):
    model = Venta
    template_name = 'sales/sales_confirm_delete.html'
    success_url = reverse_lazy('sales_list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)