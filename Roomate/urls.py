
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls), #url para administracion
    #url(r'^accounts/login/$', views.login,name='auth_login'), #login provisto por Django
    url(r'^accounts/login/$', views.auth_view,name='auth_login'), #login provisto por Django
    url(r'^register/$', views.register_new_user, name='register_new_user'), #registrar a un nuevo usuario
    url(r'^accounts/invalid/$', views.invalid_login, name='invalid'), #mostrar el mensaje de error cuando el usuario falla los datos
    url(r'^register/success/$', views.user_created, name='register_success'), #mensaje que se muestra cuando se ha creado bien el nuevo usuario
    #url(r'^completar_perfil/$', views.completar_perfil, name='completar_perfil'),
    #url(r'^accounts/logout/$', views.logout, {'next_page': '/'}), #logout provisto por Django
    url(r'^accounts/password/reset/$',auth_views.password_reset, {'template_name' : 'web/es/password_reset.html', 'post_reset_redirect' : 'password_reset_done'},
    name='password_reset'),

    url(r'^accounts/password/reset/done/$',
    auth_views.password_reset_done,
    {'template_name' : 'web/es/password_reset_done.html'},
    name='password_reset_done'),

    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    auth_views.password_reset_confirm,
    {'template_name' : 'web/es/password_reset_confirm.html'},
    name='password_reset_confirm'),

    url(r'^accounts/password/reset/complete/$',
    auth_views.password_reset_complete,
    {'template_name' : 'web/es/password_reset_complete.html'},
    name='password_reset_complete'),

    url(r'^accounts/password/change/$',
    auth_views.password_change,
    {'template_name' : 'web/es/password_change.html',
     'post_change_redirect' : 'password_change_done'},
    name='password_change'),

    url(r'^accounts/password/change/done/$',
    auth_views.password_change_done,
    {'template_name' : 'web/es/password_change_done.html'},
    name='password_change_done'),

    url(r'^accounts/user/delete/$', views.delete_user, name='delete_user'),

    url(r'^accounts/logout/$', views.logout, name='logout'), #cerrar sesion
    url(r'', include('web.urls')),  #todas las urls de web/urls.py
]
#nota: he intentado que esten aqui todos los link relacionados a la gestion de usuarios
