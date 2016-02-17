from django.db import models
from django.utils import timezone
from web.views import arrendatario

# Create your models here.
class Usuario(models.Model):
    correo = models.CharField(max_length=200)
    contrasena = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    verificado = models.BooleanField(default=False)
    conversaciones = models.ForeignKey("Conversacion",null=True)
    arrendatario = models.BooleanField(default=False)

class Persona(models.Model):
    identificador = models.CharField(max_length=200)
    usuariosSimilares = models.ManyToManyField("Persona")

    def obtener_perfil(self):
        return Perfil.objects.get(persona=me)

class Perfil(models.Model):
    persona = models.ForeignKey("Persona")
    fechaNacimiento =models.DateTimeField()
    sexo = models.CharField(max_length=200)
    trabajadorEstudiante = models.BooleanField()
    campo = models.CharField(max_length=200)
    fumador = models.BooleanField()
    animalCompania = models.CharField(max_length=200)
    descripcion = models.TextField()
    zonaBuscada = models.CharField(max_length=200)
    inicioEstancia = models.DateTimeField()
    finEstancia = models.DateTimeField()
    instrumento = models.CharField(max_length=200)

    def obtener_tags_asociados(self):
        return TagValue.objects.get(perfil=me)

class TagValue(models.Model):
    perfil = models.ForeignKey("Perfil")
    tagName = models.ForeignKey("Tag")
    value = models.TextField()

class FotoPerfil(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
    perfil = models.ForeignKey("Perfil")

class Tag(models.Model):
    name = models.CharField(max_length=200)

class Conversacion(models.Model):
    emisor = models.ForeignKey("Usuario")

    def obtener_mensajes(self):
        return Mensaje.objects.get(conversacion=me)

class Mensaje(models.Model):
    conversacion = models.ForeignKey("Conversacion")
    emisor = models.ForeignKey("Usuario")
    mensaje = models.TextField()

class Log(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    evento = models.TextField()

class Casa(models.Model):
    dueno = models.ForeignKey("Persona")
    ciudad = models.CharField(max_length=200)
    numHabitaciones = models.IntegerField()
    numHabitacionesDisponibles = models.IntegerField()
    descripcion = models.TextField()
    alquilerPorHabitaciones = models.BooleanField()
    precioAlquiler = models.FloatField()
    gastosComplementarios = models.FloatField()

    def obtener_habitaciones(self):
        return Habitacion.objects.get(casa=me)

class FotoCasa(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
    casa = models.ForeignKey("Casa")

class Habitacion(models.Model):
    casa = models.ForeignKey("Casa")
    descripcion = models.TextField()

class FotoHabitacion(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
    habitacion = models.ForeignKey("Habitacion")
