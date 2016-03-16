# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-05 10:53
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Casa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=200)),
                ('numHabitaciones', models.IntegerField()),
                ('numHabitacionesDisponibles', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('alquilerPorHabitaciones', models.BooleanField()),
                ('precioAlquiler', models.FloatField()),
                ('gastosComplementarios', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicioConv', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='FotoCasa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.CharField(max_length=200)),
                ('casa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Casa')),
            ],
        ),
        migrations.CreateModel(
            name='FotoHabitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FotoPerfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='GrupoUsuariosSimilares',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('casa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Casa')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('evento', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaEnvio', models.DateTimeField(default=django.utils.timezone.now)),
                ('mensaje', models.TextField()),
                ('conversacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Conversacion')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(blank=True, max_length=35, verbose_name='Nombre')),
                ('lastName', models.CharField(blank=True, max_length=35, verbose_name='Apellidos')),
                ('telephone', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='Número de teléfono inválido (debe tener de 9 a 15 dígitos)', regex='^\\+?1?\\d{9,15}$')], verbose_name='Número de teléfono')),
                ('gender', models.CharField(blank=True, choices=[('', 'Sin especificar'), ('H', 'Hombre'), ('M', 'Mujer')], max_length=1, verbose_name='Sexo')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('ocupation', models.CharField(blank=True, choices=[('', 'Sin especificar'), ('E', 'Estudiante'), ('T', 'Trabajador')], max_length=1, verbose_name='Ocupación')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('pet', models.CharField(blank=True, choices=[('', 'Ninguna'), ('P', 'Perro'), ('G', 'Gato'), ('O', 'Otros')], max_length=1, verbose_name='Mascota')),
                ('isSmoker', models.BooleanField(default=False, verbose_name='Fumador')),
                ('lookingIn', models.CharField(blank=True, max_length=35, verbose_name='Ciudad/zona en la que buscas piso')),
                ('iniEstancia', models.DateField(blank=True, null=True, verbose_name='Inicio de la estancia')),
                ('finEstancia', models.DateField(blank=True, null=True, verbose_name='Fin de la estancia')),
                ('Instrument', models.CharField(blank=True, max_length=50, verbose_name='Instrumento')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Perfiles',
                'verbose_name': 'Perfil',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TagValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.CharField(max_length=200, unique=True)),
                ('contrasena', models.CharField(max_length=200)),
                ('alias', models.CharField(max_length=200)),
                ('activation_key', models.CharField(max_length=40)),
                ('verificado', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='web.Persona')),
                ('fechaNacimiento', models.DateTimeField()),
                ('sexo', models.CharField(max_length=200)),
                ('trabajadorEstudiante', models.BooleanField()),
                ('campo', models.CharField(max_length=200)),
                ('fumador', models.BooleanField()),
                ('animalCompania', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('zonaBuscada', models.CharField(max_length=200)),
                ('inicioEstancia', models.DateTimeField()),
                ('finEstancia', models.DateTimeField()),
                ('instrumento', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='persona',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Usuario'),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='emisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mensaje_emisor', to='web.Usuario'),
        ),
        migrations.AddField(
            model_name='mensaje',
            name='receptor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mensaje_receptor', to='web.Usuario'),
        ),
        migrations.AddField(
            model_name='grupousuariossimilares',
            name='persona',
            field=models.ManyToManyField(to='web.Persona'),
        ),
        migrations.AddField(
            model_name='fotohabitacion',
            name='habitacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Habitacion'),
        ),
        migrations.AddField(
            model_name='conversacion',
            name='emisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversacion_emisor', to='web.Usuario'),
        ),
        migrations.AddField(
            model_name='conversacion',
            name='receptor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversacion_receptor', to='web.Usuario'),
        ),
        migrations.AddField(
            model_name='casa',
            name='dueno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Persona'),
        ),
        migrations.AddField(
            model_name='tagvalue',
            name='perfil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Perfil'),
        ),
        migrations.AddField(
            model_name='fotoperfil',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Perfil'),
        ),
    ]
