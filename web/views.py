from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

import hashlib, datetime, random

from .forms import *
from .models import *

# Create your views here.
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
