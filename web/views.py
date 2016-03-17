import math

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
    print("add tag")

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
    print("delete tag")

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
    if request.session.get('refreshing_vcs',False)==False:
        request.session['refreshing_vcs']=True
        if request.method == "POST":
            #creamos form
            formcasa = CasaForm(request.POST,request.FILES)
            if formcasa.is_valid():
                #obtener datos y guardar perfil
                Cas = formcasa.save(commit=False)
                casa=Casa.objects.filter(direccion=Cas.direccion,ciudad=Cas.ciudad, dueno=request.user)
                if casa.count()==0:
                    Cas.dueno=request.user
                    loc = getLocation("España "+Cas.ciudad+" "+Cas.direccion)
                    if loc is not None:
                        location=loc[0]
                        Cas.latitude=location.latitude
                        Cas.longitude=location.longitude
                        Cas.save()
                        for f in request.FILES._itervalues():
                            newFoto=FotoCasa(foto=f)
                            newFoto.casa=Cas
                            newFoto.save()
                        print("added")

                        request.session['direccion'] = Cas.direccion
                        request.session['ciudad'] = Cas.ciudad
                        request.session['refreshing_vcs']=False
                        return redirect("/show_location/")
                    else:
                        request.session['refreshing_vcs']=False
                        return render(request, 'web/'+idioma+'/error_casa_no_encontrada.html', {})
                else:
                    request.session['refreshing_vcs']=False
                    return render(request, 'web/'+idioma+'/error_casa.html', {})
            else:
                request.session['refreshing_vcs']=False
                return render(request, 'web/'+idioma+'/add_house.html', {'formCasa': formcasa})
        else:
            #generamos form
            formcasa = CasaForm()
        request.session['refreshing_vcs']=False
        return render(request, 'web/'+idioma+'/add_house.html', {'formCasa': formcasa})

#Anadir una casa (requiere login)

@login_required
def show_my_houses(request):
    return render(request, 'web/' + idioma + '/view_house.html', {'casas': request.user.casas.all()})


def show_house(request, dir, ciudad):
    casa=Casa.objects.filter(direccion="dir").filter(ciudad=ciudad).first()
    if casa is not None:
        return render(request, 'web/' + idioma + '/view_house.html', {'casa': casa})
    else:
        return render(request, 'web/'+idioma+'/error_casa_no_encontrada.html', {})
#Anadir una casa (requiere login)

@login_required
def edit_house(request, dir, ciudad):
    if request.session.get('refreshing_vcs',False)==False:
        request.session['refreshing_vcs']=True
        casa = Casa.objects.filter(direccion=dir,ciudad=ciudad, dueno=request.user)
        if casa is not None:
            if request.method == "POST":
                casa=Casa.objects.filter(direccion=dir,ciudad=ciudad, dueno=request.user)
                #creamos form
                formcasa = CasaForm(request.POST,request.FILES, instance=casa.first())
                if formcasa.is_valid():
                    #obtener datos y guardar perfil
                    Cas = formcasa.save(commit=False)
                    Cas.dueno=request.user
                    loc = getLocation("España "+Cas.ciudad+" "+Cas.direccion)
                    if loc is not None:
                        location=loc[0]
                        Cas.latitude=location.latitude
                        Cas.longitude=location.longitude
                        Cas.save()
                        for f in request.FILES._itervalues():
                            newFoto=FotoCasa(foto=f)
                            newFoto.casa=Cas
                            newFoto.save()
                        print("added")

                        request.session['direccion'] = Cas.direccion
                        request.session['ciudad'] = Cas.ciudad
                        request.session['refreshing_vcs']=False
                        return redirect("/show_location/")
                    else:
                        request.session['refreshing_vcs']=False
                        return render(request, 'web/'+idioma+'/error_casa_no_encontrada.html', {})

                else:
                    request.session['refreshing_vcs']=False
                    return render(request, 'web/'+idioma+'/add_house.html', {'formCasa': formcasa})
            else:
                #generamos form
                formcasa = CasaForm(instance=casa.first())
            request.session['refreshing_vcs']=False
            return render(request, 'web/'+idioma+'/edit_house.html', {'formCasa': formcasa,'casa': casa.first()})


"""" eliminar determinado tag del usuario"""
@login_required
def delete_house_image(request, path_image):
    print("delete house_image")
    fc=FotoCasa.objects.filter(foto=path_image, casa__dueno=request.user)
    cit=fc.first().casa.ciudad
    dir=fc.first().casa.direccion
    fc.all().delete()
    return edit_house(request, dir, cit) #falta editar este y crear el boton que lo llame

#Enseñar localizacion de casa y confirmar (requiere login)
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
            return render(request, 'web/' + idioma + '/casa_creada.html', {})
            print("added")
        else:
            #case that he clicks cancel
            for c in casa:
                for f in c.fotos.all():
                    f.delete()
                c.delete()
            #return one renderized view
            return redirect("/")
    else:
        return render(request, 'web/'+idioma+'/show_loc.html', {'lat':str(casa[0].latitude).replace(",", "."), 'long':str(casa[0].longitude).replace(",", ".")})


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
        print(search_str)
        loc = getLocation(search_str)
        if loc is not None:
            search = loc[0]
            casas=Casa.objects.filter(latitude__gte=search.latitude-0.05).filter(latitude__lte=search.latitude+0.05)
            if casas.count()!=0:
                searched=[]
                for casa in casas:
                    if distance_meters(search.latitude, search.longitude,casa.latitude,casa.longitude)< 1500:
                        searched.append(casa)
                return render(request, 'web/' + idioma + '/search_result.html', {'casas':searched})
            else:
                #No houses in that range
                return render(request, 'web/' + idioma + '/info.html', {})
        else:
            # Loc not found
            return render(request, 'web/' + idioma + '/info_no_loc.html', {})
    else:
        # used url /search/ with no parameters
        return render(request, 'web/' + idioma + '/error.html', {})
    return render_to_response('web/' + idioma + '/search_result.html',
                              {'latitude': search.latitude, 'longitude': search.longitude, 'distance': dist},
                              context_instance=RequestContext(request))


def cambiarIdioma(nuevo_idioma):
    idioma = nuevo_idioma
