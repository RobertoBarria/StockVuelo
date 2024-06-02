from categorias.models import Categoria
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importar el módulo messages
from .models import Producto, Avion, StockAvion, MovimientoProducto
from django.core.paginator import Paginator
from django.contrib.auth.models import User



@login_required
def producto_detalle(request, categoria_slug, producto_slug):
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    single_product = get_object_or_404(Producto, categoria=categoria, slug=producto_slug)
    avion_id = request.session.get('avion_id')

    stock_avion = StockAvion.objects.filter(producto=single_product, avion_id=avion_id).first()
    stock = stock_avion.cantidad_disponible if stock_avion else 0
    cantidad_minima = stock_avion.cantidad_Minima if stock_avion else 0

    context = {
        'single_product': single_product,
        'categoria': categoria,
        'stock': stock,
        'cantidad_minima': cantidad_minima
    }

    return render(request, 'tienda/producto_detalle.html', context)

@login_required
def lista_productos(request):
    productos_list = Producto.objects.all()
    paginator = Paginator(productos_list, 6)  # Muestra 10 productos por página

    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    return render(request, 'administracion/lista_productos.html', {'productos': productos})


@login_required
def tienda(request, categoria_slug=None):
    cat = None
    productos = None
    avion_id = request.session.get('avion_id')
    
    if not avion_id:
        messages.error(request, 'No se ha seleccionado un avión.')  
        return redirect('login')

    if categoria_slug:
        cat = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=cat, is_available=True, stockavion__avion_id=avion_id)
    else:
        productos = Producto.objects.filter(is_available=True, stockavion__avion_id=avion_id)
    
    productos = productos.distinct()
    producto_cantidad = productos.count()
    
    # Obtener el nombre del avión seleccionado
    avion_seleccionado = Avion.objects.get(id=avion_id).nombre
    
    # Obtener el nombre del usuario
    nombre_usuario = request.user.username

    # Obtener todas las categorías
    categorias = Categoria.objects.all()

    productos_stock = []
    for producto in productos:
        stock = StockAvion.objects.filter(producto=producto, avion_id=avion_id).first()
        productos_stock.append({
            'producto': producto,
            'stock': stock.cantidad_disponible if stock else 0,
            'cantidad_minima': stock.cantidad_Minima if stock else 0
        })
    
    context = {
        'productos_stock': productos_stock,
        'producto_cantidad': producto_cantidad,
        'avion_seleccionado': avion_seleccionado,
        'nombre_usuario': nombre_usuario,
        'categorias': categorias,  # Agregar las categorías al contexto
    }
    return render(request, 'tienda/tienda.html', context)



@login_required
def asignar_stock_a_avion(request):
    producto_id = request.POST.get('producto_id')
    avion_id = request.POST.get('avion_id')
    cantidad = int(request.POST.get('cantidad'))

    try:
        producto = Producto.objects.get(id=producto_id)
        avion = Avion.objects.get(id=avion_id)
        stock_avion = StockAvion(producto=producto, avion=avion, cantidad_disponible=cantidad)
        stock_avion.save()
        mensaje = f"Se asignaron {cantidad} unidades de {producto.nombre_producto} al avión {avion.nombre}."
    except Producto.DoesNotExist:
        mensaje = "El producto especificado no existe."
    except Avion.DoesNotExist:
        mensaje = "El avión especificado no existe."

    return render(request, 'tienda/asignar_stock.html', {'mensaje': mensaje})



