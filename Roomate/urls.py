
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls), #url para administracion
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',name='auth_login'), #login provisto por Django
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}), #logout provisto por Django
    url(r'', include('web.urls')),  #todas las urls de web/urls.py
]
