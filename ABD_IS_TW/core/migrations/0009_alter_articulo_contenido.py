# Generated by Django 4.0.1 on 2022-02-11 06:29

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_articulo_contenido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='contenido',
            field=django_quill.fields.QuillField(),
        ),
    ]
