from django import forms
from .models import Venta, Insumo

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['insumo', 'cantidad_vendida', 'ciudad']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        venta = self.instance if self.instance.pk else None

        # Mostrar todos los insumos disponibles
        insumos = Insumo.objects.filter(esta_publicado=True, cantidad_disponible__gt=0)

        # Si estamos editando y el insumo ya fue seleccionado, lo agregamos aunque tenga disponibilidad 0
        if venta and venta.insumo and venta.insumo not in insumos:
            insumos = list(insumos) + [venta.insumo]

        # Mostrar nombre con cantidad entre paréntesis
        self.fields['insumo'].queryset = Insumo.objects.filter(pk__in=[i.pk for i in insumos])
        self.fields['insumo'].label_from_instance = lambda obj: f"{obj.nombre} ({obj.cantidad_disponible} disponibles)"

        self.fields['cantidad_vendida'].widget.attrs.update({'min': 1})

    def clean(self):
        cleaned_data = super().clean()
        insumo = cleaned_data.get('insumo')
        nueva_cantidad = cleaned_data.get('cantidad_vendida')

        if not insumo or nueva_cantidad is None:
            return cleaned_data

        if self.instance.pk:  # estamos editando una venta existente
            venta_anterior = Venta.objects.get(pk=self.instance.pk)
            cantidad_original = venta_anterior.cantidad_vendida
            diferencia = nueva_cantidad - cantidad_original

            if diferencia > insumo.cantidad_disponible:
                raise forms.ValidationError(
                    f"No hay suficientes unidades disponibles para actualizar la venta. "
                    f"Solo puedes agregar hasta {insumo.cantidad_disponible + cantidad_original} unidades."
                )
        else:  # es una nueva venta
            if nueva_cantidad > insumo.cantidad_disponible:
                raise forms.ValidationError(
                    f"La cantidad solicitada excede la disponibilidad del insumo ({insumo.cantidad_disponible})."
                )

        return cleaned_data
