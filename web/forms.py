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
# class completarPerfilForm(forms.ModelForm):
#     class Meta:
#         model = Perfil
#         fields = ('fechaNacimiento', 'sexo', 'trabajadorEstudiante',
#          'campo', 'fumador', 'animalCompania', 'descripcion', 'zonaBuscada',
#           'inicioEstancia', 'finEstancia', 'instrumento')


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


    # def __init__(self, *args, **kwargs):
    #     num_tags = kwargs.get('num_tags')
    #     #print(num_tags)
    #     super(ProfileForm, self).__init__() #extender el constructor original
    #
    #     if not (num_tags is None):
    #
    #         for i in range(num_tags): #iterar los campos de tag necesarios
    #             self.fields['tag_%s' % (i+1)] = forms.CharField(label='Etiqueta %s' % (i+1),required=False) #crear campo
    #
    # #TODO: codigo sin completar, quiero obtener todos lo tags
    # def get_tags(self):
    #     for name, value in self.cleaned_data.items():
    #         if name.startswith('tag_'):
    #             yield (self.fields[name].label, value)


class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ('text',)