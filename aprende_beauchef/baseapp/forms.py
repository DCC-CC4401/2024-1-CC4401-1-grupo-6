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


# Index forms #


class FilterForm(forms.Form):
    search = forms.CharField(
        label="Buscador",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre del curso",
                "class": "filtro",
                "id": "buscador",
            }
        ),
        required=False,
    )
    max_price = forms.IntegerField(
        label="Precio máximo",
        widget=forms.TextInput(
            attrs={"placeholder": "0", "class": "precio", "id": "min"}
        ),
        min_value=0,
        required=False,
    )
    min_price = forms.IntegerField(
        label="Precio mínimo",
        widget=forms.TextInput(
            attrs={"placeholder": "0", "class": "precio", "id": "max"}
        ),
        min_value=0,
        required=False,
    )
    modality = forms.ChoiceField(
        choices=[("AMB", "Ambas"), ("pres", "Presencial"), ("rem", "Online")],
        label="Modalidad",
        required=False,
    )
    disponibility = forms.ChoiceField(
        choices=[
            ("ALL", "Todos"),
            ("LUN", "Lunes"),
            ("MAR", "Martes"),
            ("MIE", "Miércoles"),
            ("JUE", "Jueves"),
            ("VIE", "Viernes"),
            ("SAB", "Sábado"),
            ("DOM", "Domingo"),
        ],
        label="Disponibilidad",
        required=False,
    )

# Register form

class RegisterForm(forms.Form):
    name = forms.CharField(
        label="Nombre",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre Apellido",
                "class": "name_input",
                "id": "name",
            }
        ),
        required=True,
    )
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre de usuario",
                "class": "username_input",
                "id": "username",
            }
        ),
        required=True,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "xxxxx@xxxx.xx",
                "class": "email_input",
                "id": "email",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "password_input",
                "id": "password",
            }
        ),
        required=True,
    )
    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmar contraseña",
                "class": "password2_input",
                "id": "password2",
            }
        ),
        required=True,
    )