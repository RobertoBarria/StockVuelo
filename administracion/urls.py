from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.administracion, name='administracion'),
    

    
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    
    path('aviones/', views.lista_aviones, name='lista_aviones'),
    path('aviones/crear/', views.crear_avion, name='crear_avion'),
    path('aviones/<int:pk>/editar/', views.editar_avion, name='editar_avion'),
    path('aviones/<int:pk>/eliminar/', views.eliminar_avion, name='eliminar_avion'),
    
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    

    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/<int:producto_id>/asignar-stock/', views.asignar_stock, name='asignar_stock'),
    path('productos/movimiento/<int:producto_id>/', views.movimiento_producto, name='movimiento_producto'),    
    
    path('productos/movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('obtener_stock_origen/', views.obtener_stock_origen, name='obtener_stock_origen'),
    
]


