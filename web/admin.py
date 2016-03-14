from django.contrib import admin
from .models import *

#mapeamos todos nuestros objetos para poder administrarlos desde /admin
admin.site.register(FotoPerfil)
admin.site.register(Tag)
admin.site.register(Conversacion)
admin.site.register(Mensaje)
admin.site.register(Log)
admin.site.register(Casa)
admin.site.register(FotoCasa)
admin.site.register(Habitacion)
admin.site.register(FotoHabitacion)
admin.site.register(Profile)
