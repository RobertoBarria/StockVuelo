from categorias.models import Categoria
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importar el módulo messages
from .models import Producto, Avion, StockAvion, MovimientoProducto,Orden,OrdenProducto,MovimientoHistorial
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import transaction
from django.db import models

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
    paginator = Paginator(productos_list, 6)  

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
    
    avion_seleccionado = Avion.objects.get(id=avion_id).nombre
    nombre_usuario = request.user.username
    categorias = Categoria.objects.all()

    productos_stock = []
    for producto in productos:
        stock = StockAvion.objects.filter(producto=producto, avion_id=avion_id).first()
        productos_stock.append({
            'producto': producto,
            'stock': stock.cantidad_disponible if stock else 0,
            'cantidad_minima': stock.cantidad_Minima if stock else 0
        })
    
    orden = None
    orden_productos = 0
    
    if request.user.is_authenticated:
        orden = Orden.objects.filter(usuario=request.user, avion_id=avion_id, completada=False).first()
        if orden:
            orden_productos = OrdenProducto.objects.filter(orden=orden).count()
    
    context = {
        'productos_stock': productos_stock,
        'producto_cantidad': producto_cantidad,
        'avion_seleccionado': avion_seleccionado,
        'nombre_usuario': nombre_usuario,
        'categorias': categorias,
        'orden_productos': orden_productos,  
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
        
        MovimientoHistorial.objects.create(
            producto=producto,
            avion=avion,
            cantidad=cantidad,
            tipo_movimiento='AS',
            observacion='Ajuste Stock',
            usuario=request.user
        )
                
        mensaje = f"Se asignaron {cantidad} unidades de {producto.nombre_producto} al avión {avion.nombre}."
    except Producto.DoesNotExist:
        mensaje = "El producto especificado no existe."
    except Avion.DoesNotExist:
        mensaje = "El avión especificado no existe."

    return render(request, 'tienda/asignar_stock.html', {'mensaje': mensaje})


@login_required
def crear_orden(request):
    productos = Producto.objects.filter(is_available=True)
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        producto = get_object_or_404(Producto, id=producto_id)
        usuario = request.user
        avion_id = request.session.get('avion_id')
        avion = get_object_or_404(Avion, id=avion_id)

        with transaction.atomic():
            orden, created = Orden.objects.get_or_create(usuario=usuario, avion=avion, completada=False)

            orden_producto, created = OrdenProducto.objects.get_or_create(orden=orden, producto=producto)
            orden_producto.cantidad += cantidad
            orden_producto.save()

            stock_avion = StockAvion.objects.get(producto=producto, avion=avion)
            if stock_avion.cantidad_disponible >= cantidad:
                stock_avion.cantidad_disponible -= cantidad
                stock_avion.save()
            else:
                return HttpResponse("No hay suficiente stock para el producto: " + producto.nombre_producto)

        return redirect('producto_detalle', categoria_slug=producto.categoria.slug, producto_slug=producto.slug)

    return render(request, 'tienda/crear_orden.html', {'productos': productos})

@login_required
def agregar_a_orden(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    usuario = request.user
    avion_id = request.session.get('avion_id')
    avion = get_object_or_404(Avion, id=avion_id)

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad'))

        with transaction.atomic():
            orden, created = Orden.objects.get_or_create(usuario=usuario, avion=avion, completada=False)

            orden_producto, created = OrdenProducto.objects.get_or_create(orden=orden, producto=producto)
            if created:
                orden_producto.cantidad = cantidad
            else:
                orden_producto.cantidad += cantidad
            orden_producto.save()

            stock_avion = StockAvion.objects.get(producto=producto, avion=avion)
            if stock_avion.cantidad_disponible >= cantidad:
                stock_avion.cantidad_disponible -= cantidad
                stock_avion.save()
            else:
                return HttpResponse("No hay suficiente stock para el producto: " + producto.nombre_producto)

        return redirect('producto_detalle', categoria_slug=producto.categoria.slug, producto_slug=producto.slug)

    return redirect('producto_detalle', categoria_slug=producto.categoria.slug, producto_slug=producto.slug)


@login_required
def orden_detalle(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)
    orden_productos = OrdenProducto.objects.filter(orden=orden)

    productos_stock = []
    for orden_producto in orden_productos:
        stock_avion = StockAvion.objects.get(producto=orden_producto.producto, avion=orden.avion)
        productos_stock.append({
            'orden_producto': orden_producto,
            'cantidad_disponible': stock_avion.cantidad_disponible
        })

    context = {
        'orden': orden,
        'productos_stock': productos_stock
    }

    return render(request, 'tienda/orden_detalle.html', context)


@login_required
def actualizar_cantidad(request, orden_producto_id):
    orden_producto = get_object_or_404(OrdenProducto, id=orden_producto_id)
    nueva_cantidad = int(request.POST.get('cantidad'))
    stock_avion = get_object_or_404(StockAvion, producto=orden_producto.producto, avion=orden_producto.orden.avion)

    with transaction.atomic():
        diferencia = nueva_cantidad - orden_producto.cantidad
        if stock_avion.cantidad_disponible >= diferencia:
            stock_avion.cantidad_disponible -= diferencia
            stock_avion.save()
            orden_producto.cantidad = nueva_cantidad
            orden_producto.save()
        else:
            return HttpResponse("No hay suficiente stock para el producto: " + orden_producto.producto.nombre_producto)

    return redirect('orden_detalle', orden_id=orden_producto.orden.id)

@login_required
def eliminar_producto(request, orden_producto_id):
    orden_producto = get_object_or_404(OrdenProducto, id=orden_producto_id)
    stock_avion = get_object_or_404(StockAvion, producto=orden_producto.producto, avion=orden_producto.orden.avion)

    with transaction.atomic():
        stock_avion.cantidad_disponible += orden_producto.cantidad
        stock_avion.save()
        orden_producto.delete()

    return redirect('orden_detalle', orden_id=orden_producto.orden.id)


@login_required
def listar_ordenes(request):
    ordenes = Orden.objects.filter(usuario=request.user)

    context = {
        'ordenes': ordenes
    }

    return render(request, 'tienda/listar_ordenes.html', context)

@login_required
def cerrar_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)
    if request.method == 'POST':
        orden.completada = True
        orden.save()
        for orden_producto in OrdenProducto.objects.filter(orden=orden):
            MovimientoHistorial.objects.create(
                producto=orden_producto.producto,
                avion=orden.avion,
                cantidad=(orden_producto.cantidad * -1),
                tipo_movimiento='MO',
                observacion='Cierre de Orden',
                usuario=request.user
            )
        return redirect('orden_detalle', orden_id=orden.id)
    return redirect('orden_detalle', orden_id=orden.id)


@login_required
def cancelar_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)
    if request.method == 'POST' and not orden.completada:
        with transaction.atomic():
            for orden_producto in OrdenProducto.objects.filter(orden=orden):
                stock_avion = get_object_or_404(StockAvion, producto=orden_producto.producto, avion=orden.avion)
                stock_avion.cantidad_disponible += orden_producto.cantidad
                stock_avion.save()

                MovimientoHistorial.objects.create(
                    producto=orden_producto.producto,
                    avion=orden.avion,
                    cantidad=orden_producto.cantidad,
                    tipo_movimiento='AS',
                    observacion='Cancelación de Orden',
                    usuario=request.user
                )

            orden.delete()
            messages.success(request, 'La orden ha sido cancelada y los productos han sido devueltos al stock.')
        return redirect('listar_ordenes')
    return redirect('orden_detalle', orden_id=orden.id)