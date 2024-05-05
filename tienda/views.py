from django.shortcuts import render, get_object_or_404
from .models import StockAvion, Producto, Avion
from categorias.models import Categoria



def producto_detalle(request, categoria_slug, producto_slug):
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    single_product = get_object_or_404(Producto, categoria=categoria, slug=producto_slug)

    context = {
        'single_product': single_product,
        'categoria': categoria,
    }

    return render(request, 'tienda/producto_detalle.html', context)


def tienda(request, categoria_slug=None):
    cat = None
    productos = None
    if categoria_slug:
        cat = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=cat, is_available=True)
        producto_cantidad = productos.count()
    else:
        productos = Producto.objects.all().filter(is_available=True)
        producto_cantidad = productos.count()
    
    context = {
        'productos': productos,
        'producto_cantidad': producto_cantidad,
    }
    return render(request, 'tienda/tienda.html', context)


def asignar_stock_a_avion(request):
    # Supongamos que se recibe un formulario o una solicitud que contiene los datos del producto y el avión
    producto_id = request.POST.get('producto_id')
    avion_id = request.POST.get('avion_id')
    cantidad = int(request.POST.get('cantidad'))

    try:
        producto = Producto.objects.get(id=producto_id)
        avion = Avion.objects.get(id=avion_id)

        # Supongamos que deseas asignar la cantidad recibida de stock de este producto a este avión
        stock_avion = StockAvion(producto=producto, avion=avion, cantidad_disponible=cantidad)
        stock_avion.save()

        mensaje = f"Se asignaron {cantidad} unidades de {producto.nombre_producto} al avión {avion.nombre}."
    except Producto.DoesNotExist:
        mensaje = "El producto especificado no existe."
    except Avion.DoesNotExist:
        mensaje = "El avión especificado no existe."

    return render(request, 'tu_template.html', {'mensaje': mensaje})
