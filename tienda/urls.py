from django.urls import path
from . import views

urlpatterns = [
    path('',views.tienda, name="tienda"),
    path('<slug:categoria_slug>/', views.tienda, name='productos_por_categoria'),
    path('tienda/<slug:categoria_slug>/<slug:producto_slug>/', views.producto_detalle, name='producto_detalle'),
]




    