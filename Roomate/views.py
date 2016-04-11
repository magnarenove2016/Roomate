import logging
from datetime import timedelta
import logMessages
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core import management
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import resolve
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.translation import ugettext as _
from web.models import validation
from html import unescape
from . import forms

sessionLogger = logging.getLogger('web') ##Logging
dbLogger = logging.getLogger('database') ##Logging

castellano = "es"
euskera = "eu"

# Comprobar si el usuario esta registrado
def auth_view(request):
    username = request.POST.get('username', '')  # Almacenamos el nombre de usuario
    password = request.POST.get('password', '')  # Almacenamos la password
    user = auth.authenticate(username=username, password=password)  # Iniciamos sesion con dichos datos
    if user is not None and user.is_active:  # Si el usuario y la password son validos
        sessionLogger.info(logMessages.login_message+username+'\'')##Logging
        auth.login(request, user)
        return redirect('main')  # Le redirigimos a la pagina de Inicio
    elif user is not None:
        messages.error(request, unescape(_("La cuenta con la que est&aacute;s intentando acceder no est&aacute; activa.")))
    else:
        messages.error(request, _("Los datos introducidos son incorrectos, vuelve a intentarlo."))
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
            current_site = get_current_site(request)
            new_user = form.save(commit=True)  # Si son validos, los guardamos
            enviarCorreosActivation(new_user,current_site.domain)
            dbLogger.info(logMessages.userCreated_message+request.POST.get('username','') +"\'")##Logging
            return redirect('register_success')  # Redireccion a una pagina que muestra un mensaje de usuario creado
    else:
        form = forms.RegistrationForm();  # Si el usuario esta entrando en la pagina de registro, le mostramos un formulario vacio
    return render(request, 'web/' + request.session['lang'] + '/register.html', {'form': form})

def enviarCorreosActivation(user,dir):
    email_subject = 'Confirmación de cuenta en RooMate'
    usr = validation.objects.filter(user=user).all()
    email_body = "Hola %s, <br> ¡Te damos la bienvenida a RooMate! <br><br> \
    Gracias por haber elegido nuestra página web. <br><br> \
    Estás a un simple clic de comenzar a disfrutar de las búsquedas de compañeros que estabas deseando. <br> \
    También podrás disfrutar de los sencillos métodos de alquiler que te ofrecemos. <br><br>  \
    Ya solo necesitas activar tu cuenta para poder aprovechar todos tus privilegios: <br> \
    <a href='http://%s/accounts/confirm/%s'>Haz clic aquí para activar tu cuenta</a> <br> <br> \
    ¡Gracias por confiar en nosotros! <br><br> \
    Atentamente, <br> El equipo de RooMate." % (user.username,dir,usr[0].ash)
    subject, from_email = 'hello', 'no-reply@magnasis.com'
    text_content = 'Correo de confirmaci&oacute;n.'
    msg = EmailMultiAlternatives(email_subject, text_content, from_email, [user.email])
    msg.attach_alternative(email_body, "text/html")
    msg.send()

# Mostrar mensaje de usuario creado
def user_created(request):
    c = {}
    c.update(csrf(request))
    return render(request,'web/' + request.session['lang'] + '/register_complete.html', c)


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
            messages.error(request, _('El nombre de usuario introducido no coincide con tu nombre de usuario.'))

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

#simplemente te hace una redireccion a una pagina que te muestra el mensaje de cuenta activada
def cuentaactivada(request):
    return render(request,'web/'+request.session['lang']+'/activacion_complete.html')

#mostrar el mensaje de error de activacion de cuenta
def error_activacion(request):
    return render(request,'web/'+request.session['lang']+'/activacionerror.html')

def activar_cuenta(request,codigo):
    try:
        u = validation.objects.get(ash=codigo)
    except:
        print('error al buscar la validacion')
        c = {}
        c.update(csrf(request))
        return render(request,'web/'+request.session['lang']+'/activation_link_error.html',c)

    if u is None:
        c = {}
        c.update(csrf(request))
        return render(request,'web/'+request.session['lang']+'/activacionerror.html',c)

    else:
        expired_date = u.creation_date - timedelta(days=2)
        print(expired_date)
        if expired_date > u.creation_date :
            u.user.delete()
            u.delete()
            c = {}
            c.update(csrf(request))
            return render(request,'web/'+request.session['lang']+'/activation_link_error.html',c)

        u.user.is_active = True
        u.user.save()
        u.delete()
        c = {}
        c.update(csrf(request))
        return render(request,'web/'+request.session['lang']+'/activacion_complete.html',c)

@login_required
def gest_logging(request,log_file):
    if request.user.is_superuser:
        if (log_file=='1'):
            log=open('roomate.log','r+').read()
            return render(request, 'web/' + request.session['lang'] + '/gest_logging.html', {'text_log':log})
        elif (log_file=='2'):
            log=open('session.log','r+').read()
            return render(request, 'web/' + request.session['lang'] + '/gest_logging.html', {'text_log':log})
        elif (log_file=='3'):
            log=open('dbAccess.log','r+').read()
            return render(request, 'web/' + request.session['lang'] + '/gest_logging.html', {'text_log':log})
        else:
            return render(request, 'web/' + request.session['lang'] + '/gest_logging.html', {})
    else:
        return redirect('main')
