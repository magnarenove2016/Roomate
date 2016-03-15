from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Usuario, Casa, Perfil,Profile, Tag
from captcha.fields import ReCaptchaField
from datetime import datetime

#formulario para la creacion de nuevos usuarios
class UsuarioForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Usuario
        fields = ('correo', 'contrasena','alias',)

#formulario para la creacion de casas
class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = ('ciudad', 'numHabitaciones','numHabitacionesDisponibles',
         'descripcion', 'alquilerPorHabitaciones', 'precioAlquiler',
         'gastosComplementarios')

#formulario para la recuperacion de contrasenas
class RecoverPasswordForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = ('correo',)

#formulario para completar el perfil de arrendatario
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('firstName', 'lastName','birthdate','telephone', 'gender',
        'ocupation', 'pet','iniEstancia','finEstancia','Instrument', 'description', 'lookingIn', 'isSmoker')
        widgets = {
            'birthdate': SelectDateWidget(years = range(datetime.now().year, 1800, -1)),
            'iniEstancia': SelectDateWidget(years = range(datetime.now().year, datetime.now().year + 5, 1)),#generar 5 years mas desde el year actual
            'finEstancia': SelectDateWidget(years = range(datetime.now().year, datetime.now().year + 5, 1)), #generar 5 years mas desde el year actual
        }

class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ('text',)

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
    # lo que aparecera en el html de contacto, los nombres
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"