import pytest
from django.urls import reverse
from tienda.models import Producto, Avion, StockAvion, MovimientoProducto
from categorias.models import Categoria  # Asegúrate de importar correctamente el modelo Categoria
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_producto_str():
    categoria = Categoria.objects.create(nombre_categoria='Electrónicos', descripcion='Productos electrónicos', slug='electronica')
    producto = Producto.objects.create(nombre_producto='Smartphone', slug='smartphone', descripcion='Un smartphone genial', precio=500, categoria=categoria)
    assert str(producto) == 'Smartphone'

@pytest.mark.django_db
def test_avion_str():
    avion = Avion.objects.create(nombre='Boeing 747')
    assert str(avion) == 'Boeing 747'

@pytest.mark.django_db
def test_stock_avion_unique_together():
    categoria = Categoria.objects.create(nombre_categoria='Electrónicos', descripcion='Productos electrónicos', slug='electronica')
    producto = Producto.objects.create(nombre_producto='Smartphone', slug='smartphone', descripcion='Un smartphone genial', precio=500, categoria=categoria)
    avion = Avion.objects.create(nombre='Boeing 747')
    stock_avion1 = StockAvion.objects.create(producto=producto, avion=avion, cantidad_disponible=10)
    # Intente crear otro stock_avion con el mismo producto y avión
    with pytest.raises(Exception):
        stock_avion2 = StockAvion.objects.create(producto=producto, avion=avion, cantidad_disponible=5)

@pytest.mark.django_db
def test_movimiento_producto_str():
    usuario = User.objects.create(username='testuser', email='test@example.com')
    categoria = Categoria.objects.create(nombre_categoria='Electrónicos', descripcion='Productos electrónicos', slug='electronica')
    producto = Producto.objects.create(nombre_producto='Smartphone', slug='smartphone', descripcion='Un smartphone genial', precio=500, categoria=categoria)
    avion_origen = Avion.objects.create(nombre='Origen')
    avion_destino = Avion.objects.create(nombre='Destino')
    movimiento = MovimientoProducto.objects.create(producto=producto, avion_origen=avion_origen, avion_destino=avion_destino, cantidad=5, usuario=usuario)
    assert str(movimiento) == '5 Smartphone de Origen a Destino'