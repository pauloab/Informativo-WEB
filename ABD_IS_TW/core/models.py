from email.policy import default
import profile
from timeit import default_timer
from django.db import models

# Create your models here.
class Usuario(models.Model):
    user_name = models.CharField(max_length=150,null=False,blank=False,unique=True)
    first_name = models.CharField(max_length=150,null=False,blank=False)
    last_name = models.CharField(max_length=150,null=False,blank=False)
    email = models.EmailField(max_length=150,null=False,blank=False,unique=True)
    password = models.TextField(null=False,blank=False)
    profile_picture = models.ImageField(max_length=255,null=False,blank=False,upload_to="fotos/perfiles")
    is_sancionado = models.BooleanField(default=False,null=False,blank=False)

class Categoria(models.Model):
    categoria = models.CharField(max_length=150,null=False,blank=False)

class Articulo(models.Model):
    titulo = models.CharField(max_length=200,null=False,blank=False)
    fecha_publicacion = models.DateField(null=False,blank=False,auto_now=True)
    contenido = models.TextField(max_length=250,null=False,blank=False)
    portada = models.ImageField(null=False,blank=False,upload_to="portadas/articulos")
    usuario = models.ForeignKey(to=Usuario,null=False,blank=False,on_delete=models.CASCADE)
    categoria = models.ForeignKey(to=Categoria,null=False,blank=False,on_delete=models.CASCADE)





