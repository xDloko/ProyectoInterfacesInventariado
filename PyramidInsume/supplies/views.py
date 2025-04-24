from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Insumo
from .forms import InsumoForm  # Import the InsumoForm
from django.urls import reverse_lazy  # Import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

def is_administrador(user):
    return user.is_authenticated and user.is_administrador

def is_promotor(user):
    return user.is_authenticated and user.is_promotor

def is_admin_or_promotor(user):
    return user.is_authenticated and user.is_admin_or_promotor

class SuppliesListView(ListView):
    model = Insumo
    template_name = 'supplies/supplies_list.html'
    context_object_name = 'users'
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_administrador))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'insumos': self.get_queryset()})
    
class SuppliesCreateView(CreateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'supplies/supplies_form.html'
    success_url = reverse_lazy('supplies_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_administrador))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs
    
class SuppliesUpdateView(UpdateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'supplies/supplies_form.html'
    success_url = reverse_lazy('supplies_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_administrador))
    def dispatch(self, *args, **kwargs):
        # Solo administradores pueden editar usuarios
        if not self.request.user.is_administrador and self.request.user.pk != self.get_object().pk:
            return redirect('permission_denied')
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

class SuppliesDeleteView(DeleteView):
    model = Insumo
    template_name = 'supplies/supplies_confirm_delete.html'
    success_url = reverse_lazy('supplies_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_administrador))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



