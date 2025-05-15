from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'user_type', 'username', 'first_name', 'last_name', 'ciudad')
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Solo administradores pueden asignar tipos de usuario
        if self.request and not self.request.user.is_administrador:
            del self.fields['user_type']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'user_type', 'username','first_name', 'last_name', 'is_active', 'ciudad')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control email-field'}),
            'user_type': forms.Select(attrs={'class': 'form-check-input'}),
            'username': forms.TextInput(attrs={'class': 'form-control username-field'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control first-name-field'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control last-name-field'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control is-active-field'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control city-field'}),
            
        }
        labels = {
            'email': 'Correo Electrónico',
            'user_type': 'Tipo de Usuario',
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'is_active': 'Estado del Usuario: ',
            'ciudad': 'Ciudad',
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Si es supervisor, limita los campos visibles
        if self.request and self.request.user.is_supervisor:
            allowed_fields = ['is_active']
            for field_name in list(self.fields.keys()):
                if field_name not in allowed_fields:
                    del self.fields[field_name]
        

        
        
        