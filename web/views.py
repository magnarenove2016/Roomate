import logging
import math

import logMessages

from django.utils.encoding import smart_str
from Roomate.views import castellano, euskera
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  # para contactar con el support
from django.shortcuts import render, redirect
from django.template import RequestContext  # para mostrar el mail en el .html

from django.utils import translation
from django.utils.translation import ugettext as _
from geopy.geocoders import Nominatim
from .forms import *
from .models import *

#new imports
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from django.db import transaction, IntegrityError

import json
import urllib.request
import urllib.parse
from decimal import Decimal

sessionLogger = logging.getLogger('web') ##Logging
dbLogger = logging.getLogger('database') ##Logging

# Registrar un arrendatario completando su perfil
@login_required
def edit_profile(request):
    # Comprobar si el usuario ya tiene un perfil creado (y si no, crearselo)
    try:
        profile = request.user.profile
    except:
        profile = Profile(user=request.user)

    tags = Tag.objects.filter(perfil=profile) # obtener tags asociados al perfil

    if request.method == 'POST':
        formProfile = ProfileForm(request.POST, instance=profile, prefix='perfil')  # extraemos el profile del POST

        # Guardar los cambios realizados en los tags
        for i, tag in enumerate(tags):
            tagForm = TagForm(request.POST, instance=tag, prefix='tag_%s' % i)
            tagForm.perfil = profile
            if tagForm.is_valid():
                tagForm.save()  # TODO: comprobar si el tag ya existe?
                dbLogger.info(logMessages.tagCreated_message + request.user.username + '\'')  # Logging

        # Guardar las fotos subidas por el usuario
        for file in request.FILES._itervalues():
            newFoto = FotoPerfil(foto=file)
            newFoto.perfil = profile
            newFoto.save()
            dbLogger.info(logMessages.foPerAdded_message + request.user.username + '\'')  # Logging

        if formProfile.is_valid():  # comprobamos que el profile es valido
            formProfile.save()  # y lo guardamos
            dbLogger.info(logMessages.profileEdited_message + request.user.username + '\'')  # Logging
            messages.success(request, _("Los cambios han sido guardados!"))
            return redirect('completar_perfil')
        else:
            messages.error(request, _('No se han podido guardar todos los cambios, hay un error en el perfil.'))

    else:
        formProfile = ProfileForm(instance=profile, prefix='perfil')  # formulario con solo con los tags que ya tiene

    tag_forms = get_tag_forms(tags)

    images = FotoPerfil.objects.filter(perfil=profile)

    return render(request, 'web/' + request.session['lang'] + '/edit_profile.html',
                  {'form': formProfile, 'tag_forms': tag_forms, 'images': images})


# eliminar determinada imagen del usuario
@login_required
def delete_profile_image(request, path_image):
    fc=FotoPerfil.objects.filter(foto=path_image, perfil=request.user.profile)
    fc.all().delete()
    dbLogger.info(logMessages.foPerDeleted_message+request.user.username+'\'')##Logging
    return edit_profile(request) #


def get_tag_forms(tags):
    tag_forms = []
    for i, tag in enumerate(tags):
         # Anadir un campo al tag con un prefijo unico
         tag_forms.append(TagForm(instance=tag, prefix='tag_%s' % i))
    return tag_forms

# anadir tag al usuario
@login_required
def add_tag(request):
    try:  # obtenemos el perfil del usuario
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)  # si no tiene perfil, se lo creamos
        profile.save()
        dbLogger.info(logMessages.profileCreated_message+request.user.username+'\'')

    tag = Tag()

    tag.perfil = profile  # asignamos el perfil
    tag.text = "Etiqueta en blanco"  # y un texto generico
    tag.save()  # y lo guardamos
    dbLogger.info(logMessages.tagAdded_message+request.user.username+'\'')

    if(request.is_ajax()):
        tags = Tag.objects.filter(perfil=profile)
        tag_forms = get_tag_forms(tags)
        return render(request, 'web/es/tags.html', {'tag_forms' : tag_forms})
    else:
        return redirect('/completar_perfil/', )


# eliminar determinado tag del usuario
@login_required
def delete_tag(request, texto_del_tag):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)  # si no tiene perfil, se lo creamos
        profile.save()
        dbLogger.info(logMessages.profileCreated_message+request.user.username+'\'')

    tag = Tag.objects.filter(perfil=profile, text=texto_del_tag)  # obtenemos sus tags #TODO: buscamos el tag a eliminar
    tag[0].delete()

    dbLogger.info(logMessages.tagDeleted_message+request.user.username+'\'')
    return redirect('/completar_perfil/', )


#New
def geocode( address):
    address = urllib.parse.quote_plus(smart_str(address))
    maps_api_url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % address
    response = urllib.request.urlopen(maps_api_url)
    data = json.loads(response.read().decode('utf8'))

    if data['status'] == 'OK' and data != None:
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return Decimal(lat), Decimal(lng)
    else:
        return None, None
#end new

# Anadir una casa (requiere login)
@login_required
def add_house(request):
    if request.method == "POST":
        #creamos form
        formcasa = CasaForm(request.POST,request.FILES)
        if formcasa.is_valid():
            geolocator = Nominatim()
            #new ani multi-click
            try:
                with transaction.atomic():
                    #obtener datos y guardar perfil
                    Cas = formcasa.save(commit=False)
                    casa=Casa.objects.filter(direccion=Cas.direccion,ciudad=Cas.ciudad, dueno=request.user)
                    if casa.count() == 0:
                        Cas.dueno=request.user
                        #location = geolocator.geocode("Espana "+Cas.ciudad+" "+Cas.direccion)
                        #google geolocator
                        loc="Espana "+Cas.ciudad+" "+Cas.direccion.replace('/', ' ').replace('\\', ' ')
                        #print(loc)
                        Cas.latitude, Cas.longitude = geocode(address=loc)
                        if Cas.latitude != None and Cas.longitude != None:
                            Cas.save()
                            dbLogger.info(logMessages.casaCreated_message+request.user.username+'\'')##Logging
                            for f in request.FILES._itervalues():
                                newFoto=FotoCasa(foto=f)
                                newFoto.casa=Cas
                                newFoto.save()
                                dbLogger.info(logMessages.fotoAdded_message+request.user.username+'\'')##Logging

                            request.session['direccion'] = Cas.direccion
                            request.session['ciudad'] = Cas.ciudad
                            return redirect("/show_location/")
                        else:
                            return render(request, 'web/'+request.session['lang']+'/error_casa_no_encontrada.html', {})
                    else:
                        return render(request, 'web/'+request.session['lang']+'/error_casa.html', {})
            except IntegrityError:
                formcasa.addError('House exists')
            except ConnectionAbortedError:
                print("Connection closed")
        else:
            return render(request, 'web/'+request.session['lang']+'/add_house.html', {'formCasa': formcasa})
    else:
        #generamos form
        formcasa = CasaForm()
    return render(request, 'web/'+request.session['lang']+'/add_house.html', {'formCasa': formcasa})

#Anadir una casa (requiere login)

@login_required
def show_my_houses(request):
    return render(request, 'web/' + request.session['lang'] + '/view_house.html', {'casas': request.user.casas.all()})


def show_house(request, dir, ciudad):
    casa=Casa.objects.filter(direccion=dir,ciudad=ciudad).first()
    if casa is not None:
        return render(request, 'web/' + request.session['lang'] + '/show_house.html', {'casa': casa})
    else:
        return render(request, 'web/'+request.session['lang']+'/error_casa_no_encontrada.html', {})
#Anadir una casa (requiere login)

@login_required
def edit_house(request, dir, ciudad):
        casa = Casa.objects.filter(direccion=dir, ciudad=ciudad, dueno=request.user)
        if casa is not None:
            if request.method == "POST":
                casa=Casa.objects.filter(direccion=dir,ciudad=ciudad, dueno=request.user)
                #creamos form
                formcasa = CasaForm(request.POST,request.FILES, instance=casa.first())
                if formcasa.is_valid():
                    try:
                        with transaction.atomic():
                            #obtener datos y guardar perfil
                            Cas = formcasa.save(commit=False)
                            Cas.dueno=request.user
                            loc="Espana "+ciudad+" "+dir.replace('/', ' ').replace('\\', ' ')
                            Cas.latitude, Cas.longitude  = geocode(address=loc)
                            if Cas.latitude!= None and Cas.longitude!= None:
                                Cas.save()
                                #dbLogger.info(logMessages.casaEdited_message+request.user.username+'Ciudad: '+Cas.ciudad+'Direccion: '+Cas.direccion+'\'')##Logging
                                dbLogger.info(logMessages.casaCreated_message+request.user.username+'\'')##Logging
                                for f in request.FILES._itervalues():
                                    newFoto=FotoCasa(foto=f)
                                    newFoto.casa=Cas
                                    newFoto.save()
                                    #dbLogger.info(logMessages.fotoAdded_message+request.user.username+' de la casa:'+Cas.ciudad+' '+Cas.direccion+'\'')##Logging
                                    dbLogger.info(logMessages.fotoAdded_message+request.user.username+'\'')##Logging

                                request.session['direccion'] = Cas.direccion
                                request.session['ciudad'] = Cas.ciudad
                                return redirect("/show_location/")
                            else:
                                return render(request, 'web/'+request.session['lang']+'/error_casa_no_encontrada.html', {})
                    except IntegrityError:
                        formcasa.addError('House exists')
                    except ConnectionAbortedError:
                        print("Connection closed")
                else:
                    return render(request, 'web/'+request.session['lang']+'/add_house.html', {'formCasa': formcasa})
            else:
                #generamos form
                formcasa = CasaForm(instance=casa.first())
            return render(request, 'web/'+request.session['lang']+'/edit_house.html', {'formCasa': formcasa,'casa': casa.first()})
        else:
            return render(request, 'web/'+request.session['lang']+'/error_casa_no_encontrada.html', {})


"""" eliminar determinado tag del usuario"""
@login_required
def delete_house_image(request, path_image):
    fc=FotoCasa.objects.filter(foto=path_image, casa__dueno=request.user)
    cit=fc.first().casa.ciudad
    dir=fc.first().casa.direccion
    fc.all().delete()
    dbLogger.info(logMessages.foCasDeleted_message+request.user.username+'\'')##Logging
    return redirect("/edit_house/"+dir+"/"+cit+"/") #falta editar este y crear el boton que lo llame

#Ensenar localizacion de casa y confirmar (requiere login)
@login_required
def show_location(request):
    #creamos form
    casaDir=request.session.get('direccion')
    casaCi=request.session.get('ciudad')

    request.session.delete('direccion')
    request.session.delete('ciudad')

    casa=Casa.objects.filter(direccion=casaDir,ciudad=casaCi).all()
    if(request.method=="POST"):
        if 'accept' in request.POST:
            messages.success(request, _("La casa ha sido creada correctamente!"))
            return redirect('show_my_houses')
        else:
            #case that he clicks cancel
            for c in casa:
                for f in c.fotos.all():
                    f.delete()
                c.delete()
            #return one renderized view
            return redirect("/")
    else:
        return render(request, 'web/'+request.session['lang']+'/show_loc.html', {'lat':str(casa[0].latitude).replace(",", "."), 'long':str(casa[0].longitude).replace(",", ".")})

#Ensenar localizacion de casa y confirmar (requiere login)
@login_required
def show_loc_edit(request):
    #creamos form
    casaDir=request.session.get('direccion')
    casaCi=request.session.get('ciudad')

    request.session.delete('direccion')
    request.session.delete('ciudad')

    casa=Casa.objects.filter(direccion=casaDir,ciudad=casaCi).all()
    if(request.method=="POST"):
        if 'accept' in request.POST:
            messages.success(request, _("Los cambios han sido guardados!"))
            return redirect('show_my_houses')
        else:
            #case that he clicks cancel
            for c in casa:
                for f in c.fotos.all():
                    f.delete()
                c.delete()
            #return one renderized view
            return redirect("/")
    else:
        return render(request, 'web/'+request.session['lang']+'/show_loc_edit.html', {'lat':str(casa[0].latitude).replace(",", "."), 'long':str(casa[0].longitude).replace(",", ".")})


# pagina generica para funciones sin desarrollar
def undeveloped(request):
    return render(request, 'web/' + request.session['lang'] + '/undeveloped.html', {})


def change_language(request, language, actual):
    if language == castellano:
        request.session['lang'] = castellano
        request.session[translation.LANGUAGE_SESSION_KEY] = castellano
        translation.activate(castellano)
    elif language == euskera:
        request.session['lang'] = euskera
        request.session[translation.LANGUAGE_SESSION_KEY] = euskera
        translation.activate(euskera)
    return redirect(actual);


# pagina sobre los desarrolladores
def about_us(request):
    return render(request, 'web/' + request.session['lang'] + '/about_us.html', {})


def welcome(request):
    if 'lang' not in request.session:
        request.session['lang'] = castellano
        request.session[translation.LANGUAGE_SESSION_KEY] = castellano
    return render(request, 'web/' + request.session['lang'] + '/welcome.html', {})


# ----------------------------------- Funciones adicionales --------------------------------------------------

def getLocation(name):
    geolocator = Nominatim()
    localizacion = geolocator.geocode(name, exactly_one=False)
    return localizacion


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

        #loc = getLocation(search_str)
        #if loc is not None:

        lat, long= geocode(address=search_str)
        print (lat)
        if not lat==None or not long==None:
            #search = loc[0]
            casas=Casa.objects.filter(latitude__gte=float(lat)-0.05).filter(latitude__lte=float(lat)+0.05)
            if casas.count()!=0:
                searched=[]
                for casa in casas:
                    if distance_meters(float(lat), float(long),casa.latitude,casa.longitude)< 1500:
                        searched.append(casa)
                return render(request, 'web/' + request.session['lang'] + '/search_result.html', {'casas':searched})
            else:
                #No houses in that range
                return render(request, 'web/' + request.session['lang'] + '/info.html', {})
        else:
            # Loc not found
            return render(request, 'web/' + request.session['lang'] + '/info_no_loc.html', {})
    else:
        # used url /search/ with no parameters
        return render(request, 'web/' + request.session['lang'] + '/error.html', {})
    return render(request, 'web/' + request.session['lang'] + '/search_result.html',
                              {'latitude': search.latitude, 'longitude': search.longitude, 'distance': dist},
                              context_instance=RequestContext(request))


# para contactar con la web
def contact(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            # crear el mail y enviarlo
            email_subject = 'Soporte de RooMate, nuevo mensaje de ' + contact_email
            email_body = "Nuevo mensaje de %s desde RooMate.\n\nCorreo al que responder: %s\nMensaje:\n%s.\n\nUn cordial saludo de RooMate." % (
            contact_name, contact_email, form_content)
            send_mail(email_subject, email_body, 'no-reply@magnasis.com', ['support@magnasis.com'], fail_silently=False)
            return redirect('contact_done')
        else:
            return render(request, 'web/' + request.session['lang'] + '/contact.html', {'form': form,})
    return render(request, 'web/' + request.session['lang'] + '/contact.html', {
        'form': ContactForm,
    })


def contact_done(request):
    return render(request, 'web/' + request.session['lang'] + '/contact_submitted.html', {})

def legal(request):
    return render(request, 'web/'+request.session['lang'] + '/legal.html', {})

#funciones de bienve
def filtros(sex,fumador,city):
    if sex == '':
        if fumador == False:
            if city == '':
                return Profile.objects.all()
            else:
                return Profile.objects.filter(lookingIn=city,isSmoker=False).all()
        else:
            if city == '':
                return Profile.objects.filter(isSmoker=True).all()
            else:
                return Profile.objects.filter(lookingIn=city,isSmoker=True).all()
    else:
        if fumador == False:
            if city == '':
                return Profile.objects.filter(isSmoker=False,gender=sex).all()
            else:
                return Profile.objects.filter(lookingIn=city,isSmoker=False,gender=sex).all()
        else:
            if city == '':
                return Profile.objects.filter(isSmoker=True,gender=sex).all()
            else:
                return Profile.objects.filter(lookingIn=city,isSmoker=True,gender=sex).all()

#buscar companeros de piso
@login_required
def busquedaCompa(request):
    if request.method == "POST":
        #creamos form
        form = BusquedaForm(request.POST)
        if form.is_valid():
            sex=form.cleaned_data['gender']
            fumador = form.cleaned_data['isSmoker']
            city = form.cleaned_data['lookingIn']

            print('sex '+ sex+' fumador: '+str(fumador)+' ciudad: '+city)
            usuarios =filtros(sex,fumador,city)
            return render(request, 'web/'+ request.session['lang']+'/ver_resul_busqueda_compa.html', {'usuarios':usuarios})
    else:
        #generamos form
        form = BusquedaForm()
    return render(request, 'web/'+ request.session['lang']+'/buscar_compa.html', {'form':form})

#miestra el perfil del usuario por su nombre
def mostrarcontacto(request,nombre):

    user=User.objects.filter(username=nombre)
    #print(user[0].username + 'impreso222')
    b = Profile.objects.filter(user=user[0])
    form = ProfileForm2(instance=b[0])

    return render(request, 'web/'+request.session['lang']+'/ver_perfil_compa.html', {'fon':b[0].telephone,'mail':user[0].email})