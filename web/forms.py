from datetime import datetime

from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Casa, Profile, Tag

#formulario para la creacion de casas
class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = ('ciudad', 'numHabitaciones','numHabitacionesDisponibles',
         'descripcion', 'alquilerPorHabitaciones', 'precioAlquiler',
         'gastosComplementarios')

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