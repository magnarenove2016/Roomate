from django.db import models
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):
    correo = models.CharField(max_length=200)
    contrasena = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    conversaciones = models.ForeignKey("Conversacion",null=True)

class Persona(models.Model):
    perfil = models.ForeignKey("Perfil")
    identificador = models.CharField(max_length=200)
    usuariosSimilares = models.ManyToManyField("Persona")

class Perfil(models.Model):
    fechaNacimiento =models.DateTimeField(default=timezone.now)
    sexo = models.CharField(max_length=200)
    trabajadorEstudiante = models.BooleanField()
    campo = models.CharField(max_length=200)
    fumador = models.BooleanField()
    animalCompania = models.CharField(max_length=200)
    descripcion = models.TextField()
    zonaBuscada = models.CharField(max_length=200)
    inicioEstancia = models.DateTimeField(default=timezone.now)
    finEstancia = models.DateTimeField(default=timezone.now)
    instrumento = models.CharField(max_length=200)

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

class FotoCasa(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
    casa = models.ForeignKey("Casa")

class Habitacion(models.Model):
    descripcion = models.TextField()
    casa = models.ForeignKey("Casa")

class FotoHabitacion(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
    habitacion = models.ForeignKey("Habitacion")
