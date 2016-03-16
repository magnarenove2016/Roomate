from django.contrib.auth.models import User
<<<<<<< HEAD
from django.core.validators import RegexValidator  # utilizando una expresion regular valida un determinado campo
from django.db import models
from django.utils.translation import ugettext_lazy as _  # traduccion de los formatos de texto de errores
from time import time
=======
from django.utils import timezone
from django.core.validators import RegexValidator  #utilizando una expresion regular valida un determinado campo
from django.utils.translation import ugettext_lazy as _  #traduccion de los formatos de texto de errores
from datetime import datetime

#formato de mensaje para controlar que no se meta mal las fechas
FECHAS_ESTANCIA_ERROR = _(u"revise las fechas de estancia. "u"La fecha de inicio no debe ser superior a la fecha de final")
FECHAS_ESTANCIA_INCOMPLT = _(u"revise las fechas de estancia. "u"Rellene las fechas de estancia")
# Create your models here.
class Usuario(models.Model):
    # Campo asociado al usuario gestionado por django.
    user = models.OneToOneField(User)
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
        Usuario,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def obtener_perfil(self):
        return Perfil.objects.get(persona=me)

    def eliminar_perfil(self):
        b = Perfil.objects.get(persona=me)
        b.delete()
>>>>>>> origin/djbienve

# formato de mensaje para controlar que no se meta mal las fechas
FECHAS_ESTANCIA_ERROR = _(
    u"revise las fechas de estancia. "u"La fecha de inicio no debe ser superior a la fecha de final")
FECHAS_ESTANCIA_INCOMPLT = _(u"revise las fechas de estancia. "u"Rellene las fechas de estancia")

"""
    Perfil del usuario que contiene todos los datos extra que
    necesitamos saber de un usuario a parte de los que le pedimos
    cuando se registra. Hay un unico perfil por usuario.
"""
class validation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False, blank=True
    )
    ash = models.TextField(null=False,max_length=200)
    creation_date = models.DateField()


<<<<<<< HEAD
=======
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

"""
    perfil del usuario en él.
    contiene todos los datos extra que  necesitamos saber de un Usuario
    a parte de los que le pedimos cuando se registra.
    hay un unico perfil por usuario.
"""
class validation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False, blank=True
    )
    ash = models.TextField(null=False,max_length=200)
    creation_date = models.DateField()


>>>>>>> origin/djbienve
class Profile(models.Model):
    # Las elecciones posibles de la opcion de sexo. del usuario
    GENDER_CHOICES = (
        ('', 'Sin especificar'),
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )
    # Las elecciones posibles de la opcion de ocupacion. del usuario
    OCUPATION_CHOICES = (
        ('', 'Sin especificar'),
        ('E', 'Estudiante'),
        ('T', 'Trabajador'),
    )
    # Las elecciones posibles de la opcion de mascota. del usuario
    PET_CHOICES = (
        ('', 'Ninguna'),
        ('P', 'Perro'),
        ('G', 'Gato'),
        ('O', 'Otros'),
    )

    # Expresion regular para validar el numero de telefono
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="N&uacute;mero de tel&eacute;fono inv&aacute;lido (debe tener de 9 a 15 d&iacute;gitos)")

    # Usuario asociado al perfil (un perfil por usuario)
    user = models.OneToOneField('auth.User', models.CASCADE, related_name='profile')

    # Campos del perfil
    firstName = models.CharField(max_length=35, blank=True, verbose_name='Nombre')
    lastName = models.CharField(max_length=35, blank=True, verbose_name='Apellidos')
    telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True, verbose_name='Numero de telefono')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="Sexo")

    birthdate = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    ocupation = models.CharField(max_length=1, choices=OCUPATION_CHOICES, blank=True, verbose_name="Ocupacion")
    description = models.TextField(blank=True, verbose_name="Descripcion")

    pet = models.CharField(max_length=1, choices=PET_CHOICES, blank=True, verbose_name='Mascota')
    isSmoker = models.BooleanField(default=False, verbose_name='Fumador')
    lookingIn = models.CharField(max_length=35, blank=True, verbose_name="Ciudad/zona en la que buscas piso")
    iniEstancia = models.DateField(blank=True, null=True, verbose_name="Inicio de la estancia")
    finEstancia = models.DateField(blank=True, null=True, verbose_name="Fin de la estancia")
    Instrument = models.CharField(max_length=50, blank=True, verbose_name='Instrumento')

    # photo = models.ImageField(upload_to='/data/photos/', verbose_name='Una foto tuya')

    # Controlar que las fechas de estancia sean coherentes
    def clean(self):
        from django.core.exceptions import ValidationError
        if (self.iniEstancia is None  and   self.finEstancia is not None) or (self.iniEstancia is not None  and  self.finEstancia is  None):
            raise ValidationError(FECHAS_ESTANCIA_INCOMPLT)
        elif (self.iniEstancia is not None  and  self.finEstancia is not None) and self.iniEstancia > self.finEstancia:
            raise ValidationError(FECHAS_ESTANCIA_ERROR)

    def __str__(self):
        return 'Perfil de ' + self.user.username

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


def generar_ruta_image(instance, filename):
    return "%s_%s" % (str(time()).replace('.', '_'), filename)


class FotoPerfil(models.Model):
    foto = models.FileField(upload_to=generar_ruta_image)
    perfil = models.ForeignKey(Profile, blank=True, null=True)


class Tag(models.Model):
<<<<<<< HEAD
    perfil = models.ForeignKey(Profile, null=True, blank=True)
    text = models.CharField(max_length=200, verbose_name='Etiqueta')

=======
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
    titulo = models.CharField(max_length=50) #nombre indentificativo del log
    fecha = models.DateTimeField(default=timezone.now)
    evento = models.TextField()
    def __str__(self):
        return 'Log: ' + self.titulo
>>>>>>> origin/djbienve

class Casa(models.Model):
    dueno = models.ForeignKey('auth.User', models.CASCADE, blank=True, null=True)
    ciudad = models.CharField(max_length=200)
    numHabitaciones = models.IntegerField()
    numHabitacionesDisponibles = models.IntegerField()
    descripcion = models.TextField()
    alquilerPorHabitaciones = models.BooleanField()
    precioAlquiler = models.FloatField()
    gastosComplementarios = models.FloatField()

    def obtener_habitaciones(self):
        return Habitacion.objects.get(casa=self)


class FotoCasa(models.Model):
    foto = models.FileField(upload_to=generar_ruta_image)
    casa = models.ForeignKey(Casa, blank=True, null=True)


class Habitacion(models.Model):
    casa = models.ForeignKey(Casa, null=True, blank=True)
    descripcion = models.TextField()


class FotoHabitacion(models.Model):
    foto = models.CharField(max_length=200)  # path a las fotos
    habitacion = models.ForeignKey(Habitacion, blank=True, null=True)
