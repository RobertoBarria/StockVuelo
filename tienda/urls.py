from django.urls import path
from . import views

urlpatterns = [
    path('', views.tienda, name='tienda'),
    path('categoria/<slug:categoria_slug>/', views.tienda, name='productos_por_categoria'),
    path('categoria/<slug:categoria_slug>/producto/<slug:producto_slug>/', views.producto_detalle, name='producto_detalle'),
    path('producto/<int:producto_id>/agregar/', views.agregar_a_orden, name='agregar_a_orden'),
    path('orden/<int:orden_id>/', views.orden_detalle, name='orden_detalle'),
    path('orden_producto/<int:orden_producto_id>/actualizar/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('orden_producto/<int:orden_producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('orden/<int:orden_id>/cerrar/', views.cerrar_orden, name='cerrar_orden'),
    path('orden/<int:orden_id>/cancelar/', views.cancelar_orden, name='cancelar_orden'),
    path('crear_orden/', views.crear_orden, name='crear_orden'),
    path('mis_ordenes/', views.listar_ordenes, name='listar_ordenes'),
    
]