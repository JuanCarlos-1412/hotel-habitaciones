from django import forms
from .models import Habitacion


class CrearHabitacionForm(forms.ModelForm):
    def clean(self):
        datos = super().clean()
        tipo = datos.get("tipo")
        capacidad = datos.get("capacidad")

        if tipo == "individual" and capacidad is not None and capacidad != 1:
            self.add_error(
                "capacidad",
                "Una habitación individual debe tener capacidad para 1 persona."
            )

        return datos

    class Meta:
        model = Habitacion
        fields = [
            "numero",
            "tipo",
            "capacidad",
            "precio_noche",
            "piso",
            "estado",
            "descripcion",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "precio_noche": forms.NumberInput(
                attrs={"step": "0.01", "min": "0.01"}
            ),
        }


class EditarHabitacionForm(CrearHabitacionForm):
    class Meta(CrearHabitacionForm.Meta):
        fields = [
            "estado",
            "precio_noche",
            "tipo",
            "capacidad",
            "piso",
            "descripcion",
        ]