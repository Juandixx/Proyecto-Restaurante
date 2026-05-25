from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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

    def save(self, *args, **kwargs):

        if not self.pk:

            self.producto.stock_actual += self.cantidad

            self.producto.save()

        super().save(*args, **kwargs)

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

    def clean(self):

        if self.cantidad > self.producto.stock_actual:

            raise ValidationError(
                'No hay suficiente stock disponible.'
            )

    def save(self, *args, **kwargs):

        self.clean()

        if not self.pk:

            self.producto.stock_actual -= self.cantidad

            self.producto.save()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"Salida - {self.producto.nombre}"

    class Meta:

        verbose_name = "Salida de Producto"
        verbose_name_plural = "Salidas de Productos"