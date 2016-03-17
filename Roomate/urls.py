from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from .forms import ValidatedSetPasswordForm, ValidatedPasswordChangeForm

urlpatterns = [

    url(r'^admin/', admin.site.urls), #url para administracion
    url(r'^accounts/login/$', views.auth_view,name='auth_login'), #login provisto por Django
    url(r'^accounts/logout/$', views.logout, name='logout'),  # cerrar sesion
    url(r'^accounts/invalid/$', views.invalid_login, name='invalid'), # mostrar el mensaje de error cuando el usuario falla los datos
    url(r'^database_backup/$', views.database_backup, name='database_backup'), # pagina para la gestion de backups
    url(r'^database_backup/trigger_backup/$', views.trigger_backup, name='trigger_backup'), # pagina para disparar una copia de seguridad d ela base de datos
    url(r'^accounts/user/delete/$', views.delete_user, name='delete_user'),
    url(r'^register/$', views.register_new_user, name='register_new_user'), #registrar a un nuevo usuario
    url(r'^register/success/$', views.user_created, name='register_success'), #mensaje que se muestra cuando se ha creado bien el nuevo usuario

    url(r'^accounts/password/reset/$', auth_views.password_reset,
        {'template_name': 'web/es/password_reset.html',
         'post_reset_redirect': 'password_reset_done'},
        name='password_reset'),

    url(r'^accounts/password/reset/done/$',
    auth_views.password_reset_done,
    {'template_name' : 'web/es/password_reset_done.html'},
    name='password_reset_done'),

    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'web/es/password_reset_confirm.html',
         'set_password_form': ValidatedSetPasswordForm},
        name='password_reset_confirm'),

    url(r'^accounts/password/reset/complete/$',
    auth_views.password_reset_complete,
    {'template_name' : 'web/es/password_reset_complete.html'},
    name='password_reset_complete'),

    url(r'^accounts/password/change/$',
    auth_views.password_change,
    {'template_name' : 'web/es/password_change.html',
     'password_change_form': ValidatedPasswordChangeForm,
     'post_change_redirect' : 'password_change_done'},
    name='password_change'),

    url(r'^accounts/password/change/done/$',
    auth_views.password_change_done,
    {'template_name' : 'web/es/password_change_done.html'},
    name='password_change_done'),

    url(r'', include('web.urls')), #todas las urls de web/urls.py
]

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )

