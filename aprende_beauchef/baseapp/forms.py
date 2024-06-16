from django import forms

class FilterForm(forms.Form):
    search = forms.CharField(label="Buscador", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre del curso', 'class': 'filtro','id': 'buscador'}), required=False)
    max_price = forms.IntegerField(label='Precio máximo',widget=forms.TextInput(attrs={'placeholder': '0', 'class': 'precio','id': 'min'}), min_value=0 ,required=False)
    min_price = forms.IntegerField(label='Precio mínimo',widget=forms.TextInput(attrs={'placeholder': '0', 'class': 'precio','id': 'max'}), min_value=0 ,required=False)
    modality = forms.ChoiceField(choices=[('AMB', 'Ambas'),('pres', 'Presencial'), ('rem', 'Online')], label='Modalidad', required=False)
    disponibility = forms.ChoiceField(choices=[
        ('ALL', 'Todos') ,('LUN', 'Lunes'), ('MAR', 'Martes'), ('MIE', 'Miércoles'), 
        ('JUE', 'Jueves'), ('VIE', 'Viernes'), ('SAB', 'Sábado'), ('DOM', 'Domingo')    
    ], label='Disponibilidad', required=False)