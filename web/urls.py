from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^register/$', views.register_new_user, name='register_new_user'),
    url(r'^add_house/$', views.add_house, name='add_house'),
]
