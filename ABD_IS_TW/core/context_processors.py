import imp
from ABD_IS_TW.core.models import Categoria
from ABD_IS_TW.core.utils import get_user

def categories_processor(request):
    categories = Categoria.objects.all()            
    return {'categorias': categories,
            "usuario": get_user(request)}