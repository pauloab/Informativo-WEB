from django import views
from django.urls import path
from ABD_IS_TW.core import views
urlpatterns = [
    path("",views.index)
]
