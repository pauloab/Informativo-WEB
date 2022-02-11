from ast import If, Return, Try
from audioop import reverse
import random
import re
import string
from xml.dom import NotFoundErr
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest

# Local Imports
from ABD_IS_TW.core.models import Articulo, Usuario, Categoria
from ABD_IS_TW.core.forms import LoginForm, UserForm, CategoriaForm, ArticuloForm
from ABD_IS_TW.core.utils import get_user


def index(request: HttpRequest):
    context = {}

    if request.method == "GET":
        noticias = Articulo.objects.all()[0:12]
        context['noticias'] = noticias
        return render(request, "index.html", context)
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
            elif usuario.sancionado:
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
    usuario = get_user(request)
    if request.method == "GET" and usuario:
        noticias = usuario.articulos.all()
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

    if articulo.usuario != get_user(request):
        return HttpResponseForbidden()

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