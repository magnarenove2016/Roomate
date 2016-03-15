import math

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext  # para mostrar el mail en el .html
from geopy.geocoders import Nominatim
from .forms import *
from .models import *

castellano = "es"
euskera = "es"
idioma = "es"


# Registrar un arrendatario completando su perfil (requiere login) Eficiente
@login_required
def edit_profile(request):
    # Comprobar si el usuario ya tiene un perfil creado
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)  # si no tiene perfil, se lo creamos

    tags = Tag.objects.filter(perfil=profile)  # obtener tags asociados al perfil

    if request.method == 'POST':
        formProfile = ProfileForm(request.POST, instance=profile, prefix='perfil')  # extraemos el profile del POST

        if formProfile.is_valid():  # comprobamos que el profile es valido
            formProfile.save()  # y lo guardamos

        i = 0
        for tag in tags:
            tagForm = TagForm(request.POST, instance=tag, prefix='tag_%s' % i)
            i = i + 1
            tagForm.perfil = profile
            if tagForm.is_valid():
                tagForm.save()  # TODO: comprobar si el tag ya existe?

        for file in request.FILES._itervalues(): # TODO: in development
            newFoto=FotoPerfil(foto=file)
            newFoto.perfil=profile
            newFoto.save()

        return redirect('completar_perfil')
    else:
        form = ProfileForm(instance=profile, prefix='perfil')  # formulario con solo con los tags que ya tiene
        tag_forms = []  # lista de formularios de tag vacia

        if tags:
            i = 0
            for tag in tags:  # iterar los campos de tag asociados al perfil
                tag_forms.append(
                    TagForm(instance=tag, prefix='tag_%s' % i))  # anadir un campo tipo tag con un prefijo unico
                i = i + 1

    return render(request, 'web/' + idioma + '/edit_profile.html', {'form': form, 'tag_forms': tag_forms})


# anadir tag al usuario
@login_required
def add_tag(request):

    try:  # obtenemos el perfil del usuario
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)  # si no tiene perfil, se lo creamos
        profile.save()

    tag = Tag()

    tag.perfil = profile  # asignamos el perfil
    tag.text = "Etiqueta en Blanco"  # y un texto generico
    tag.save()  # y lo guardamos
    return redirect('/completar_perfil/', )


# eliminar determinado tag del usuario
@login_required
def delete_tag(request, texto_del_tag):

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)  # si no tiene perfil, se lo creamos

        profile.save()

    tag = Tag.objects.filter(perfil=profile, text=texto_del_tag)  # obtenemos sus tags #TODO: buscamos el tag a eliminar

    tag.delete()
    return redirect('/completar_perfil/', )

#Anadir una casa (requiere login)
@login_required
def add_house(request):
    if request.method == "POST":
        #creamos form
        formcasa = CasaForm(request.POST,request.FILES)
        if formcasa.is_valid():
            #obtener datos y guardar perfil
            Casa = formcasa.save(commit=False)
            Casa.dueno=request.user
            Casa.save()
            for file in request.FILES._itervalues():
                newFoto=FotoCasa(foto=file)
                newFoto.casa=Casa
                newFoto.save()
            return redirect("/");
        else:
            return render(request, 'web/'+idioma+'/add_house.html', {'formCasa': formcasa})
    else:
        #generamos form
        formcasa = CasaForm()
    return render(request, 'web/'+idioma+'/add_house.html', {'formCasa': formcasa})


# pagina generica para funciones sin desarrollar
def undeveloped(request):
    return render(request, 'web/' + idioma + '/undeveloped.html', {})


# ----------------------------------- Funciones adicionales --------------------------------------------------

def getLocation(name):
    geolocator = Nominatim()
    localizacion = geolocator.geocode(name, exactly_one='False')
    return localizacion


def welcome(request):
    return render(request, 'web/' + idioma + '/welcome.html', {})


def distance_meters(lat1, long1, lat2, long2):
    # earth's radius in meters
    R = 6371000
    alfa1 = math.radians(lat1)
    alfa2 = math.radians(lat2)
    betaLat = math.radians(lat2 - lat1)
    betaLong = math.radians(long2 - long1)

    a = math.sin(betaLat / 2) * math.sin(betaLat / 2) + math.cos(alfa1) * math.cos(alfa2) * math.sin(
        betaLong / 2) * math.sin(betaLong / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist = R * c
    return dist


def metersToKm(dist):
    return round(dist / 1000, 2)


def get_location_search(request):
    if 's' in request.GET:
        search_str = request.GET['s']
        loc = getLocation(search_str)
        if loc is not None:
            search = loc[0]
            # Punto en donostia
            latitude = 43.3224219
            longitude = -1.9838888
            dist = distance_meters(search.latitude, search.longitude, latitude, longitude)
            dist = metersToKm(dist)
        else:
            # Nothing found
            return render(request, 'web/' + idioma + '/error.html', {})
    else:
        # used url /search/ with no parameters
        return render(request, 'web/' + idioma + '/error.html', {})
    return render_to_response('web/' + idioma + '/search_result.html',
                              {'latitude': search.latitude, 'longitude': search.longitude, 'distance': dist},
                              context_instance=RequestContext(request))


def cambiarIdioma(nuevo_idioma):
    idioma = nuevo_idioma
