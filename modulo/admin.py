from django.contrib import admin

from .models import (
    Usuario,
    Categoria,
    Producto,
    Proveedor,
    OrdenCompra,
    EntradaProducto,
    SalidaProducto
)

admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(OrdenCompra)
admin.site.register(EntradaProducto)
admin.site.register(SalidaProducto)