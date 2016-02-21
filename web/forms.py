from django import forms
from .models import Usuario, Casa, Perfil

#formulario para la creacion de nuevos usuarios
class UsuarioForm(forms.ModelForm):
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
class completarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('fechaNacimiento', 'sexo', 'trabajadorEstudiante',
         'campo', 'fumador', 'animalCompania', 'descripcion', 'zonaBuscada',
          'inicioEstancia', 'finEstancia', 'instrumento')
