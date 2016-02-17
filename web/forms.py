from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('correo', 'contrasena','alias',)

class RecoverPasswordForm(forms.ModelForm):

	class Meta:
		model = Usuario
		fields = ('correo',)
