
from lib2to3.pgen2 import token
from django.http import HttpRequest

from ABD_IS_TW.core.models import Usuario

def get_user(request : HttpRequest) -> Usuario:
    user = request.session.get('token')
    if user:
        user = Usuario.objects.filter(token=user).first()
    return user