from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.template.context_processors import csrf #para verificar la integridad de render_to_response (cookies) https://docs.djangoproject.com/en/1.8/ref/csrf/
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail #para el prototipo de enviar mail
from django.template import Context, RequestContext #para mostrar el mail en el .html
from geopy.geocoders import Nominatim
from django.db import IntegrityError
import hashlib, datetime, random, math

import re #for regex expresions

from .forms import *
from .models import *

castellano = "es"
euskera = "es"
idioma = "es"

# Registrar nuevo usuario (Version Jon).
def register_new_user(request):
    if request.method == "POST":
        #obtener formulario
        form = UsuarioForm(request.POST)
        if form.is_valid():
            #si existe un usuario con el mismo correo se guarda en b
            b = Usuario.objects.filter(correo=request.POST.get('correo'))

            #verificar seguridad del password
            if not re.match(r'^(?=.*\d)(?=.*[a-z]).{8,20}$', form.cleaned_data['contrasena'] ):
                context = {
                    'insecure':request.POST.get('correo')
                }
                context.update(csrf(request))
                return render_to_response('web/'+idioma+'/register_new_user.html', context)

            #verificar seguridad del password
            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", form.cleaned_data['correo'] ):
                context = {
                    'no_email':request.POST.get('correo')
                }
                con

                text.update(csrf(request))
                return render_to_response('web/'+idioma+'/register_new_user.html', context)

            #guarda el usuario sii no existe un usuario con el mismo correo
            elif b.count() == 0:
                usuario = form.save(commit=False)

                #creamos un User de tipo Django

                userDjango = User.objects.create_user(usuario.alias, usuario.correo, usuario.contrasena)
                #asignar el usuario recien creado a nuestro usuario
                usuario.user=userDjango

                #generar hash para la verificacion por mail y asignar
                salt_str=str(random.random())
                salt = hashlib.sha1(salt_str.encode('utf_8')).hexdigest()[:5]
                salt_bytes = salt.encode('utf-8')
                correo_bytes=usuario.correo.encode('utf-8')
                activation_key = hashlib.sha1(salt_bytes+correo_bytes).hexdigest()
                usuario.activation_key= activation_key

                #marcar como no verificado y guardar ambos
                usuario.verificado=False
                try:
                    usuario.save()
                except IntegrityError as e:
                    print("Correo existente")
                    context = {
                        'exist':request.POST.get('correo')
                    }
                    context.update(csrf(request))
                    return render_to_response('web/'+idioma+'/register_new_user.html', context)
                userDjango.save()

                #crear el mail y enviarlo
                email_subject = 'Confirmacion de cuenta'
                email_body = "Hola %s, bienvenido a Roomate. Por favor, haz click \
                en el siguiente link para confirmar tu correo y disfrutar \
                plenamente de tu cuenta: \
                http://localhost:8080/accounts/confirm/%s" % (usuario.alias, activation_key)
                send_mail(email_subject, email_body, 'magnasis.grupo1@gmail.com', [usuario.correo], fail_silently=False)

                #crear variable de contexto "created" (para el render de la HTML)
                context = {
                    'created':request.POST.get('correo')
                }

                #render
                context.update(csrf(request))
                return render_to_response('web/'+idioma+'/register_new_user.html', context)
            else: #existe un usuario con ese correo
                context = {
                    'exist':request.POST.get('correo')
                }
                context.update(csrf(request))
                return render_to_response('web/'+idioma+'/register_new_user.html', context)
            return redirect('/',)
    else:
        #generar formulario
        form = UsuarioForm()
    return render(request, 'web/'+idioma+'/register_new_user.html', {'form':form})



#Registrar un arrendatario completando su perfil (requiere login) Eficiente
@login_required
def edit_profile(request):
    # Comprobar si el usuario ya tiene un perfil creado
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user) #si no tiene perfil, se lo creamos

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid(): #comprobar los datos
            form.save()
            return redirect('main')
    else:
        form = ProfileForm(instance=profile)
    return render(request,'web/'+idioma+'/edit_profile.html', {'form': form})


#Anadir una casa (requiere login)
@login_required
def add_house(request):
    if request.method == "POST":

        #creamos form
        formcasa = CasaForm(request.POST)
        if formcasa.is_valid():
            #obtener datos y guardar perfil
            print("valid")
            Casa = formcasa.save(commit=False)
            Casa.dueno=request.user
            Casa.save()
            for f in request.FILES._itervalues():
                newFoto=FotoCasa(foto=f)
                newFoto.casa=Casa
                newFoto.save()
            return render_to_response('web/'+idioma+'/welcome.html', {})
    else:
        #generamos form
        formcasa = CasaForm()
    return render(request, 'web/'+idioma+'/add_house.html', {'formCasa': formcasa})


#pagina generica para funciones sin desarrollar
def undeveloped(request):
    return render(request, 'web/'+idioma+'/undeveloped.html', {})

#----------------------------------- Funciones experimentales sin documentar -----------------------------------------

'''
def recover_password(request):
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
	return render(request, 'web/'+idioma+'/recover_password.html', {'form':form})
'''

#funcion para la recuperacion de la password
def recover_password(request):
    if request.method == "POST":
        #obtenemos form
        user_mail = request.POST.get('correo')
        #TODO: envio de mail desactivado
        #send_mail('Password reset', 'Hello: please click the link below to reset your password.', 'admin@roomate.com', [user_mail], fail_silently=False)
        return redirect('recover_password_done', mail=user_mail)
    else:
        #creamos form
        form = RecoverPasswordForm()
    return render(request, 'web/'+idioma+'/recover_password.html', {'form' : form})

def recover_password_done(request, mail):
    #creamos variable de contexto "mail"
    context = {
        'mail': mail
    }
    #b = Usuario.objects.get(correo=mail) #es otra manera de conseguir los objetos deseados de la base de datos
    #obtenemos el mail
    b = Usuario.objects.filter(correo=mail)
    if b.count() > 0:
        send_mail('Password reset', 'Hello: please click the link below to reset your password.', 'magnasis.grupo1@gmail.com', [mail], fail_silently=False)
    return render_to_response('web/'+idioma+'/recover_password_done.html', context)

#----------------------------------- Funciones adicionales -----------------------------------------

def getLocation(name):
    geolocator = Nominatim()
    localizacion = geolocator.geocode(name, exactly_one='False')
    return localizacion

def welcome(request):
    return render(request, 'web/'+idioma+'/welcome.html',{})


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

def metersToKm( dist):
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
            return render(request, 'web/'+idioma+'/error.html', {})
    else:
        #used url /search/ with no parameters
        return render(request, 'web/'+idioma+'/error.html', {})
    return render_to_response('web/'+idioma+'/search_result.html', {'latitude': search.latitude, 'longitude': search.longitude, 'distance':dist}, context_instance=RequestContext(request))

def cambairIdioma(nuevo_idioma):
    idioma=nuevo_idioma
