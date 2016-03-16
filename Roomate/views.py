from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from datetime import datetime,timedelta
from . import forms
from web.models import *
<<<<<<< HEAD
from django.core import management
=======
>>>>>>> origin/djbienve


<<<<<<< HEAD

castellano = "es"
euskera = "eu"

# Comprobar si el usuario esta registrado
def auth_view(request):
    username = request.POST.get('username', '')  # Almacenamos el nombre de usuario
    password = request.POST.get('password', '')  # Almacenamos la password
    user = auth.authenticate(username=username, password=password)  # Iniciamos sesion con dichos datos
    if user is not None:  # Si el usuario y la password son validos
        auth.login(request, user)
        return redirect('main')  # Le redirigimos a la pagina de Inicio
    else:
        return redirect('invalid')  # Si no son validos, se redirige al usuario a una pagina de error


# Redirige al usuario a una pagina de error
=======
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
	if user is not None and user.is_active: # Si el usuario y la contraseña son válidos y esta activo
		auth.login(request, user)
		return redirect('main') # Le redirigimos a la página de Inicio
	else:
		return redirect('invalid') # Si no son válidos, se redirige al usuario a una página de error

# Redirige al usuario a una página de error
>>>>>>> origin/djbienve
def invalid_login(request):
    c = {}
    c.update(csrf(request))
    return redirect('main') #TODO: mostrar mensaje de error


# Cerrar sesion
def logout(request):
<<<<<<< HEAD
    auth.logout(request)
    c = {}
    c.update(csrf(request))
    return redirect('main')


# Registrar un nuevo usuario
def register_new_user(request):
    if request.method == "POST":  # Si el usuario le ha dado al boton de registrarse
        form = forms.RegistrationForm(request.POST);  # Generar un formulario con los datos introducidos por el usuario
        if form.is_valid():  # Comprobar si los datos son validos
            new_user = form.save(commit=True)  # Si son validos, los guardamos
            return redirect('register_success')  # Redireccion a una pagina que muestra un mensaje de usuario creado
    else:
        form = forms.RegistrationForm();  # Si el usuario esta entrando en la pagina de registro, le mostramos un formulario vacio
    return render(request, 'web/' + request.session['lang'] + '/register.html', {'form': form})


# Mostrar mensaje de usuario creado
def user_created(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('web/' + request.session['lang'] + '/register_complete.html', c)

=======
	auth.logout(request)
	c = {}
	c.update(csrf(request))
	return redirect('main')

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
>>>>>>> origin/djbienve

# Borrar un usuario
@login_required
def delete_user(request):
<<<<<<< HEAD
    if request.method == "POST":
        # Si el usuario ha introducido su nombre de usuario correctamente,
        # borrarlo de la base de datos
        username = request.POST.get('username', '')
        if (request.user.username == username):
            request.user.delete()
            auth.logout(request)
            return redirect('main')
        else:
            messages.error(request, 'El nombre de usuario introducido no coincide con tu nombre de usuario.')

    return render(request, 'web/' + request.session['lang'] + '/delete_user.html')
=======
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
>>>>>>> origin/djbienve

def cuentaactivada(request):
	#c = {}
	#c.update(csrf(request))
<<<<<<< HEAD
	return render_to_response('web/'+request.session['lang']+'/activacion_complete.html')
=======
	return render_to_response('web/'+idioma+'/activacion_complete.html')
>>>>>>> origin/djbienve


def error_activacion(request):
	#c = {}
	#c.update(csrf(request))
<<<<<<< HEAD
	return render_to_response('web/'+request.session['lang']+'/activacionerror.html')
=======
	return render_to_response('web/'+idioma+'/activacionerror.html')
>>>>>>> origin/djbienve


#metodo que va ha recibir el link de confirmacion

def activar_cuenta(request,codigo):
    try:
        u = validation.objects.get(ash=codigo)
    except:
        print('error al buscar la validacion')
        c = {}
        c.update(csrf(request))
<<<<<<< HEAD
        return render_to_response('web/'+request.session['lang']+'/activation_link_error.html',c)
=======
        return render_to_response('web/'+idioma+'/activation_link_error.html',c)
>>>>>>> origin/djbienve

    if u is None:
        c = {}
        c.update(csrf(request))
<<<<<<< HEAD
        return render_to_response('web/'+request.session['lang']+'/activacionerror.html',c)
=======
        return render_to_response('web/'+idioma+'/activacionerror.html',c)
>>>>>>> origin/djbienve
        #return redirect('ErrorActivacion')
    else:
        expired_date = u.creation_date - timedelta(days=2)
        print(expired_date)
        if expired_date > u.creation_date :
            u.user.delete()
            u.delete()
            c = {}
            c.update(csrf(request))
<<<<<<< HEAD
            return render_to_response('web/'+request.session['lang']+'/activation_link_error.html',c)
=======
            return render_to_response('web/'+idioma+'/activation_link_error.html',c)
>>>>>>> origin/djbienve
            #return Null
        u.user.is_active = True
        u.user.save()
        u.delete()
        c = {}
        c.update(csrf(request))
<<<<<<< HEAD
        return render_to_response('web/'+request.session['lang']+'/activacion_complete.html',c)
=======
        return render_to_response('web/'+idioma+'/activacion_complete.html',c)
>>>>>>> origin/djbienve
        #return redirect('cuentaActivada')



<<<<<<< HEAD

# Gestionar backups de la base de datos
@login_required
def database_backup(request):
    if request.user.is_superuser:
        if request.method == "POST":
            a=1
            # TODO: descargar backups
        else:
            return render(request, 'web/' + request.session['lang'] + '/database_backup.html', {})
    else:
        return redirect('main')


# Ejecutar copia d ela base de datos y ficheros
@login_required
def trigger_backup(request):
    if request.user.is_superuser:
        management.call_command('dbbackup')  # Copia de la base de datos
        management.call_command('mediabackup')  # Copia de Media
        return render(request, 'web/' + request.session['lang'] + '/database_backup_complete.html', {})
    else:
        return redirect('main')
=======
>>>>>>> origin/djbienve
