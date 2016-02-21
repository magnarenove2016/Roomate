from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template.context_processors import csrf #para verificar la integridad de render_to_response (cookies) https://docs.djangoproject.com/en/1.8/ref/csrf/
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail #para el prototipo de enviar mail
from django.template import Context, RequestContext #para mostrar el mail en el .html
from geopy.geocoders import Nominatim

import hashlib, datetime, random, math

import re #for regex expresions

from .forms import *
from .models import *

# Registrar nuevo usuario (Version Jon).
def register_new_user(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            b = Usuario.objects.filter(correo=request.POST.get('correo'))#si existe un usuario con el mismo correo se guarda en b
            if not re.match(r'^(?=.*\d)(?=.*[a-z]).{8,20}$', form.cleaned_data['contrasena'] ): #verificar seguridad del password
                context = {
                    'insecure':request.POST.get('correo')
                }
                context.update(csrf(request))
                return render_to_response('web/register_new_user.html', context)
            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", form.cleaned_data['correo'] ): #verificar seguridad del password
                context = {
                    'no_email':request.POST.get('correo')
                }
                context.update(csrf(request))
                return render_to_response('web/register_new_user.html', context)
            elif b.count() == 0: #guarda el usuario sii no existe un usuario con el mismo correo
                usuario = form.save(commit=False)
                userDjango = User.objects.create_user(usuario.alias, usuario.correo, usuario.contrasena)
                usuario.user=userDjango
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                activation_key = hashlib.sha1(salt+usuario.correo).hexdigest()
                usuario.activation_key= activation_key
                usuario.verificado=False
                usuario.save()
                userDjango.save()


                email_subject = 'Confirmacion de cuenta'
                email_body = "Hola %s, bienvenido a Roomate. Por favor, haz click \
                en el siguiente link para confirmar tu correo y disfrutar \
                plenamente de tu cuenta: \
                http://localhost:8080/accounts/confirm/%s" % (usuario.alias, activation_key)
                send_mail(email_subject, email_body, 'magnasis.grupo1@gmail.com',
                    [usuario.correo], fail_silently=False)

                context = {
                    'created':request.POST.get('correo')
                }
                context.update(csrf(request))
                return render_to_response('web/register_new_user.html', context)
            else: #existe un usuario con ese correo
                context = {
                    'exist':request.POST.get('correo')
                }
                context.update(csrf(request))
                return render_to_response('web/register_new_user.html', context)
            return redirect('/',)
    else:
        form = UsuarioForm()
    return render(request, 'web/register_new_user.html', {'form':form})

#Registrar un arrendatario completando su perfil
@login_required
def completar_perfil(request):
    if request.method == "POST":
        form = completarPerfilForm(request.POST)
        if form.is_valid():
            Perfil = completarPerfilForm(request.POST)
            Perfil.persona=request.user
            Perfil.save()
            return redirect('/',)
    else:
        form = completarPerfilForm()
    return render(request, 'web/completar_perfil.html', {'form':form})

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
    #b = Usuario.objects.get(correo=mail) #es otra manera de conseguir los objetos deseados de la base de datos
    b = Usuario.objects.filter(correo=mail)
    if b.count() > 0:
        send_mail('Password reset', 'Hello: please click the link below to reset your password.', 'magnasis.grupo1@gmail.com', [mail], fail_silently=False)
        #none
    #return render_to_response('web/recover_password_done.html', context, context_instance=RequestContext(request))
    return render_to_response('web/recover_password_done.html', context)

def getLocation(name):
    geolocator = Nominatim()
    localizacion = geolocator.geocode(name, exactly_one='False')
    return localizacion

def welcome(request):
    return render(request, 'web/welcome.html', {})

def distance_meters(lat1, long1, lat2, long2):
    #earth's radius in meters
    R=6371000
    alfa1=math.radians(lat1)
    alfa2=math.radians(lat2)
    betaLat=math.radians(lat2-lat1)
    betaLong=math.radians(long2-long1)

    a=math.sin(betaLat/2) * math.sin(betaLat/2) + math.cos(alfa1) * math.cos(alfa2) * math.sin(betaLong/2)*math.sin(betaLong/2)

    c=2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist=R*c
    return dist

def metersToKm(dist):
    return round(dist/1000,2)


def get_location_search(request):
    if 's' in request.GET:
        search_str=request.GET['s']
        print(search_str)
        loc=getLocation(search_str)
        if loc is not None:
            search=loc[0]
            print (search.latitude)
            #Punto en donostia
            latitude=43.3224219
            longitude=-1.9838888
            dist=distance_meters(search.latitude, search.longitude, latitude, longitude)
            dist=metersToKm(dist)
        else:
            #Nothing found
            return render(request, 'web/error.html', {})
    else:
        #used url /search/ with no parameters
        return render(request, 'web/error.html', {})
    return render_to_response('web/search_result.html',{'latitude': search.latitude, 'longitude': search.longitude,'distance':dist},context_instance=RequestContext(request))


def undeveloped(request):
    return render(request, 'web/undeveloped.html', {})
