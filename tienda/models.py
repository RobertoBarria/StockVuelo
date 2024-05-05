from django.db import models
from categorias.models import Categoria
from django.urls import reverse



class Avion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


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

    class Meta:
        unique_together = ('producto', 'avion')  # Garantiza que no haya duplicados