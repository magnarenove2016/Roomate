from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Formato de mensaje para controlar correos duplicados en el registro
DOBLE_EMAIL = _(u"Este correo ya est&aacute; en uso. "u"Por favor utilice otro correo o inicie sesi&oacte;n")

# Formulario de registro del usuario.
class RegistrationForm(UserCreationForm):
    
    # Anadir al formulario un campo para el email, el captcha,
    # y un checkbox para que el usuario acepte las condiciones de uso
    email = forms.EmailField(
        required = True
    )

    #Anadir el campo de Captcha
    captcha = ReCaptchaField(
        label = 'Captcha'
    )

    #Checkbox de licencia el cual el usuario debe aceptar
    tos = forms.BooleanField(
        widget = forms.CheckboxInput,
        label = 'He le&iacute;do y acepto las condiciones de uso',
        error_messages={'required': 'Debes aceptar las condiciones de uso para continuar'}
    )

    # Funcion que se encargar de mirar en la base de datos
    # si existe el correo con el que intenta registrarse
    def clean_email(self):
            """
            Ya que Django solo nos ofrece el formulario de registro, pero no controla que el campo de correo electronico
            no sea doble, asi que con esta funcion cada vez que el usuario le da al boton de registrar verificamos que su correo
            no exista previamente en la base de datos.
            """
            if User.objects.filter(email__iexact=self.cleaned_data['email']): # Buscar en la base de datos el correo introducido
                raise forms.ValidationError(DOBLE_EMAIL)
            return self.cleaned_data['email']

    # Ampliar la funcion de guardado para que tambien guarde el email
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

