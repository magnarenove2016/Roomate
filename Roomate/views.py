from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from . import forms

idioma = "es"

# Iniciar sesión
def login(request):
	c = {}
	c.update(csrf(request)) # Actualizar la autenticidad de la redirección
	return render_to_response('accounts/login.html',c)

# Comprobar si el usuario está registrado
def auth_view(request):
	username = request.POST.get('username','') # Almacenamos el nombre de usuario
	password = request.POST.get('password','') # Almacenamos la contraseña
	user = auth.authenticate(username=username,password=password) # Iniciamos sesión con dichos datos
	if user is not None: # Si el usuario y la contraseña son válidos
		auth.login(request, user)
		return redirect('main') # Le redirigimos a la página de Inicio
	else:
		return redirect('invalid') # Si no son válidos, se redirige al usuario a una página de error

# Redirige al usuario a una página de error
def invalid_login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('web/'+idioma+'/invalid_login.html',c)

# Cerrar sesión
def logout(request):
	auth.logout(request)
	c = {}
	c.update(csrf(request))
	return render_to_response('web/'+idioma+'/welcome.html',c)

# Registrar un nuevo usuario
def register_new_user(request):
	if request.method == "POST": # Si el usuario le dio al boton de registrarse
		form = forms.RegistrationForm(request.POST); # Generar un formulario con los datos introducidos por el usuario
		if form.is_valid(): # Comprobar si son válidos dichos datos
			new_user = form.save(commit=True) # Si son validos, los guardamos
			return redirect('register_success') # Redirección a una página que muestra un mensaje de usuario creado
	else:
		form = forms.RegistrationForm(); # Si el usuario está entrando en la página de registro, le mostramos un formulario vacío
	return render(request, 'web/'+idioma+'/register.html', {'form': form})

# Mostrar mensaje de usuario creado
def user_created(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('web/'+idioma+'/registro_completado.html',c)

# Borrar un usuario
@login_required
def delete_user(request):
	if request.method == "POST":
		# Si el usuario ha introducido su nombre de usuario correctamente,
		# borrarlo de la base de datos
		username = request.POST.get('username','')
		if (request.user.username == username):
			request.user.delete()
			auth.logout(request)
			return redirect('main')
		else:
			messages.error(request, 'El nombre de usuario introducido no coincide con tu nombre de usuario.')

	return render(request, 'web/' + idioma + '/delete_user.html')
