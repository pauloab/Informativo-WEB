# Generated by Django 4.0.1 on 2022-02-11 06:23

from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_categoria_fa_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='core.categoria'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='contenido',
            field=django_quill.fields.QuillField(),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articulos', to='core.usuario'),
        ),
    ]
