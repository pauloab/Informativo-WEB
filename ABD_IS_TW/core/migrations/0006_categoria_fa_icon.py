# Generated by Django 4.0.1 on 2022-02-11 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_usuario_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='fa_icon',
            field=models.CharField(default='fas fa-home', max_length=150),
            preserve_default=False,
        ),
    ]