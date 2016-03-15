from django.contrib import admin
from .models import *

# Mapeamos todos nuestros objetos para poder administrarlos desde /admin
admin.site.register(FotoPerfil)
admin.site.register(Tag)
admin.site.register(Casa)
admin.site.register(FotoCasa)
admin.site.register(Habitacion)
admin.site.register(FotoHabitacion)
admin.site.register(Profile)
