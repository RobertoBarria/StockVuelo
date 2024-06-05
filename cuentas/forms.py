from django import forms
from django.contrib.auth.forms import AuthenticationForm
from aviones.models import Avion

class LoginForm(AuthenticationForm):
    avion = forms.ModelChoiceField(queryset=Avion.objects.all(), required=True, label='Avión')
        
    class Meta:
        fields = ['username', 'password', 'avion']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Correo electrónico"
        self.fields['password'].label = "Contraseña"

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'Por favor introduzca email y contraseña correctos. Note que puede que ambos campos sean estrictos en relación a diferencias entre mayúsculas y minúsculas.'        