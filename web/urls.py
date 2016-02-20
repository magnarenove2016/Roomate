from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.web_prueba),
    url(r'^search/$', views.get_location_search, name='get_location_search'),
    url(r'^register/$', views.register_new_user, name='register_new_user'),
    url(r'^add_house/$', views.add_house, name='add_house'),
    #url(r'^accounts/confirmation/$', views.confirmar_email, name='confirmar_email'),
	url(r'^recoverPassword/$', views.recover_password, name='recover_password'),
    #url(r'^recover-password/sent=(?P<mail>\w+)/$', views.recover_password_done, name='recover_password_done'),
    url(r'^recoverPassword/sendTo=(?P<mail>\w+[@]\w+[.]\w+)$', views.recover_password_done, name='recover_password_done'),

]
