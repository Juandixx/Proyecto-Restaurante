from django.urls import path
from . import views

urlpatterns = [

    path('', views.iniciar_sesion, name='login'),

    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('logout/', views.cerrar_sesion, name='logout'),

    path('productos/', views.lista_productos, name='productos'),

    path(
        'crear-producto/',
        views.crear_producto,
        name='crear_producto'
    ),

    path(
        'editar-producto/<int:producto_id>/',
        views.editar_producto,
        name='editar_producto'
    ),

    path(
        'eliminar-producto/<int:producto_id>/',
        views.eliminar_producto,
        name='eliminar_producto'
    ),

    path(
        'gestionar-roles/',
        views.gestionar_roles,
        name='gestionar_roles'
    ),

    path(
        'cambiar-rol/<int:user_id>/',
        views.cambiar_rol,
        name='cambiar_rol'
    ),

    path(
        'eliminar-usuario/<int:user_id>/',
        views.eliminar_usuario,
        name='eliminar_usuario'
    ),

    path(
    'categorias/',
    views.lista_categorias,
    name='categorias'
    ),

    path(
        'crear-categoria/',
        views.crear_categoria,
        name='crear_categoria'
    ),

    path(
        'editar-categoria/<int:categoria_id>/',
        views.editar_categoria,
        name='editar_categoria'
    ),

    path(
        'eliminar-categoria/<int:categoria_id>/',
        views.eliminar_categoria,
        name='eliminar_categoria'
    ),

    path(
    'proveedores/',
    views.lista_proveedores,
    name='proveedores'
    ),

    path(
        'crear-proveedor/',
        views.crear_proveedor,
        name='crear_proveedor'
    ),

    path(
        'editar-proveedor/<int:proveedor_id>/',
        views.editar_proveedor,
        name='editar_proveedor'
    ),

    path(
        'eliminar-proveedor/<int:proveedor_id>/',
        views.eliminar_proveedor,
        name='eliminar_proveedor'
    ),

    path(
        'registrar-salida/',
        views.registrar_salida,
        name='registrar_salida'
    ),

    path(
        'registrar-entrada/',
        views.registrar_entrada,
        name='registrar_entrada'
    ),

    path(
        'salidas/',
        views.lista_salidas,
        name='salidas'
    ),

    path(
        'entradas/',
        views.lista_entradas,
        name='entradas'
    ),

    path(
        'editar-entrada/<int:entrada_id>/',
        views.editar_entrada,
        name='editar_entrada'
    ),

    path(
        'editar-salida/<int:salida_id>/',
        views.editar_salida,
        name='editar_salida'
    ),

]