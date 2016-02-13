from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

# Create your views here.
def register_new_user(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            Usuario = form.save(commit=False)
            Usuario.save()
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
            #anadir usuario actual
            Casa.save()
            return redirect('/',)
    else:
        form = CasaForm()
    return render(request, 'web/add_house.html', {'form':form})
