
from django.conf.urls import include, url
from django.contrib import admin
#from django.contrib.auth import views
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls), #url para administracion
    #url(r'^accounts/login/$', views.login,name='auth_login'), #login provisto por Django
    url(r'^accounts/login/$', views.auth_view,name='auth_login'), #login provisto por Django
    url(r'^register/$', views.register_new_user, name='register_new_user'), #registrar a un nuevo usuario
    url(r'^accounts/invalid/$', views.invalid_login, name='invalid'), #mostrar el mensaje de error cuando el usuario falla los datos
    url(r'^register/success/$', views.user_created, name='register_success'), #mensaje que se muestra cuando se creó bien el nuevo usuario
    #url(r'^completar_perfil/$', views.completar_perfil, name='completar_perfil'),
    #url(r'^accounts/logout/$', views.logout, {'next_page': '/'}), #logout provisto por Django
    url(r'^accounts/logout/$', views.logout, name='logout'), #cerrar sesión
    url(r'', include('web.urls')),  #todas las urls de web/urls.py
]
#nota: he intentado que esten aqui todos los link relacionados a la gestion de usuarios
