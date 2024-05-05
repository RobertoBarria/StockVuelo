import pytest
from django.urls import reverse
from categorias.models import Categoria

@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nombre_categoria='Electrónica', slug='electronica')

@pytest.mark.django_db
def test_categoria_creation(categoria):
    assert categoria.nombre_categoria == 'Electrónica'
    assert categoria.slug == 'electronica'
    assert categoria.descripcion == ''
    assert categoria.cat_imagen == ''
    
@pytest.mark.django_db
def test_categoria_str(categoria):
    assert str(categoria) == 'Electrónica'

@pytest.mark.django_db
def test_get_url(categoria):
    expected_url = reverse('productos_por_categoria', args=[categoria.slug])
    assert categoria.get_url() == expected_url