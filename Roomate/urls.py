
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
    url(r'^admin/', admin.site.urls), #url para administracion
    url(r'^accounts/login/$', views.login,name='auth_login'), #login provisto por Django
    url(r'^accounts/logout/$', views.logout, {'next_page': '/'}), #logout provisto por Django
    url(r'', include('web.urls')),  #todas las urls de web/urls.py
]
