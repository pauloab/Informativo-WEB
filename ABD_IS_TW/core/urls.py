from unicodedata import name
from django import views
from django.urls import path
from ABD_IS_TW.core import views

urlpatterns = [
    path("",views.index, name="index"),
    path("auth/login",views.login,name="login"),
    path("auth/logout",views.logout,name="logout")
]
