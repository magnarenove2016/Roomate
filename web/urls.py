from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^$', views.welcome, name='main'),
    url(r'^search/$', views.get_location_search, name='get_location_search'),
    url(r'^add_house/$', views.add_house, name='add_house'),
    url(r'^completar_perfil/$', views.edit_profile, name='completar_perfil'),
    url(r'^add_tag/$', views.add_tag, name='add_tag'),
    url(r'^delete_tag/(?P<texto_del_tag>.+)/$', views.delete_tag, name='delete_tag'),
    url(r'^change_language/(?P<language>.+)/$', views.change_language, name='change_language'),
    url(r'^undeveloped/$', views.undeveloped, name='undeveloped'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/done/$', views.contact_done, name='contact_done'),
    url(r'^legal/$', views.legal, name='legal'),
]
