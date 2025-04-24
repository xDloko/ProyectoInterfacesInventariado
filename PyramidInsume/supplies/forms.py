from django import forms
from .models import Insumo

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'cantidad_disponible', 'precio_unitario', 'esta_publicado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'esta_publicado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del insumo',
            'descripcion': 'Descripción',
            'cantidad_disponible': 'Cantidad disponible',
            'precio_unitario': 'Precio unitario',
            'esta_publicado': '¿Disponible para venta?',
        }

