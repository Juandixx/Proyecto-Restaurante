from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum


STOCK_MINIMO_GLOBAL = 10


# =========================
# PERFIL / ROLES
# =========================

class Usuario(models.Model):

    ROLES = (

        ('admin', 'Administrador'),

        ('empleado', 'Empleado'),

    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='usuario'
        
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='empleado'
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username

    class Meta:

        verbose_name = "Usuario"

        verbose_name_plural = "Usuarios"

# =========================
# CATEGORIA
# =========================

class Categoria(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):

        return self.nombre

    class Meta:

        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


# =========================
# PRODUCTO
# =========================

class Producto(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_actual = models.IntegerField(
        default=0
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    def __str__(self):

        return self.nombre

    @property
    def stock_bajo(self):

        return self.stock_actual <= STOCK_MINIMO_GLOBAL

    class Meta:

        verbose_name = "Producto"
        verbose_name_plural = "Productos"


# =========================
# PROVEEDOR
# =========================

class Proveedor(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    contacto = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    direccion = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    def __str__(self):

        return self.nombre

    class Meta:

        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


# =========================
# ORDEN DE COMPRA
# =========================

class OrdenCompra(models.Model):

    ESTADOS = (

        ('pendiente', 'Pendiente'),

        ('recibido', 'Recibido'),

        ('cancelado', 'Cancelado'),

    )

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):

        return f"Orden #{self.id}"

    class Meta:

        verbose_name = "Orden de Compra"
        verbose_name_plural = "Ordenes de Compra"


# =========================
# ENTRADA DE PRODUCTO
# =========================

class EntradaProducto(models.Model):

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    cantidad = models.IntegerField()

    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def actualizar_stock_producto(self, producto):
        total_entradas = EntradaProducto.objects.filter(
            producto=producto
        ).aggregate(
            total=Sum('cantidad')
        )['total'] or 0

        total_salidas = SalidaProducto.objects.filter(
            producto=producto
        ).aggregate(
            total=Sum('cantidad')
        )['total'] or 0

        producto.stock_actual = total_entradas - total_salidas
        producto.save()

    def save(self, *args, **kwargs):

        producto_anterior = None

        if self.pk:
            anterior = EntradaProducto.objects.get(pk=self.pk)
            producto_anterior = anterior.producto

        super().save(*args, **kwargs)

        # recalcula producto actual
        self.actualizar_stock_producto(self.producto)

        # si cambió de producto, recalcular el viejo también
        if producto_anterior and producto_anterior != self.producto:
            self.actualizar_stock_producto(producto_anterior)

    def delete(self, *args, **kwargs):

        producto = self.producto

        super().delete(*args, **kwargs)

        self.actualizar_stock_producto(producto)

    def __str__(self):
        return f"Entrada - {self.producto.nombre}"

    class Meta:
        verbose_name = "Entrada de Producto"
        verbose_name_plural = "Entradas de Productos"
        
# =========================
# SALIDA DE PRODUCTO
# =========================

class SalidaProducto(models.Model):

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    cantidad = models.IntegerField()

    motivo = models.CharField(
        max_length=255
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def actualizar_stock_producto(self, producto):

        total_entradas = EntradaProducto.objects.filter(
            producto=producto
        ).aggregate(
            total=Sum('cantidad')
        )['total'] or 0

        total_salidas = SalidaProducto.objects.filter(
            producto=producto
        ).aggregate(
            total=Sum('cantidad')
        )['total'] or 0

        producto.stock_actual = total_entradas - total_salidas

        producto.save()

    def clean(self):

        total_entradas = EntradaProducto.objects.filter(
            producto=self.producto
        ).aggregate(
            total=Sum('cantidad')
        )['total'] or 0

        total_salidas = SalidaProducto.objects.filter(
            producto=self.producto
        ).exclude(
            pk=self.pk
        ).aggregate(
            total=Sum('cantidad')
        )['total'] or 0

        stock_disponible = total_entradas - total_salidas

        if self.cantidad > stock_disponible:

            raise ValidationError(
                'No hay suficiente stock disponible.'
            )

    def save(self, *args, **kwargs):

        producto_anterior = None

        if self.pk:

            anterior = SalidaProducto.objects.get(pk=self.pk)

            producto_anterior = anterior.producto

        self.clean()

        super().save(*args, **kwargs)

        # recalcular producto actual
        self.actualizar_stock_producto(self.producto)

        # si cambió producto
        if producto_anterior and producto_anterior != self.producto:

            self.actualizar_stock_producto(producto_anterior)

    def delete(self, *args, **kwargs):

        producto = self.producto

        super().delete(*args, **kwargs)

        self.actualizar_stock_producto(producto)

    def __str__(self):

        return f"Salida - {self.producto.nombre}"

    class Meta:

        verbose_name = "Salida de Producto"

        verbose_name_plural = "Salidas de Productos"