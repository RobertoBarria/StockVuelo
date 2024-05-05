import pytest
from django.urls import reverse
from tienda.models import Producto
from categorias.models import Categoria

@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nombre_categoria='Electrónica', slug='electronica')

@pytest.fixture
def producto(categoria, db):
    return Producto.objects.create(
        nombre_producto='Producto de prueba',
        slug='producto-de-prueba',
        descripcion='Descripción de prueba',
        precio=100,
        imagen='test.jpg',
        categoria=categoria
    )

@pytest.mark.django_db
def test_producto_creation(producto):
    assert producto.nombre_producto == 'Producto de prueba'
    assert producto.slug == 'producto-de-prueba'
    assert producto.descripcion == 'Descripción de prueba'
    assert producto.precio == 100
    assert producto.imagen == 'test.jpg'
    assert producto.is_available is True
    assert producto.categoria.nombre_categoria == 'Electrónica'

@pytest.mark.django_db
def test_producto_str(producto):
    assert str(producto) == 'Producto de prueba'

@pytest.mark.django_db
def test_get_url(producto, categoria):
    expected_url = reverse('productos_por_categoria', args=[categoria.slug])
    assert categoria.get_url() == expected_url