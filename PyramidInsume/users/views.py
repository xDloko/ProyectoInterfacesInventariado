from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import logout
from .forms import CustomLoginForm

def is_administrador(user):
    return user.is_authenticated and user.is_administrador

def is_supervisor(user):
    return user.is_authenticated and user.is_supervisor

def is_admin_or_surpervisor(user):
    return user.is_authenticated and user.is_admin_or_supervisor

class DashBoard(View):
    template_name = 'users/dashboard.html'
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_admin_or_surpervisor))


    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Obtener el usuario actual
        user = self.request.user

        # Si el usuario es un vendedor, mostrar solo los usuarios que él creó
        if user.is_vendedor:
            return User.objects.filter(created_by=user)

        # Si el usuario es administrador o supervisor, mostrar todos los usuarios
        elif user.is_administrador or user.is_supervisor:
            return User.objects.all()

        # Por defecto, no mostrar ningún usuario
        return User.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_vendedor'] = self.request.user.is_vendedor
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_vendedor'] = self.request.user.is_vendedor

        # Si el usuario es administrador, agregar información sobre los usuarios creados
        if self.request.user.is_administrador:
            users_with_created_info = []
            for user in self.get_queryset():
                created_users_count = user.created_users.count()
                created_users_names = [created_user.get_full_name() for created_user in user.created_users.all()]
                users_with_created_info.append({
                    'user': user,
                    'created_users_count': created_users_count,
                    'created_users_names': created_users_names,
                })
            context['users_with_created_info'] = users_with_created_info

        elif self.request.user.is_supervisor:
            users_with_created_info = []
            for user in self.get_queryset():
                created_users_count = user.created_users.count()
                created_users_names = [created_user.get_full_name() for created_user in user.created_users.all()]
                users_with_created_info.append({
                    'user': user,
                    'created_users_count': created_users_count,
                    'created_users_names': created_users_names,
                })
            context['users_with_created_info'] = users_with_created_info

        

        return context

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    
    @method_decorator(login_required)
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
        if not self.request.user.is_administrador and not self.request.user.is_supervisor and self.request.user.pk != self.get_object().pk:
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
    

login_required
user_passes_test(is_admin_or_surpervisor)
def toggle_user_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active == False:
        user.is_active = True
    else:
        user.is_active = not user.is_active
    user.save()
    return redirect('user_list')






#login


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm 
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.is_administrador:
            return reverse_lazy('admin_dashboard')
        elif user.is_vendedor:
            return reverse_lazy('sales_list')
        elif user.is_supervisor:
            return reverse_lazy('user_list')
        return reverse_lazy('home')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

