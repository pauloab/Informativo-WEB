# Generated by Django 4.0.1 on 2022-08-09 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_articulo_contenido'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sugerencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_sug', models.TextField()),
                ('asunto_sug', models.CharField(max_length=254)),
                ('fecha_sug', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo_boletin', models.EmailField(max_length=50, unique=True)),
                ('nom_boletin', models.CharField(max_length=50)),
                ('ape_boletin', models.CharField(max_length=50)),
                ('estado_sub', models.BooleanField(default=True)),
            ],
        ),
    ]