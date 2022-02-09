from multiprocessing import context
from django.shortcuts import render
from ABD_IS_TW.core.models import Articulo
# Create your views here.

def index(request):
    if request.method == "GET":
        noticias = Articulo.objects.all()[0:12]
        context = {'noticias':noticias,'nombre':"pito"}
        print(context['nombre'])
        return render(request,"index.html", context)