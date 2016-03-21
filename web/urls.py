from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^$', views.welcome, name='main'),
    url(r'^search/$', views.get_location_search, name='get_location_search'),
    url(r'^add_house/$', views.add_house, name='add_house'),
    url(r'^completar_perfil/$', views.edit_profile, name='completar_perfil'),
    url(r'^delete_profile_image/(?P<path_image>.+)/$', views.delete_profile_image, name='delete_profile_image'),
    url(r'^add_tag/$', views.add_tag, name='add_tag'),
    url(r'^delete_tag/(?P<texto_del_tag>.+)/$', views.delete_tag, name='delete_tag'),
    url(r'^change_language/(?P<language>.+)/(?P<actual>/.*)/$', views.change_language, name='change_language'),
    url(r'^undeveloped/$', views.undeveloped, name='undeveloped'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^contact/done/$', views.contact_done, name='contact_done'),
    url(r'^legal/$', views.legal, name='legal'),
    url(r'^show_location/$', views.show_location, name='show_location'),
    url(r'^show_loc_edit/$', views.show_loc_edit, name='show_loc_edit'),
    url(r'^show_my_houses/$', views.show_my_houses, name='show_my_houses'),
    url(r'^edit_house/(?P<dir>.+)/(?P<ciudad>.+)/$', views.edit_house, name='edit_house'),
    url(r'^show_house/(?P<dir>.+)/(?P<ciudad>.+)/$', views.show_house, name='show_house'),
    url(r'^delete_house_image/(?P<path_image>.+)/$', views.delete_house_image, name='delete_house_image'),
    url(r'^busqueda/$', views.busquedaCompa, name='busqueda'),
    url(r'^usuario/(?P<nombre>.+)/$', views.mostrarcontacto, name='mostrarperfil'),
]
