
from .models import Orden, OrdenProducto
from categorias.models import Categoria

def cantidad_productos_en_orden(request):
    if request.user.is_authenticated:
        avion_id = request.session.get('avion_id')
        orden = Orden.objects.filter(usuario=request.user, avion_id=avion_id, completada=False).first()
        if orden:
            orden_productos = OrdenProducto.objects.filter(orden=orden).count()
        else:
            orden_productos = 0
    else:
        orden_productos = 0

    return {'orden_productos': orden_productos}



def categorias_context(request):
    return {
        'categorias': Categoria.objects.all()
    }