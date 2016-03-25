from time import time

from django.contrib.auth.models import User
from django.core.validators import RegexValidator  # utilizando una expresion regular valida un determinado campo
from django.db import models
from django.utils.translation import ugettext_lazy as _  # traduccion de los formatos de texto de errores

# formato de mensaje para controlar que no se meta mal las fechas
FECHAS_ESTANCIA_ERROR = _("Revisa las fechas de estancia. La fecha de inicio no debe ser superior a la fecha final.")
PHONE_ERROR = _('N&uacute;mero de tel&eacute;fono inv&aacute;lido (debe tener de 9 a 15 d&iacute;gitos)')

"""
    Perfil del usuario que contiene todos los datos extra que
    necesitamos saber de un usuario a parte de los que le pedimos
    cuando se registra. Hay un unico perfil por usuario.
"""

class Profile(models.Model):
    # Las elecciones posibles de la opcion de sexo. del usuario
    GENDER_CHOICES = (
        ('', _('Sin especificar')),
        ('H', _('Hombre')),
        ('M', _('Mujer')),
    )
    # Las elecciones posibles de la opcion de ocupacion. del usuario
    OCUPATION_CHOICES = (
        ('', _('Sin especificar')),
        ('E', _('Estudiante')),
        ('T', _('Trabajador')),
    )
    # Las elecciones posibles de la opcion de mascota. del usuario
    PET_CHOICES = (
        ('', _('Ninguna')),
        ('P', _('Perro')),
        ('G', _('Gato')),
        ('O', _('Otros')),
    )

    # Expresion regular para validar el numero de telefono
    phone_regex = RegexValidator(regex=r'^\+?1?(\d){9,15}$', message=PHONE_ERROR)

    # Usuario asociado al perfil (un perfil por usuario)
    user = models.OneToOneField('auth.User', models.CASCADE, related_name='profile')

    # Campos del perfil
    firstName = models.CharField(max_length=35, blank=True)
    lastName = models.CharField(max_length=35, blank=True)
    telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    birthdate = models.DateField(blank=True, null=True)
    ocupation = models.CharField(max_length=1, choices=OCUPATION_CHOICES, blank=True,)
    description = models.TextField(blank=True, )

    pet = models.CharField(max_length=1, choices=PET_CHOICES, blank=True)
    isSmoker = models.BooleanField(default=False)
    lookingIn = models.CharField(max_length=35, blank=True)
    iniEstancia = models.DateField(blank=True, null=True)
    finEstancia = models.DateField(blank=True, null=True)
    Instrument = models.CharField(max_length=50, blank=True)

    # Controlar que las fechas de estancia sean coherentes
    def clean(self):
        from django.core.exceptions import ValidationError
        if (self.iniEstancia is None): return
        if (self.finEstancia is None): return
        if (self.iniEstancia > self.finEstancia):
            raise ValidationError({'iniEstancia':'', 'finEstancia': _(FECHAS_ESTANCIA_ERROR)})

    def __str__(self):
        return 'Perfil de ' + self.user.username

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


def generar_ruta_image(instance, filename):
    return "%s_%s" % (str(time()).replace('.', '_'), filename)


class FotoPerfil(models.Model):
    id = models.AutoField(primary_key=True)
    foto = models.FileField(upload_to=generar_ruta_image)
    perfil = models.ForeignKey(Profile, blank=True, null=True, related_name="fotos")


class Tag(models.Model):
    perfil = models.ForeignKey(Profile, null=True, blank=True, related_name="tags")
    text = models.CharField(max_length=25, verbose_name='Etiqueta')


class Casa(models.Model):
    id = models.AutoField(primary_key=True)
    dueno = models.ForeignKey('auth.User', models.CASCADE, blank=True, null=True, related_name="casas")
    direccion=models.TextField()
    ciudad = models.CharField(max_length=200)
    numHabitaciones = models.IntegerField()
    numHabitacionesDisponibles = models.IntegerField()
    descripcion = models.TextField()
    alquilerPorHabitaciones = models.BooleanField()
    precioAlquiler = models.FloatField()
    gastosComplementarios = models.FloatField()
    latitude=models.FloatField()
    longitude=models.FloatField()

    def obtener_habitaciones(self):
        return self.habitaciones.all()


def generar_ruta_image(instance, filename):
    return "%s_%s" % (str(time()).replace('.', '_'), filename)


class FotoCasa(models.Model):
    id = models.AutoField(primary_key=True)
    foto = models.FileField(upload_to=generar_ruta_image)
    casa = models.ForeignKey(Casa, blank=True, null=True, related_name="fotos")


class Habitacion(models.Model):
    id = models.AutoField(primary_key=True)
    casa = models.ForeignKey(Casa, null=True, blank=True,related_name="habitaciones")
    descripcion = models.TextField()


class FotoHabitacion(models.Model):
    id = models.AutoField(primary_key=True)
    foto = models.CharField(max_length=200)  # path a las fotos
    habitacion = models.ForeignKey(Habitacion, blank=True, null=True)


#esta clase solo sirve para realizar busquedas. Nada mas
class Busqueda(models.Model):
    #las elecciones posibles de la opcion de sexo. del usuario
    GENDER_CHOICES = (
        ('', _('Sin especificar')),
        ('H', _('Hombre')),
        ('M', _('Mujer')),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name=_("Sexo"))
    isSmoker = models.BooleanField(default=False, verbose_name=_('Fumador'))
    lookingIn = models.CharField(max_length=35, blank=True, verbose_name=_("Ciudad / zona en la que buscas piso"))

#clase para mantener registro de gente que esta o no registrada
class validation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False, blank=True
    )
    ash = models.TextField(null=False,max_length=200)
    creation_date = models.DateField()

