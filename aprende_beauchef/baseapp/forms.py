from django import forms
from .models import Materia, Afiche

# Login Form #


# Register Form #


# Publish Form #


class AficheForm(forms.ModelForm):
    class Meta:
        model = Afiche
        fields = ["url", "descripcion", "nombre"]
        labels = {
            "url": "Sube tu afiche",
            "descripcion": "Escribe una descripción (opcional)",
            "nombre": "Escribe el nombre de tu afiche",
        }

    def __init__(self, *args, **kwargs):
        super(AficheForm, self).__init__(*args, **kwargs)
        self.fields["descripcion"].required = False


class PublishForm(forms.Form):
    courses = forms.ModelChoiceField(
        queryset=Materia.objects.all(), label="Escoge el curso", required=True
    )
    price = forms.IntegerField(
        label="Precio estimado",
        min_value=0,
        widget=forms.TextInput(attrs={"placeholder": "14000"}),
        required=True,
    )
    modality = forms.ChoiceField(
        choices=[("pres", "presencial"), ("rem", "remota")],
        label="Modalidad",
        required=True,
    )
    phone = forms.IntegerField(
        label="Teléfono de contacto",
        max_value=999999999,
        widget=forms.TextInput(attrs={"placeholder": "922224444"}),
        required=True,
    )
    disponibility = forms.ChoiceField(
        choices=[
            ("LUN", "Lunes"),
            ("MAR", "Martes"),
            ("MIE", "Miércoles"),
            ("JUE", "Jueves"),
            ("VIE", "Viernes"),
            ("SAB", "Sábado"),
            ("DOM", "Domingo"),
        ],
        label="Disponibilidad",
        required=True,
    )
    time_init = forms.TimeField(
        label="Hora inicio",
        widget=forms.TextInput(attrs={"placeholder": "HH:MM"}),
        required=True,
    )
    time_end = forms.TimeField(
        label="Hora fin",
        widget=forms.TextInput(attrs={"placeholder": "HH:MM"}),
        required=True,
    )
