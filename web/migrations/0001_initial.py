# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 21:15
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import web.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Busqueda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('', 'Sin especificar'), ('H', 'Hombre'), ('M', 'Mujer')], max_length=1, verbose_name='Sexo')),
                ('pet', models.CharField(blank=True, choices=[('', 'Ninguna'), ('P', 'Perro'), ('G', 'Gato'), ('O', 'Otros')], max_length=1, verbose_name='Mascota')),
                ('isSmoker', models.BooleanField(default=False, verbose_name='Fumador')),
                ('lookingIn', models.CharField(blank=True, max_length=35, verbose_name='Ciudad/zona en la que buscas piso')),
            ],
        ),
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
                ('dueno', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FotoCasa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.FileField(upload_to=web.models.generar_ruta_image)),
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
                ('foto', models.FileField(upload_to=web.models.generar_ruta_image)),
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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(blank=True, max_length=35, verbose_name='Nombre')),
                ('lastName', models.CharField(blank=True, max_length=35, verbose_name='Apellidos')),
                ('telephone', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message='N&uacute;mero de tel&eacute;fono inv&aacute;lido (debe tener de 9 a 15 d&iacute;gitos)', regex='^\\+?1?\\d{9,15}$')], verbose_name='Numero de telefono')),
                ('gender', models.CharField(blank=True, choices=[('', 'Sin especificar'), ('H', 'Hombre'), ('M', 'Mujer')], max_length=1, verbose_name='Sexo')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('ocupation', models.CharField(blank=True, choices=[('', 'Sin especificar'), ('E', 'Estudiante'), ('T', 'Trabajador')], max_length=1, verbose_name='Ocupacion')),
                ('description', models.TextField(blank=True, verbose_name='Descripcion')),
                ('pet', models.CharField(blank=True, choices=[('', 'Ninguna'), ('P', 'Perro'), ('G', 'Gato'), ('O', 'Otros')], max_length=1, verbose_name='Mascota')),
                ('isSmoker', models.BooleanField(default=False, verbose_name='Fumador')),
                ('lookingIn', models.CharField(blank=True, max_length=35, verbose_name='Ciudad/zona en la que buscas piso')),
                ('iniEstancia', models.DateField(blank=True, null=True, verbose_name='Inicio de la estancia')),
                ('finEstancia', models.DateField(blank=True, null=True, verbose_name='Fin de la estancia')),
                ('Instrument', models.CharField(blank=True, max_length=50, verbose_name='Instrumento')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=25, verbose_name='Etiqueta')),
                ('perfil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='validation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ash', models.TextField(max_length=200)),
                ('creation_date', models.DateField()),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='fotoperfil',
            name='perfil',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Profile'),
        ),
        migrations.AddField(
            model_name='fotohabitacion',
            name='habitacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Habitacion'),
        ),
    ]
