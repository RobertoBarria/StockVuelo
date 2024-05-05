import pytest
from tienda.models import Avion, StockAvion
from tienda.fixtures import create_producto

@pytest.fixture
def avion():
    return Avion.objects.create(nombre='Avión de prueba')

@pytest.fixture
def producto():
    return create_producto()

@pytest.fixture
def stock_avion(producto, avion):
    return StockAvion.objects.create(producto=producto, avion=avion, cantidad_disponible=10)

@pytest.mark.django_db
def test_avion_creation(avion):
    assert avion.nombre == 'Avión de prueba'

@pytest.mark.django_db
def test_avion_str(avion):
    assert str(avion) == 'Avión de prueba'

@pytest.mark.django_db
def test_stock_avion_creation(stock_avion):
    assert stock_avion.producto.nombre_producto == 'Producto de prueba'
    assert stock_avion.avion.nombre == 'Avión de prueba'
    assert stock_avion.cantidad_disponible == 10

@pytest.mark.django_db
def test_stock_avion_unique_together(stock_avion, producto, avion):
    with pytest.raises(Exception):
        StockAvion.objects.create(producto=producto, avion=avion, cantidad_disponible=5)