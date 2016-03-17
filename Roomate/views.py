from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template.context_processors import csrf
from . import forms
from django.core import management
import logging
import logMessages

sessionLogger = logging.getLogger('web') ##Logging
dbLogger = logging.getLogger('database') ##Logging

castellano = "es"
euskera = "eu"

# Comprobar si el usuario esta registrado
def auth_view(request):
    username = request.POST.get('username', '')  # Almacenamos el nombre de usuario
    password = request.POST.get('password', '')  # Almacenamos la password
    user = auth.authenticate(username=username, password=password)  # Iniciamos sesion con dichos datos
    if user is not None:  # Si el usuario y la password son validos
        sessionLogger.info(logMessages.login_message+username+'\'')##Logging
        auth.login(request, user)
        return redirect('main')  # Le redirigimos a la pagina de Inicio
    else:
        return redirect('invalid')  # Si no son validos, se redirige al usuario a una pagina de error


# Redirige al usuario a una pagina de error
def invalid_login(request):
    c = {}
    c.update(csrf(request))
    return redirect('main') #TODO: mostrar mensaje de error


# Cerrar sesion
def logout(request):
    sessionLogger.info(logMessages.logout_message+request.user.username+'\'')##Logging
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
            dbLogger.info(logMessages.userCreated_message+request.POST.get('username','') +"\'")##Logging
            return redirect('register_success')  # Redireccion a una pagina que muestra un mensaje de usuario creado
    else:
        form = forms.RegistrationForm();  # Si el usuario esta entrando en la pagina de registro, le mostramos un formulario vacio
    return render(request, 'web/' + request.session['lang'] + '/register.html', {'form': form})


# Mostrar mensaje de usuario creado
def user_created(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('web/' + request.session['lang'] + '/register_complete.html', c)


# Borrar un usuario
@login_required
def delete_user(request):
    if request.method == "POST":
        # Si el usuario ha introducido su nombre de usuario correctamente,
        # borrarlo de la base de datos
        username = request.POST.get('username', '')
        if (request.user.username == username):
            request.user.delete()
            dbLogger.info(logMessages.userDeleted_message+username+"\'") ##Logging
            auth.logout(request)
            sessionLogger.info(logMessages.logout_message+username+'\'') ##Logging
            return redirect('main')
        else:
            messages.error(request, 'El nombre de usuario introducido no coincide con tu nombre de usuario.')

    return render(request, 'web/' + request.session['lang'] + '/delete_user.html')

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


# Ejecutar copia de la base de datos y ficheros
@login_required
def trigger_backup(request):
    if request.user.is_superuser:
        management.call_command('dbbackup')  # Copia de la base de
        dbLogger.info(logMessages.dbBackup_message+request.user.username+'\'')
        management.call_command('mediabackup')  # Copia de Media
        dbLogger.info(logMessages.mediaBackup_message+request.user.username+'\'')
        return render(request, 'web/' + request.session['lang'] + '/database_backup_complete.html', {})
    else:
        return redirect('main')

@login_required
def gest_logging(request):
    if request.user.is_superuser:
        log=open('roomate.log','r+').read()
        if request.method == "POST":
            return render(request, 'web/' + request.session['lang'] + '/gest_logging.html', {})
        else:
            return render(request, 'web/' + request.session['lang'] + '/gest_logging.html', {'text_log':log})
    else:
        return redirect('main')