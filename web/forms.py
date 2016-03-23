from datetime import datetime
from django import forms
from django.forms.widgets import SelectDateWidget
from django.utils.translation import ugettext as _
from html import unescape

from .models import Casa, Profile, Tag,Busqueda


# formulario para la creacion de casas
class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = ('ciudad','direccion', 'numHabitaciones', 'numHabitacionesDisponibles',
                  'descripcion', 'alquilerPorHabitaciones', 'precioAlquiler',
                  'gastosComplementarios',)

    # Asignar los placeholder adecuados a cada campo
    def __init__(self, *args, **kwargs):
        super(CasaForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'].widget.attrs.update({'placeholder': _('Ciudad')})
        self.fields['direccion'].widget.attrs.update({'placeholder': unescape(_('Descripci&oacute;n'))})
        self.fields['numHabitaciones'].widget.attrs.update({'placeholder': unescape(_('N&uacute;mero de habitaciones'))})
        self.fields['numHabitacionesDisponibles'].widget.attrs.update({'placeholder': unescape(_('N&uacute;mero de habitaciones disponibles'))})
        self.fields['descripcion'].widget.attrs.update({'placeholder': unescape(_('Descripci&oacute;n'))})
        self.fields['precioAlquiler'].widget.attrs.update({'placeholder': _('Precio del alquiler (en euros)')})
        self.fields['gastosComplementarios'].widget.attrs.update({'placeholder': _('Gastos complementarios (en euros)')})

# formulario para completar el perfil de arrendatario
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('firstName', 'lastName', 'birthdate', 'telephone', 'gender',
                  'ocupation', 'pet', 'iniEstancia', 'finEstancia', 'Instrument', 'description', 'lookingIn',
                  'isSmoker')
        widgets = {
            'birthdate': SelectDateWidget(years=range(datetime.now().year, 1800, -1)),
            'iniEstancia': SelectDateWidget(years=range(datetime.now().year, datetime.now().year + 5, 1)),
            # generar 5 years mas desde el year actual
            'finEstancia': SelectDateWidget(years=range(datetime.now().year, datetime.now().year + 5, 1)),
            # generar 5 years mas desde el year actual
        }

    # Asignar los placeholder adecuados a cada campo
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs.update({'placeholder': _('Nombre')})
        self.fields['lastName'].widget.attrs.update({'placeholder': _('Apellidos')})
        self.fields['telephone'].widget.attrs.update({'placeholder': unescape(_('N&uacute;mero de tel&eacute;fono'))})
        self.fields['Instrument'].widget.attrs.update({'placeholder': _('Instrumento')})
        self.fields['description'].widget.attrs.update({'placeholder': unescape(_('Una breve descripci&oacute;n sobre ti'))})
        self.fields['lookingIn'].widget.attrs.update({'placeholder': _('Ciudad / zona en la que buscas piso')})


class ConfirmationForm(forms.Form):
     myBool = forms.BooleanField(
        required=False,
        initial=False
     )


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
    # def __init__(self, *args, **kwargs):
    #     super(ContactForm, self).__init__(*args, **kwargs)
    #     self.fields['contact_name'].label = "Your name:"
    #     self.fields['contact_email'].label = "Your email:"
    #     self.fields['content'].label = "What do you want to say?"

#formulario para Buscar companero
class BusquedaForm(forms.ModelForm):
    class Meta:
        model = Busqueda
        fields = ('gender','isSmoker','lookingIn')

#formulario de visualizacion parcial de los datos de la persona
class ProfileForm2(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('firstName', 'lastName','telephone', 'gender',
        'ocupation', 'pet','Instrument', 'description', 'lookingIn', 'isSmoker')

