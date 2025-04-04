from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'user_type', 'username', 'first_name', 'last_name')
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Solo administradores pueden asignar tipos de usuario
        if self.request and not self.request.user.is_administrador:
            del self.fields['user_type']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'user_type', 'username','first_name', 'last_name', 'is_active')
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Solo administradores pueden cambiar tipos de usuario
        if self.request and not self.request.user.is_administrador:
            del self.fields['user_type']
        
        