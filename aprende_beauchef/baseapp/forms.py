from django import forms
from .models import Materia, Afiche

class AficheForm(forms.ModelForm):
    class Meta:
        model = Afiche
        fields = ['url', 'descripcion', 'nombre']

    def __init__(self, *args, **kwargs):
        super(AficheForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].required = False

class PublishForm(forms.Form):
    courses = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Escoge el curso', required=True)
    price = forms.IntegerField(label='Precio estimado', min_value = 0, required=True)
    modality = forms.ChoiceField(choices=[('pres', 'presencial'), ('rem', 'remota')], label='Modalidad', required=True)
    phone = forms.IntegerField(label='Teléfono de contacto', max_value=999999999, required=True)
    disponibility = forms.ChoiceField(choices=[
        ('LUN', 'Lunes'), ('MAR', 'Martes'), ('MIE', 'Miércoles'), 
        ('JUE', 'Jueves'), ('VIE', 'Viernes'), ('SAB', 'Sábado'), ('DOM', 'Domingo')
    ], label='Disponibilidad',required=True)
    time_init = forms.TimeField(label='Hora inicio', widget=forms.TextInput(attrs={'placeholder': 'HH:MM'}) ,required=True)
    time_end = forms.TimeField(label='Hora fin', required=True)