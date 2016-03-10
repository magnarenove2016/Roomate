from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

#formato de mensaje para controlar correos duplicados en el registro
DOBLE_EMAIL = _(u"Este Correo ya esta en uso. "u"Por favor utilice otro correo o inicie sesión")

#formulario de registro del usuario.
class RegistrationForm(UserCreationForm):
    
    # Añadir al formulario un campo para el email, el captcha,
    # y un checkbox para que el usuario acepte las condiciones de uso
    email = forms.EmailField(
        required = True
    )
    #añadir el campo de Captcha
    captcha = ReCaptchaField(
        label = 'Captcha'
    )
    #checkbox de licencia el cual el usuario debe aceptar
    tos = forms.BooleanField(
        widget = forms.CheckboxInput,
        label = 'He leído y acepto las condiciones de uso',
        error_messages={'required': 'Debes aceptar las condiciones de uso para continuar'}
    )
    #funcion que se encargar de mirar en la base de datos si es que ya existe el correo com el que se intenta registrarse
    def clean_email(self):
            """
            ya que django solo nos ofrece el formulario de registro, pero no controla que el campo de correo electronico
            no sea doble, asi que con esta funcion cada ves que el usuario le da al boton de registrar verificamos que su correo
            no exista previamente en la base de datos
            """
            if User.objects.filter(email__iexact=self.cleaned_data['email']): #buscar en la base de datos el correo introducido
                raise forms.ValidationError(DOBLE_EMAIL)
            return self.cleaned_data['email']

    # Ampliar la función de guardado para que también guarde el email
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
