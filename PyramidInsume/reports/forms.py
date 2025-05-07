
from django import forms
import datetime

class ReporteForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    mostrar_insumos = forms.BooleanField(label='Mostrar Insumos', required=False)
    mostrar_usuarios = forms.BooleanField(label='Mostrar Usuarios', required=False)
    mostrar_ventas = forms.BooleanField(label='Mostrar Ventas', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fechas por defecto: hoy -7 días y hoy
        self.fields['fecha_inicio'].initial = datetime.date.today() - datetime.timedelta(days=7)
        self.fields['fecha_fin'].initial = datetime.date.today()