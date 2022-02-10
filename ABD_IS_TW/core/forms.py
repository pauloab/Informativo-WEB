from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre de usuario")
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True, max_length=220,
        label="Contraseña")