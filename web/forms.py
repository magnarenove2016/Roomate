from django import forms
from .models import Usuario
from web.models import Persona

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('correo', 'contrasena','alias',)
        
class ArrendatarioForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ('arrendatario')
        
class ArrendatarioForm(forms.ModelForm):
    
    class Meta:
        model = Perfil
        fields = ('fechaNacimiento', 'sexo', 'trabajadorEstudiante', 'fumador',
                  'animalCompania', 'descripcion', 'zona', 'inicioEstancia',
                   'finEstancia', 'instrumento')
