from django import forms
from .models import Usuario, Casa

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('correo', 'contrasena','alias',)

class CasaForm(forms.ModelForm):

    class Meta:
        model = Casa
        fields = ('ciudad', 'num Habitaciones','numHabitacionesDisponibles',
         'descripcion', 'alquilerPorHabitaciones', 'precioAlquiler',
         'gastosComplementarios')
