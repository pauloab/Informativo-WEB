from ast import If, Return, Try
from audioop import reverse
from base64 import encode
import base64
import random
import re
import string
from telnetlib import STATUS
from xml.dom import NotFoundErr
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest
from django.urls import reverse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

# Local Imports
from ABD_IS_TW.core.models import Articulo, Sugerencias, Suscripcion, Usuario, Categoria
from ABD_IS_TW.core.forms import LoginForm, UserForm, CategoriaForm, ArticuloForm
from ABD_IS_TW.core.utils import get_user


def index(request: HttpRequest):
    context = {}

    if request.method == "GET":
        noticias = Articulo.objects.all()[0:12]
        context['noticias'] = noticias
        return render(request, "index.html", context)
    return HttpResponseBadRequest()

def recientes(request: HttpRequest):
    context = {}

    if request.method == "GET":
        articulos = Articulo.objects.all()
        context['articulos'] = articulos
        context['titulo'] = 'Recientes'
        return render(request, "articles.html", context)
    return HttpResponseBadRequest()

def login(request: HttpRequest):
    context = {}

    if request.method == 'GET':
        loginForm = LoginForm()
        context["loginForm"] = loginForm
        return render(request, 'login.html', context)
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        context["loginForm"] = loginForm
        if loginForm.is_valid():
            username = loginForm.cleaned_data["username"]
            password = loginForm.cleaned_data["password"]
            usuario = Usuario.objects.filter(
                user_name=username, password=password).first()
            if not usuario:
                loginForm.add_error(None, error="Credenciales Incorrectas.")
            elif usuario.is_sancionado:
                loginForm.add_error(None, error="Este usuario se encuentra sancionado.")
            else:
                token = ''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(24))
                usuario.token = token
                usuario.save()
                request.session["token"] = token
                return redirect("index")
        return render(request, 'login.html', context)
    return HttpResponseBadRequest()


def logout(request: HttpRequest):
    context = {}
    if get_user(request):
        request.session["usuario"] = None
        usr = get_user(request)
        usr.token = None
        usr.save()
        return redirect("index")
    return HttpResponseBadRequest()


def profile_info(request: HttpRequest):
    context = {}
    if request.method == "GET":
        return render(request, "showProfile.html", context)


def profile_edit(request: HttpRequest):
    context = {}
    usuario = get_user(request)
    if request.method == 'GET':
        userForm = UserForm(instance=usuario)
        context["userForm"] = userForm
        return render(request, "editProfile.html", context)
    elif request.method == "POST":
        userForm = UserForm(request.POST, request.FILES, instance=usuario)
        context["userForm"] = userForm
        if userForm.is_valid():
            userForm.save()
            return redirect("userInfo")
        return render(request, "editProfile.html", context)
    return HttpResponseBadRequest()


def render_article(request: HttpRequest, id: int):
    context = {}
    if request.method == "GET":
        articulo = None
        try:
            articulo = Articulo.objects.get(id=id)
        except Articulo.DoesNotExist:
            return HttpResponseNotFound()
        context["articulo"] = articulo
        return render(request, "article.html", context)
    return HttpResponseBadRequest()


def article_by_category(request: HttpRequest, id: int):
    context = {}
    if request.method == "GET":
        category = None
        try:
            category = Categoria.objects.get(id=id)
        except Articulo.DoesNotExist:
            return HttpResponseNotFound()
        context["icono"] = category.fa_icon
        context["articulos"] = category.articulos.all()
        context["titulo"] = category.categoria
        return render(request, "articles.html", context)
    return HttpResponseBadRequest()


def categories(request: HttpRequest):
    if request.method == "GET":
        return render(request, "categories.html")
    return HttpResponseBadRequest()


def delete_category(request: HttpRequest, id: int):
    if request.method == "GET":
        if get_user(request):
            try:
                categoria = Categoria.objects.get(id=id)
                categoria.delete()
                return redirect("category_list")
            except Categoria.DoesNotExist:
                return HttpResponseNotFound()
    return HttpResponseBadRequest()


def edit_category(request: HttpRequest, id: int):
    categoria = None
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == "GET":
        categoryForm = CategoriaForm(instance=categoria)
        context = {"categoryForm": categoryForm, "categoria" : categoria}
        return render(request, "categoryEdit.html",context)
    elif request.method == "POST":
        categoryForm = CategoriaForm(request.POST, instance=categoria)
        context = {"categoryForm": CategoriaForm, "categoria" : categoria}
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect("category_list")
        return render(request, "categoryEdit.html",context)
    return HttpResponseBadRequest()


def add_category(request: HttpRequest):
    if request.method == "GET":
        categoryForm = CategoriaForm()
        context = {"categoryForm": CategoriaForm}
        return render(request, "categoryAdd.html",context)
    elif request.method == "POST":
        categoryForm = CategoriaForm(request.POST)
        context = {"categoryForm": CategoriaForm}
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect("category_list")
        return render(request, "categoryAdd.html",context)
    return HttpResponseBadRequest()

def user_news_list(request: HttpRequest):
    if request.method == "GET":
        noticias = Articulo.objects.all()
        context = {"noticias":noticias}
        return render(request, "userNewsList.html",context)
    return HttpResponseBadRequest()

def add_user_new(request: HttpRequest):

    if request.method == "GET":
        form = ArticuloForm()
        context = {"articuloForm":form}
        return render(request,"addUserNew.html",context)
    elif request.method == "POST":
        articulo = Articulo()
        articulo.usuario = get_user(request)
        form = ArticuloForm(request.POST, request.FILES, instance= articulo)
        if form.is_valid():
            form.save()
         
            emails = Suscripcion.objects.values_list("correo_boletin",flat=True)
            with open(articulo.portada.path,"rb") as image_file: 
                encoded = base64.b64encode(image_file.read()).decode("utf-8")
            print(encoded)
            context = {"title":form.cleaned_data["titulo"],"image": encoded,
            "url":request.build_absolute_uri(reverse('article',kwargs={'id':articulo.id}))}
            plano = get_template("email.txt")
            html = get_template("mailBody.html")
            asunto = articulo.titulo+" - Informáticos-Web"
            desde = 'vegageovanny36@gmail.com'
            plano = plano.render(context)
            html = html.render(context)
            print(html)
            print()
            mensaje = EmailMultiAlternatives(asunto,plano,desde,emails)
            mensaje.attach_alternative(html, 'text/html')
            mensaje.send()
            return redirect("userNewsList")
        context = {"articuloForm":form}
        return render(request,"addUserNew.html",context)

    return HttpResponseBadRequest()

def edit_user_new(request: HttpRequest, id: int):
    articulo = None
    try:
        articulo = Articulo.objects.get(id=id)
    except Articulo.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == "GET":
        form = ArticuloForm(instance=articulo)
        context = {"articuloForm":form,
                    "noticia":articulo}
        return render(request,"editUserNew.html",context)
    elif request.method == "POST":
        form = ArticuloForm(request.POST, request.FILES, instance= articulo)
        if form.is_valid():
            form.save()
            return redirect("userNewsList")
        context = {"articuloForm":form,
                    "noticia":articulo}
        return render(request,"editUserNew.html",context)

    return HttpResponseBadRequest()

def delete_user_new(request: HttpRequest, id: int): 
    articulo = None
    try:
        articulo = Articulo.objects.get(id=id)
    except Articulo.DoesNotExist:
        return HttpResponseNotFound()

    if articulo.usuario != get_user(request):
        return HttpResponseForbidden()

    if request.method == "GET":
        articulo.delete()
        return redirect("userNewsList")
    return HttpResponseBadRequest()


def search_article(request: HttpRequest ):
    if request.method == "GET":
        search = request.GET.get("search")
        if search:
            context = {}
            articles = Articulo.objects.filter(titulo__contains=search)
            context["icono"] = "fas fa-search"
            context["articulos"] = articles.all()
            context["titulo"] = "Resultados de: "+search
            return render(request, "articles.html", context)
             
    return HttpResponseBadRequest()

def suscribirse(request: HttpRequest ):
    contex = {}
    if request.method == 'POST':
        correo = request.POST.get("email")
        nombre = request.POST.get("nom")
        apellido = request.POST.get("ape")
        print(f"{ correo }-{ nombre }-{ apellido }")
        if correo and nombre and apellido:
            sub = Suscripcion(correo_boletin = correo, nom_boletin = nombre, ape_boletin = apellido)
            sub.save()
            contex["msg"] = "Se ha guardado con exito la suscripcion."
        else:
            contex["msg"] = "Datos incompletos, su operacion no se llevo acabo."

    return render(request,"suscripcion.html",context=contex)

def suscribirseList(request: HttpRequest):
    if request.method == "GET":
        suscribirse = Suscripcion.objects.all()
        context = {"suscribirse":suscribirse}
        return render(request, "suscripcionList.html",context)
    return HttpResponseBadRequest()

def delete_sub(request: HttpRequest, id: int):
    if request.method == "GET":
        if get_user(request):
            try:
                subs = Suscripcion.objects.get(id=id)
                subs.delete()
                return redirect("suscribirseList")
            except Suscripcion.DoesNotExist:
                return HttpResponseNotFound()
    return HttpResponseBadRequest()

def escribir_sugerencia(request: HttpRequest ):
    contex = {}
    if request.method == 'POST':
        asunto = request.POST.get("asunto")
        descripcion = request.POST.get("descripcion")
        print(f"{ asunto }-{ descripcion }")
        if asunto and descripcion:
            sug = Sugerencias(asunto_sug = asunto, descripcion_sug = descripcion)
            sug.save()
            contex["msg"] = "Se ha guardado con exito su sugerencia."
        else:
            contex["msg"] = "Datos incompletos, su operacion no se llevo acabo."

    return render(request,"sugerencias.html",context=contex)

def sugerencia_listar(request: HttpRequest ):
    if request.method == "GET":
        sugerencias = Sugerencias.objects.all()
        context = {"sugerencias":sugerencias}
        return render(request, "sugerenciasList.html",context)
    return HttpResponseBadRequest()


