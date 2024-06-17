from django import forms



# Login Form #
class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=25,
                            widget=forms.TextInput(attrs={'class': 'username_input','id': 'username'}), 
                            required=True, error_messages={'required': 'Este campo es obligatorio'})
    password = forms.CharField(label="Contraseña", 
                            widget=forms.PasswordInput(attrs={'class': 'password_input','id': 'password'}), 
                            required=True, error_messages={'required': 'Este campo es obligatorio'})

class LoginRecoveryPassword(forms.Form):
    email = forms.EmailField(label="Correo electrónico", max_length=50, 
                            widget=forms.TextInput(attrs={'class': 'email','id': 'username'}), 
                            error_messages={'required': 'Este campo es obligatorio'}, required=True)

class LoginNewPassword(forms.Form):
    password = forms.CharField(label="Contraseña", 
                            widget=forms.PasswordInput(attrs={'class': 'password_input','id': 'password'}), 
                            required=True, error_messages={'required': 'Este campo es obligatorio'})
    confirmPassword = forms.CharField(label="Confirmar contraseña", 
                                    widget=forms.PasswordInput(attrs={'class': 'password_input','id': 'password'}), 
                                    required=True, error_messages={'required': 'Este campo es obligatorio'})
                                    