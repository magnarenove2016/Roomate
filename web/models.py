from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from time import time


# Create your models here.
class Usuario(models.Model):
    # Campo asociado al usuario gestionado por django.
    user = models.OneToOneField(User,related_name='usuario')
    correo = models.CharField(max_length=200,unique=True)
    contrasena = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    activation_key = models.CharField(max_length=40)
    verificado = models.BooleanField(default=False)
    def cambiar_contrasena(self, x):
        self.contrasena = x
    def cambiar_alias(self, x):
        self.alias = x
    def cambiar_correo(self, x):
        self.correo = x


class Persona(models.Model):
    identificador = models.CharField(max_length=200)
    usuario=models.OneToOneField(
        Usuario,related_name='persona',
        on_delete=models.CASCADE,
        null=True, blank=True
    )



    def eliminar_perfil(self):
        b = self.perfil
        b.delete()


class GrupoUsuariosSimilares(models.Model):
    persona=models.ManyToManyField(Persona)
    desc=models.CharField(max_length=200)


class Perfil(models.Model):
    persona=models.OneToOneField(
        Persona,related_name='perfil',
        on_delete=models.CASCADE,
        primary_key=True
    )
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

    def cambiar_fechaNacimiento(self, x):
        self.fechaNacimiento = x

    def cambiar_sexo(self, x):
        self.sexo = x

    def cambiar_trabajadorEstudiante(self, x):
        self.trabajadorEstudiante = x

    def cambiar_campo(self, x):
        self.campo = x

    def cambiar_fumador(self, x):
        self.fumador = x

    def cambiar_animalCompania(self, x):
        self.animalCompania = x

    def cambiar_descripcion(self, x):
        self.descripcion = x

    def cambiar_zonaBuscada(self, x):
        self.zonaBuscada = x

    def cambiar_inicioEstancia(self, x):
        self.inicioEstancia = x

    def cambiar_finEstancia(self, x):
        self.finEstancia = x

    def cambiar_instrumento(self, x):
        self.instrumento = x

    def obtener_tags_asociados(self):
        return TagValue.objects.get(perfil=me)


class TagValue(models.Model):
    perfil = models.ForeignKey(Perfil,null=True, blank=True)
    tag = models.ForeignKey("Tag",null=True, blank=True)
    value = models.TextField()


class FotoPerfil(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
    perfil = models.ForeignKey(Perfil)


class Tag(models.Model):
    name = models.CharField(max_length=200)


class Conversacion(models.Model):
    emisor = models.ForeignKey(Usuario,related_name='conversacion_emisor',null=True, blank=True)
    receptor = models.ForeignKey(Usuario,related_name='conversacion_receptor',null=True, blank=True)
    inicioConv = models.DateTimeField(default=timezone.now)
    def obtener_mensajes(self):
        return Mensaje.objects.get(conversacion=me)


class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, null=True, blank=True)
    emisor = models.ForeignKey(Usuario,related_name='mensaje_emisor',null=True, blank=True)
    #u2.mensaje_emisor.all()
    #obtener todos los mensajes en los que u2 es emisor
    receptor= models.ForeignKey(Usuario,related_name='mensaje_receptor',null=True, blank=True)
    #u2.mensaje_receptor.all()
    #obtener todos los mensajes en los que u2 es receptor
    fechaEnvio = models.DateTimeField(default=timezone.now)
    mensaje = models.TextField()


class Log(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    evento = models.TextField()


class Casa(models.Model):
    dueno = models.ForeignKey(Persona,blank=True,null=True)
    ciudad = models.CharField(max_length=200)
    numHabitaciones = models.IntegerField()
    numHabitacionesDisponibles = models.IntegerField()
    descripcion = models.TextField()
    alquilerPorHabitaciones = models.BooleanField()
    precioAlquiler = models.FloatField()
    gastosComplementarios = models.FloatField()

    def obtener_habitaciones(self):
        return Habitacion.objects.get(casa=me)


def generar_ruta_image(instance, filename):
    return "%s_%s" % (str(time()).replace('.', '_'),filename)


class FotoCasa(models.Model):
    foto = models.FileField(upload_to=generar_ruta_image)
    casa = models.ForeignKey(Casa,blank=True,null=True)


class Habitacion(models.Model):
    casa = models.ForeignKey(Casa,null=True, blank=True)
    descripcion = models.TextField()


class FotoHabitacion(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
    habitacion = models.ForeignKey(Habitacion,blank=True,null=True)
