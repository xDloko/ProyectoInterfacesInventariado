from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'cedula', 'user_type', 'username', 'first_name', 'last_name', 'ciudad')
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Solo administradores pueden asignar tipos de usuario
        if self.request and not self.request.user.is_administrador:
            del self.fields['user_type']

        self.fields['ciudad'].widget = forms.Select(
            attrs={'class': 'form-control city-field'},
            choices=self.Meta.model.CIUDAD_CHOICES
        )

    def save(self, commit=True):
        # Asignamos el usuario autenticado como creador del nuevo usuario
        user = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            user.created_by = self.request.user  # Asignamos el creador
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'cedula', 'user_type', 'username','first_name', 'last_name', 'is_active', 'ciudad')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control email-field'}),
            'user_type': forms.Select(attrs={'class': 'form-check-input'}),
            'username': forms.TextInput(attrs={'class': 'form-control username-field'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control first-name-field'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control last-name-field'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control is-active-field'}),
            'ciudad': forms.Select(attrs={'class': 'form-control city-field'}, choices=User.CIUDAD_CHOICES),
            'cedula': forms.TextInput(attrs={'class': 'form-control city-field'}),
            
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
        

        
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Correo electrónico o Cédula'),
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Intentar autenticar al usuario por correo o cédula
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            # Si no se encontró usuario
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Correo electrónico, cédula o contraseña incorrectos."),
                    code='invalid_login',
                )

            # Si el usuario está inactivo
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    _("Tu cuenta está inactiva. Contacta con el administrador."),
                    code='inactive_user',
                )

        return self.cleaned_data