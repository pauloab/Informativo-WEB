from cProfile import label
import imp
from django import forms

from ABD_IS_TW.core import models

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre de usuario")
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True, max_length=220,
        label="Contraseña")

class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nombres")
    last_name =forms.CharField(
        max_length=150,
        required=True,
        label="Apellidos")
    email = forms.EmailField(
        max_length=150,
        required=True,
        label="Correo Electrónico")
    profile_picture = forms.FileField(
        max_length=255,
        allow_empty_file=True,
        required=False,
        label="Foto de perfil")
    
    class Meta:
        model = models.Usuario
        fields = ['first_name', 'last_name', 'email', 'profile_picture']

class CategoriaForm(forms.ModelForm):

    fa_icon = forms.CharField(max_length=150, required=True,label="Clase HTML del icono")

    class Meta:
        model = models.Categoria
        fields = '__all__'

class ArticuloForm(forms.ModelForm):

    class Meta:
        model = models.Articulo
        fields = ["titulo","contenido","portada","categoria"]