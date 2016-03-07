from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='main'),
    url(r'^undeveloped/$', views.undeveloped, name='undeveloped'),
    url(r'^search/$', views.get_location_search, name='get_location_search'),
    #url(r'^register/$', views.register_new_user, name='register_new_user'),
    url(r'^add_house/$', views.add_house, name='add_house'),
    url(r'^completar_perfil/$', views.edit_profile, name='completar_perfil'),
    #url(r'^completar_perfil/$', views.completar_perfil, name='completar_perfil'),
    #url(r'^accounts/confirm/(?P<activation_key>\w+)/$', views.confirmar_email, name='confirmar_email'),
	url(r'^recoverPassword/$', views.recover_password, name='recover_password'),
    #url(r'^recover-password/sent=(?P<mail>\w+)/$', views.recover_password_done, name='recover_password_done'),
    url(r'^recoverPassword/sendTo=(?P<mail>\w+[@]\w+[.]\w+)$', views.recover_password_done, name='recover_password_done'),

]
