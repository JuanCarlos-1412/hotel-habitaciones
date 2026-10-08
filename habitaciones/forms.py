from django import forms
from .models import Habitacion

class CrearHabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'capacidad', 'precio_noche', 'piso', 'estado', 'descripcion']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3}), 'precio_noche': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'})}

class EditarHabitacionForm(CrearHabitacionForm):
    # La identidad de la habitación permanece fija durante la edición.
    class Meta(CrearHabitacionForm.Meta):
        fields = ['estado', 'precio_noche', 'tipo', 'capacidad', 'piso', 'descripcion']
