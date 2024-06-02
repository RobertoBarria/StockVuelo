
from django.shortcuts import render, redirect, get_object_or_404
from tienda.models import Producto
from categorias.models import Categoria  # Importa el modelo Categoria
from .forms import ProductoForm
from django.utils.text import slugify  # Importa slugify para generar slugs únicos
from .forms import CategoriaForm
from django.db import IntegrityError
from .forms import AvionForm,StockAvionForm
from cuentas.models import Cuenta
from django.contrib import messages
from .forms import RegistrationForm,UserEditForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .forms import MovimientoProductoForm
from tienda.models import MovimientoProducto
from tienda.models import Producto, StockAvion  # Importa Producto y StockAvion desde la aplicación tienda
from aviones.models import Avion  # Importa Avion desde la aplicación aviones
from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_GET



@login_required
def administracion(request):
    # Lógica para mostrar la vista general de administración
    return render(request, 'administracion/administracion.html')
@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'administracion/lista_productos.html', {'productos': productos})
@login_required
def crear_producto(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.slug = slugify(producto.nombre_producto)
            producto.precio = 0
            producto.is_available = True  # Establece is_available como True
            producto.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
        return render(request, 'administracion/crear_producto.html', {'form': form, 'categorias': categorias})



@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'administracion/editar_producto.html', {'form': form})
@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'administracion/confirmar_eliminar_producto.html', {'producto': producto})

#!/###############     Categorias
@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'administracion/lista_categorias.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.slug = slugify(categoria.nombre_categoria)
            categoria.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
        return render(request, 'administracion/crear_categoria.html', {'form': form})
    
@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            categoria = form.save(commit=False)
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'administracion/editar_categoria.html', {'form': form})
@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'administracion/confirmar_eliminar_categoria.html', {'categoria': categoria})



############    Aviones

@login_required
def lista_aviones(request):
    aviones = Avion.objects.all()
    return render(request, 'administracion/lista_aviones.html', {'aviones': aviones})
@login_required
def crear_avion(request):
    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_aviones')
    else:
        form = AvionForm()
    return render(request, 'administracion/crear_avion.html', {'form': form})
@login_required
def editar_avion(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        form = AvionForm(request.POST, instance=avion)
        if form.is_valid():
            form.save()
            return redirect('lista_aviones')
    else:
        form = AvionForm(instance=avion)
    return render(request, 'administracion/editar_avion.html', {'form': form})
@login_required
def eliminar_avion(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        avion.delete()
        return redirect('lista_aviones')
    return render(request, 'administracion/confirmar_eliminar_avion.html', {'avion': avion})


############    cuentas 

@login_required(login_url='login')
def lista_usuarios(request):
    usuarios = Cuenta.objects.all()
    return render(request, 'administracion/lista_usuarios.html', {'usuarios': usuarios})
@login_required(login_url='login')
def crear_usuario(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('lista_usuarios')
        else:
            # Aquí se maneja el caso de formulario no válido
            # Se renderiza el formulario nuevamente con los errores
            messages.error(request, 'Hubo un error al crear el usuario. Por favor, revisa los datos ingresados.')
            return render(request, 'administracion/crear_usuario.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'administracion/crear_usuario.html', {'form': form})

@login_required(login_url='login')
def editar_usuario(request, pk):
    usuario = get_object_or_404(Cuenta, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()  # Guarda los cambios en el usuario existente
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UserEditForm(instance=usuario)
    return render(request, 'administracion/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required(login_url='login')
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Cuenta, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('lista_usuarios')
    return render(request, 'administracion/confirmar_eliminar_usuario.html', {'usuario': usuario})

######### Asignación Stock

        
@login_required
def asignar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    aviones = Avion.objects.all()

    stock_por_avion = {}
    for avion in aviones:
        try:
            stock = StockAvion.objects.get(producto=producto, avion=avion)
            stock_por_avion[avion.id] = {
                'cantidad_disponible': stock.cantidad_disponible,
                'cantidad_Minima': stock.cantidad_Minima
            }
        except StockAvion.DoesNotExist:
            stock_por_avion[avion.id] = {
                'cantidad_disponible': 0,
                'cantidad_Minima': 0
            }

    if request.method == 'POST':
        forms = [StockAvionForm(avion, request.POST, prefix=str(avion.id)) for avion in aviones]
        all_valid = all(form.is_valid() for form in forms)
        if all_valid:
            for form in forms:
                cantidad_disponible = form.cleaned_data['cantidad_disponible']
                cantidad_Minima = form.cleaned_data['cantidad_Minima']
                avion = form.avion
                try:
                    stock_avion = StockAvion.objects.get(producto=producto, avion=avion)
                    stock_avion.cantidad_disponible = cantidad_disponible
                    stock_avion.cantidad_Minima = cantidad_Minima
                    stock_avion.save()
                except StockAvion.DoesNotExist:
                    StockAvion.objects.create(producto=producto, avion=avion, cantidad_disponible=cantidad_disponible, cantidad_Minima=cantidad_Minima)
            return redirect('lista_productos')
    else:
        forms = [
            StockAvionForm(
                avion,
                initial={
                    'cantidad_disponible': stock_por_avion[avion.id]['cantidad_disponible'],
                    'cantidad_Minima': stock_por_avion[avion.id]['cantidad_Minima']
                },
                prefix=str(avion.id)
            ) for avion in aviones
        ]

    return render(request, 'administracion/asignar_stock.html', {'forms': forms, 'producto': producto})

######### Movimiento Stock

@login_required
def movimiento_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = MovimientoProductoForm(request.POST, producto=producto)
        if form.is_valid():
            avion_origen = form.cleaned_data['avion_origen']
            avion_destino = form.cleaned_data['avion_destino']
            cantidad = form.cleaned_data['cantidad']

            # Verificar y actualizar el stock del avión de origen
            stock_origen = StockAvion.objects.get(producto=producto, avion=avion_origen)
            stock_resultante = stock_origen.cantidad_disponible - cantidad

            if stock_origen.cantidad_disponible >= cantidad:
                if stock_resultante >= stock_origen.cantidad_Minima:
                    stock_origen.cantidad_disponible -= cantidad
                    stock_origen.save()

                    # Actualizar el stock del avión de destino
                    stock_destino, created = StockAvion.objects.get_or_create(producto=producto, avion=avion_destino)
                    stock_destino.cantidad_disponible += cantidad
                    stock_destino.save()

                    # Crear el registro de movimiento
                    movimiento = MovimientoProducto(
                        producto=producto, 
                        avion_origen=avion_origen, 
                        avion_destino=avion_destino, 
                        cantidad=cantidad, 
                        usuario=request.user
                    )
                    movimiento.save()

                    messages.success(request, 'Movimiento de producto realizado exitosamente.')
                    return redirect('lista_movimientos')
                else:
                    messages.error(request, f'No se puede realizar el movimiento. El stock resultante en el avión de origen ({stock_resultante}) quedaría por debajo del mínimo permitido ({stock_origen.cantidad_Minima}).')
            else:
                messages.error(request, 'La cantidad de movimientos supera el stock disponible en el avión de origen.')
            
            return redirect('movimiento_producto', producto_id=producto_id)
    else:
        form = MovimientoProductoForm(producto=producto)
    
    return render(request, 'administracion/movimiento_producto.html', {'form': form, 'producto': producto})


@login_required
def lista_movimientos(request):
    movimientos = MovimientoProducto.objects.all()
    return render(request, 'administracion/lista_movimientos.html', {'movimientos': movimientos})


@require_GET
def obtener_stock_origen(request):
    producto_id = request.GET.get('producto_id')
    avion_id = request.GET.get('avion_id')

    if producto_id and avion_id:
        try:
            producto = Producto.objects.get(id=producto_id)
            avion = Avion.objects.get(id=avion_id)
            stock_avion = StockAvion.objects.get(producto=producto, avion=avion)
            return JsonResponse({'stock_origen': stock_avion.cantidad_disponible})
        except (Producto.DoesNotExist, Avion.DoesNotExist, StockAvion.DoesNotExist):
            return JsonResponse({'error': 'Datos no encontrados'}, status=404)
    
    return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
