import re

from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives,send_mail #para el prototipo de enviar mail
from web.models import *
import hashlib,random

# Formato de mensaje para controlar correos duplicados en el registro
<<<<<<< HEAD
DOBLE_EMAIL = _(u"Este correo ya est&aacute; en uso. "u"Por favor utilice otro correo o inicie sesi&oacte;n")
=======
DOBLE_EMAIL = _(u"Este correo ya está en uso. "u"Por favor utilice otro correo o inicie sesión")
>>>>>>> origin/djbienve

# Formulario de registro del usuario.
class RegistrationForm(UserCreationForm):

<<<<<<< HEAD
    # Anadir al formulario un campo para el email, el captcha,
=======
    # Añadir al formulario un campo para el email, el captcha,
>>>>>>> origin/djbienve
    # y un checkbox para que el usuario acepte las condiciones de uso
    email = forms.EmailField(
        required = True
    )

<<<<<<< HEAD
    # Anadir el campo de Captcha
=======
    #Añadir el campo de Captcha
>>>>>>> origin/djbienve
    captcha = ReCaptchaField(
        label = 'Captcha'
    )

<<<<<<< HEAD
    # Checkbox para las condiciones de uso que el usuario debe aceptar
=======
    #Checkbox de licencia el cual el usuario debe aceptar
>>>>>>> origin/djbienve
    tos = forms.BooleanField(
        widget = forms.CheckboxInput,
        label = 'He le&iacute;do y acepto las condiciones de uso',
        error_messages={'required': 'Debes aceptar las condiciones de uso para continuar'}
    )

<<<<<<< HEAD
    # Funcion que se encargar de mirar en la base de datos
    # si existe el correo con el que intenta registrarse
    def clean_email(self):
            """
            Ya que Django solo nos ofrece el formulario de registro, pero no controla que el campo de correo electronico
            no sea doble, asi que con esta funcion cada vez que el usuario le da al boton de registrar verificamos que su correo
=======
    # Función que se encargar de mirar en la base de datos
    # si existe el correo con el que intenta registrarse
    def clean_email(self):
            """
            Ya que Django solo nos ofrece el formulario de registro, pero no controla que el campo de correo electrónico
            no sea doble, así que con esta funcion cada vez que el usuario le da al botón de registrar verificamos que su correo
>>>>>>> origin/djbienve
            no exista previamente en la base de datos.
            """
            if User.objects.filter(email__iexact=self.cleaned_data['email']): # Buscar en la base de datos el correo introducido
                raise forms.ValidationError(DOBLE_EMAIL)
            return self.cleaned_data['email']

<<<<<<< HEAD
    def clean_password2(self):
        password2 = super().clean_password2()

        # Expresion regular que comprueba si la password tiene al menos 8 caracteres,
        # entre los cuales debe haber como minimo un digito y una letra
        valid = re.match(r'^(?=.*[A-Za-zñÑ])(?=.*\d).{8,}$', password2)

        # Si la password no cumple estos requisitos, se eleva un error
        if not valid:
            raise forms.ValidationError(
                "La contraseña debe tener una longitud mínima de 8 caracteres y contener, al menos, una letra y un número",
                code='invalid_password',
            )

        return password2

    # Ampliar la funcion de guardado para que tambien guarde el email
=======


    # Ampliar la función de guardado para que también guarde el email
>>>>>>> origin/djbienve
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.is_active = False
            user.save()

            salt_str=str(random.random())
            salt = hashlib.sha1(salt_str.encode('utf_8')).hexdigest()[:5]
            salt_bytes = salt.encode('utf-8')
            correo_bytes=user.email.encode('utf-8')
            Activation_key = hashlib.sha1(salt_bytes+correo_bytes).hexdigest()
            val= validation(user=user,ash=Activation_key,creation_date=datetime.now().today())
            val.save();

            #crear el mail y enviarlo
            email_subject = 'Confirmacion de cuenta'
            email_body = "Hola %s, bienvenido a Roomate. Por favor, haz click \
            en el siguiente link para confirmar tu correo y disfrutar \
            plenamente de tu cuenta:<br> \
           <a href='http://127.0.0.1:8000/accounts/confirm/%s'>Confirmar cuenta</a>" % (user.username, Activation_key)
            subject, from_email = 'hello', 'no-reply@magnasis.com'
            text_content = 'Correo de confirmación.'
            #html_content = '<p>This is an <strong>important</strong> message.</p>'
            msg = EmailMultiAlternatives(email_subject, text_content, from_email, [user.email])
            msg.attach_alternative(email_body, "text/html")
            msg.send()
            #send_mail(email_subject, email_body, 'magnasis.grupo1@gmail.com', [user.email], fail_silently=False)
        return user

<<<<<<< HEAD

class ValidatedPasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        password2 = super().clean_new_password2()

        # Expresion regular que comprueba si la password tiene al menos 8 caracteres,
        # entre los cuales debe haber como minimo un digito y una letra
        valid = re.match(r'^(?=.*[A-Za-zñÑ])(?=.*\d).{8,}$', password2)

        # Si la password no cumple estos requisitos, se eleva un error
        if not valid:
            raise forms.ValidationError(
                "La contraseña debe tener una longitud mínima de 8 caracteres y contener, al menos, una letra y un número",
                code='invalid_password',
            )

        return password2


class ValidatedSetPasswordForm(SetPasswordForm):
    def clean_new_password2(self):
        password2 = super().clean_new_password2()

        # Expresion regular que comprueba si la password tiene al menos 8 caracteres,
        # entre los cuales debe haber como minimo un digito y una letra
        valid = re.match(r'^(?=.*[A-Za-zñÑ])(?=.*\d).{8,}$', password2)

        # Si la password no cumple estos requisitos, se eleva un error
        if not valid:
            raise forms.ValidationError(
                "La contraseña debe tener una longitud mínima de 8 caracteres y contener, al menos, una letra y un número",
                code='invalid_password',
            )

        return password2
=======
>>>>>>> origin/djbienve
