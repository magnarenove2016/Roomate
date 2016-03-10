from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator  #utilizando una expresion regular valida un determinado campo
from django.utils.translation import ugettext_lazy as _  #traduccion de los formatos de texto de errores

#formato de mensaje para controlar que no se meta mal las fechas
FECHAS_ESTANCIA_ERROR = _(u"revise las fechas de estancia. "u"La fecha de inicio no debe ser superior a la fecha de final")


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

class GrupoUsuariosSimilares(models.Model):
    persona=models.ManyToManyField(Persona)
    desc=models.CharField(max_length=200)

class Perfil(models.Model):
    persona=models.OneToOneField(
        Persona,
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

"""
    perfil del usuario en él.
    contiene todos los datos extra que  necesitamos saber de un Usuario
    a parte de los que le pedimos cuando se registra.
    hay un unico perfil por usuario.
"""
class Profile(models.Model):
    #las elecciones posibles de la opción de sexo. del usuario
    GENDER_CHOICES = (
        ('', 'Sin especificar'),
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )
    #las elecciones posibles de la opción de ocupación. del usuario
    OCUPATION_CHOICES = (
        ('', 'Sin especificar'),
        ('E', 'Estudiante'),
        ('T', 'Trabajador'),
    )
    #las elecciones posibles de la opción de mascota. del usuario
    PET_CHOICES = (
        ('', 'Ninguna'),
        ('P', 'Perro'),
        ('G', 'Gato'),
        ('O', 'Otros'),
    )


    # Expresión regular para validar el número de teléfono
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Número de teléfono inválido (debe tener de 9 a 15 dígitos)")


    # Usuario asociado al perfil (un perfil por usuario)
    user = models.OneToOneField('auth.User', models.CASCADE)

    # Campos del perfil
    firstName = models.CharField(max_length=35, blank=True, verbose_name='Nombre')
    lastName = models.CharField(max_length=35, blank=True, verbose_name='Apellidos')
    telephone = models.CharField(max_length=15, validators=[phone_regex], blank=True, verbose_name='Número de teléfono')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="Sexo")

    birthdate = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    ocupation = models.CharField(max_length=1, choices=OCUPATION_CHOICES, blank=True, verbose_name="Ocupación")
    description = models.TextField(blank=True, verbose_name="Descripción")

    pet = models.CharField(max_length=1, choices=PET_CHOICES, blank=True, verbose_name='Mascota')
    isSmoker = models.BooleanField(default=False, verbose_name='Fumador')
    lookingIn = models.CharField(max_length=35, blank=True, verbose_name="Ciudad/zona en la que buscas piso")
    iniEstancia = models.DateField(blank=True, null=True, verbose_name="Inicio de la estancia")
    finEstancia = models.DateField(blank=True, null=True, verbose_name="Fin de la estancia")
    Instrument = models.CharField(max_length=50, blank=True, verbose_name='Instrumento')
    # photo = models.ImageField(upload_to='/data/photos/', verbose_name='Una foto tuya')

    #controlar que las fechas de estancia sean coherentes.
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.iniEstancia > self.finEstancia:
            raise ValidationError(FECHAS_ESTANCIA_ERROR)

    def __str__(self):
        return 'Perfil de ' + self.user.username

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'



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

class FotoCasa(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
                                            #Probablemente pasaran a ser filefield
    casa = models.ForeignKey(Casa,blank=True,null=True)

class Habitacion(models.Model):
    casa = models.ForeignKey(Casa,null=True, blank=True)
    descripcion = models.TextField()

class FotoHabitacion(models.Model):
    foto = models.CharField(max_length=200) #path a las fotos
    habitacion = models.ForeignKey(Habitacion,blank=True,null=True)
