from ast import If, Return
from audioop import reverse
import random
import string
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest

# Local Imports
from ABD_IS_TW.core.models import Articulo, Usuario
from ABD_IS_TW.core.forms import LoginForm
from ABD_IS_TW.core.utils import get_user

def index(request: HttpRequest):

    # obtener el usuario en caso de existir
    context = {"usuario":get_user(request)}

    if request.method == "GET":
        noticias = Articulo.objects.all()[0:12]
        context['noticias'] = noticias
        return render(request,"index.html", context)
    return HttpResponseBadRequest()

def login(request: HttpRequest):
    context = {"usuario":get_user(request)}

    if request.method == 'GET':
        loginForm = LoginForm()
        context["loginForm"] = loginForm
        return render(request,'login.html', context)
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        context["loginForm"] = loginForm
        if loginForm.is_valid():
            username = loginForm.cleaned_data["username"]
            password = loginForm.cleaned_data["password"]
            usuario  =Usuario.objects.filter(user_name=username, password=password).first()
            if usuario:
                token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24))
                usuario.token = token
                usuario.save()
                request.session["token"] = token
                return redirect("index")
            loginForm.add_error(None, error="Credenciales Incorrectas")
        return render(request,'login.html',context)
    return HttpResponseBadRequest()


def logout(request: HttpRequest):
    context = {"usuario":get_user(request)}
    if context.get("usuario"):
        request.session["usuario"] = None
        usr = context["usuario"]
        usr.token = None
        usr.save()
        return redirect("index")
    return HttpResponseBadRequest()

def profile_info(request: HttpRequest):
    context = {"usuario":get_user(request)}
    if request.method == "GET":
        return render(request,"showProfile.html",context)