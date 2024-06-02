from django.db import models
from categorias.models import Categoria
from django.urls import reverse
from django.contrib.auth import get_user_model
from aviones.models import Avion

User = get_user_model()

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=500, blank=True)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='photos/productos')
    is_available = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('producto_detalle', args=[self.categoria.slug, self.slug])
    
    def __str__(self):
        return self.nombre_producto


class StockAvion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(default=0)
    cantidad_Minima = models.IntegerField(default=5)

    class Meta:
        unique_together = ('producto', 'avion')

    def __str__(self):
        return f"{self.avion} - {self.producto}"


class MovimientoProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    avion_origen = models.ForeignKey(Avion, related_name='movimientos_salida', on_delete=models.CASCADE)
    avion_destino = models.ForeignKey(Avion, related_name='movimientos_entrada', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cantidad} {self.producto.nombre_producto} de {self.avion_origen.nombre} a {self.avion_destino.nombre}"