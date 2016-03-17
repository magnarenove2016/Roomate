import math
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  # para contactar con el support
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext  # para mostrar el mail en el .html

from Roomate.views import castellano, euskera
from geopy.geocoders import Nominatim
from .forms import *
from .models import *

def filtros(sex,fumador,city):
    if sex == '':
        if fumador == False:
            if city == '':
                return Profile.objects.filter(ocupation='E',isSmoker=False).all()
            else:
                return Profile.objects.filter(ocupation='E',lookingIn=city,isSmoker=False).all()
        else:
            if city == '':
                return Profile.objects.filter(ocupation='E',isSmoker=True).all()
            else:
                return Profile.objects.filter(ocupation='E',lookingIn=city,isSmoker=True).all()
    else:
        if fumador == False:
            if city == '':
                return Profile.objects.filter(ocupation='E',isSmoker=False,gender=sex).all()
            else:
                return Profile.objects.filter(ocupation='E',lookingIn=city,isSmoker=False,gender=sex).all()
        else:
            if city == '':
                return Profile.objects.filter(ocupation='E',isSmoker=True,gender=sex).all()
            else:
                return Profile.objects.filter(ocupation='E',lookingIn=city,isSmoker=True,gender=sex).all()




#buscar compañeros de piso
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

    return render_to_response('web/'+request.session['lang']+'/ver_perfil_compa.html', {'fon':b[0].telephone,'mail':user[0].email})


# Registrar un arrendatario completando su perfil
@login_required
def edit_profile(request):
    # Comprobar si el usuario ya tiene un perfil creado
    try:
        profile = request.user.profile
    except:
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

        for file in request.FILES._itervalues():  # TODO: in development
            newFoto = FotoPerfil(foto=file)
            newFoto.perfil = profile
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

    return render(request, 'web/' + request.session['lang'] + '/edit_profile.html',
                  {'form': form, 'tag_forms': tag_forms})


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


# Anadir una casa (requiere login)
@login_required
def add_house(request):
    if request.method == "POST":
        # creamos form
        formcasa = CasaForm(request.POST, request.FILES)
        if formcasa.is_valid():
            # obtener datos y guardar perfil
            Casa = formcasa.save(commit=False)
            Casa.dueno = request.user
            Casa.save()
            for file in request.FILES._itervalues():
                newFoto = FotoCasa(foto=file)
                newFoto.casa = Casa
                newFoto.save()
            return redirect('main');
        else:
            return render(request, 'web/' + request.session['lang'] + '/add_house.html', {'formCasa': formcasa})
    else:
        # generamos form
        formcasa = CasaForm()
    return render(request, 'web/' + request.session['lang'] + '/add_house.html', {'formCasa': formcasa})


# pagina generica para funciones sin desarrollar
def undeveloped(request):
    return render(request, 'web/' + request.session['lang'] + '/undeveloped.html', {})


def change_language(request, language):
    if language == castellano:
        request.session['lang'] = castellano
    elif language == euskera:
        request.session['lang'] = euskera
    return redirect('main');


# pagina sobre los desarrolladores
def about_us(request):
    return render(request, 'web/' + request.session['lang'] + '/about_us.html', {})


def welcome(request):
    if 'lang' not in request.session:
        request.session['lang'] = castellano
    return render(request, 'web/' + request.session['lang'] + '/welcome.html', {})


# ----------------------------------- Funciones adicionales --------------------------------------------------

def getLocation(name):
    geolocator = Nominatim()
    localizacion = geolocator.geocode(name, exactly_one='False')
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
            return render(request, 'web/' + request.session['lang'] + '/error.html', {})
    else:
        # used url /search/ with no parameters
        return render(request, 'web/' + request.session['lang'] + '/error.html', {})
    return render_to_response('web/' + request.session['lang'] + '/search_result.html',
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
