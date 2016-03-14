from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from . import forms

idioma = "es"


# Iniciar sesion
def login(request):
	c = {}
	c.update(csrf(request)) #actualizar la autenticidad de la redireccion
	return render_to_response('accounts/login.html',c)

# Comprobar si el usuario estaS registrado
def auth_view(request):
	username = request.POST.get('username','') #Almacenamos el nombre de usuario
	password = request.POST.get('password','') #Almacenamos la password
	user = auth.authenticate(username=username,password=password) # Iniciamos sesion con dichos datos
	if user is not None: #Si el usuario y la password son validos
		auth.login(request, user)
		return redirect('main') # Le redirigimos a la pagina de Inicio
	else:
		return redirect('invalid') # Si no son validos, se redirige al usuario a una pagina de error

#Redirige al usuario a una pagina de error
def invalid_login(request):
	c = {}
	c.update(csrf(request))
	return redirect('main')

# Cerrar sesion
def logout(request):
	auth.logout(request)
	c = {}
	c.update(csrf(request))
	return redirect('main')

# Registrar un nuevo usuario
def register_new_user(request):
	if request.method == "POST": # Si el usuario le ha dado al boton de registrarse
		form = forms.RegistrationForm(request.POST); # Generar un formulario con los datos introducidos por el usuario
		if form.is_valid(): # Comprobar si los datos son validos
			new_user = form.save(commit=True) # Si son validos, los guardamos
			return redirect('register_success') # Redireccion a una pagina que muestra un mensaje de usuario creado
	else:
		form = forms.RegistrationForm(); #Si el usuario esta entrando en la pagina de registro, le mostramos un formulario vacio
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
