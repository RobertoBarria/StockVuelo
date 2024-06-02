from django.contrib import admin
from .models import Producto,  StockAvion

class StockAvionInline(admin.TabularInline):
    model = StockAvion
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio', 'get_categoria', 'fecha_modificacion', 'is_available')
    prepopulated_fields = {'slug': ('nombre_producto',)}
    inlines = [StockAvionInline]  # Agrega el administrador en línea de StockAvion

    def get_categoria(self, obj):
        return obj.categoria.nombre_categoria  # Ajusta 'nombre_categoria' al nombre correcto del campo en tu modelo Categoria
    get_categoria.short_description = 'Categoría'


