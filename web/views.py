from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail #para el prototipo de enviar mail
from django.template import Context, RequestContext #para mostrar el mail en el .html

import hashlib, datetime, random

from .forms import *
from .models import *

'''
# Registrar nuevo usuario (Version Asier).
def register_new_user(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            Usuario = form.save(commit=False)
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+Usuario.correo).hexdigest()
            Usuario.activation_key= activation_key
            Usuario.verificado=False
            Usuario.save()

            email_subject = 'Confirmacion de cuenta'
            email_body = "Hola %s, bienvenido a Roomate. Por favor, haz click \
                en el siguiente link para confirmar tu correo y disfrutar \
                plenamente de tu cuenta: \
                http://localhost:8080/accounts/confirm/'%s'" % (Usuario.alias, activation_key)
            send_mail(email_subject, email_body, 'magnasis.grupo1@gmail.com',
                [Usuario.correo], fail_silently=False)

            return HttpResponseRedirect('/accounts/register_success')

            return redirect('/',)
    else:
        form = UsuarioForm()
    return render(request, 'web/register_new_user.html', {'form':form})
'''

# Registrar nuevo usuario (Version Jon).
def register_new_user(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            b = Usuario.objects.filter(correo=request.POST.get('correo'))#si existe un usuario con el mismo correo se guarda en b
            if b.count() == 0: #guarda el usuario sii no existe un usuario con el mismo correo
            	usuario = form.save(commit=False)
            	usuario.save()
            	context = {
            		'created':request.POST.get('correo')
            	}
            	return render_to_response('web/register_new_user.html', context, context_instance=RequestContext(request))
            else:
            	context = {
            		'exist':request.POST.get('correo')
            	}
            	return render_to_response('web/register_new_user.html', context, context_instance=RequestContext(request))
            return redirect('/',)
    else:
        form = UsuarioForm()
    return render(request, 'web/register_new_user.html', {'form':form})

@login_required
def add_house(request):
    if request.method == "POST":
        form = CasaForm(request.POST)
        if form.is_valid():
            Casa = form.save(commit=False)
            Casa.dueno=request.user
            Casa.save()
            return redirect('/',)
    else:
        form = CasaForm()
    return render(request, 'web/add_house.html', {'form':form})

'''def recover_password(request):
	if request.method == "POST":
		form = RecoverPasswordForm(request.POST)
		if form.is_valid():
			Usuario = form.save(commit=False)
			Usuario.save()
			user_mail = request.POST.get('correo', '')
			#send_mail('Password reset', 'Hello: please click the link below to reset your password.', 'admin@roomate.com', [user_mail], fail_silently=False)
			return redirect('recover_password_done',mail=user_mail)
	else:
		form = RecoverPasswordForm()
	return render(request, 'web/recover_password.html', {'form':form})'''

def recover_password(request):
	if request.method == "POST":
		user_mail = request.POST.get('correo')
		#send_mail('Password reset', 'Hello: please click the link below to reset your password.', 'admin@roomate.com', [user_mail], fail_silently=False)
		return redirect('recover_password_done',mail=user_mail)
	else:
		form = RecoverPasswordForm()
	return render(request, 'web/recover_password.html', {'form':form})

def recover_password_done(request, mail):
	context = {
		'mail': mail
	}
	#b = Usuario.objects.get(correo=mail)
	b = Usuario.objects.filter(correo=mail)
	if b.count() > 0:
		#send_mail('Password reset', 'Hello: please click the link below to reset your password.', 'admin@roomate.com', [mail], fail_silently=False)
		none
	return render_to_response('web/recover_password_done.html', context, context_instance=RequestContext(request))


def welcome(request):
    return render(request, 'web/welcome.html', {})
