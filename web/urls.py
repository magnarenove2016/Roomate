from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.web_prueba),
    url(r'^register/$', views.register_new_user, name='register_new_user'),
    url(r'^recoverPassword/$', views.recover_password, name='recover_password'),
    #url(r'^recover-password/sent=(?P<mail>\w+)/$', views.recover_password_done, name='recover_password_done'),
    url(r'^recoverPassword/sendTo=(?P<mail>\w+[@]\w+[.]\w+)$', views.recover_password_done, name='recover_password_done'),

]
