from django.db import models
from django.urls import reverse


# Create your models here.
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=100, unique=True)
    cat_imagen = models.ImageField(upload_to='photos/categorias', blank=True, null=True)

    def get_url(self):
        return reverse('productos_por_categoria', args=[self.slug])

    def __str__(self):
        return self.nombre_categoria