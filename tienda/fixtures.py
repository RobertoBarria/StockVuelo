
from tienda.models import Producto

def create_producto():
    return Producto.objects.create(
        nombre_producto='Producto de prueba',
        slug='producto-de-prueba',
        descripcion='Descripción de prueba',
        precio=100,
        imagen='test.jpg',
        categoria="snack"  
    )