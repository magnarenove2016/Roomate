from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail #para el prototipo de enviar mail
from django.template import Context, RequestContext #para mostrar el mail en el .html

from .forms import UsuarioForm
from .forms import RecoverPasswordForm
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
	return render_to_response('web/recover_password_done.html', context, context_instance=RequestContext(request))