from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^$', views.welcome, name='main'),
    url(r'^search/$', views.get_location_search, name='get_location_search'),
    url(r'^add_house/$', views.add_house, name='add_house'),
    url(r'^completar_perfil/$', views.edit_profile, name='completar_perfil'),
    url(r'^add_tag/$', views.add_tag, name='add_tag'),
    url(r'^delete_tag/(?P<texto_del_tag>.+)/$', views.delete_tag, name='delete_tag'),
    url(r'^undeveloped/$', views.undeveloped, name='undeveloped'),
]
