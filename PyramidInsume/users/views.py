from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

def is_administrador(user):
    return user.is_authenticated and user.is_administrador

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_administrador))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_administrador))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # Solo administradores pueden editar usuarios
        if not self.request.user.is_administrador and self.request.user.pk != self.get_object().pk:
            return redirect('permission_denied')
        return super().dispatch(*args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_administrador))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
@user_passes_test(is_administrador)
def toggle_user_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('user_list')


#login

class CustomLoginView(LoginView):
    template_name = 'login/login.html'
    redirect_authenticated_user = True  # Redirige si ya está autenticado
    
    def get_success_url(self):
        user = self.request.user
        if user.is_administrador:
            return reverse_lazy('admin_dashboard')
        elif user.is_vendedor:
            return reverse_lazy('sales_dashboard')
        return reverse_lazy('home')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')