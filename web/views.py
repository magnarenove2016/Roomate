from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import UsuarioForm
from .models import Usuario

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
    
def web_prueba(request):
    return render(request, 'index.html', {})
