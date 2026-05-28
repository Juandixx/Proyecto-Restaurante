from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, STOCK_MINIMO_GLOBAL
from .forms import ProductoForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Usuario
from .forms import RegistroForm
from .models import Categoria
from .forms import CategoriaForm
from .models import Proveedor
from .forms import ProveedorForm
from .models import SalidaProducto
from .forms import SalidaProductoForm
from .models import EntradaProducto
from .forms import EntradaProductoForm
from .forms import LoginForm



# =========================
# INICIO
# =========================

def inicio(request):

    return render(request, 'modulo/index.html')


# =========================
# LISTA PRODUCTOS
# =========================

def lista_productos(request):

    productos = Producto.objects.all()

    return render(
        request,
        'modulo/lista_productos.html',
        {
            'productos': productos
        }
    )


def crear_producto(request):

    if request.method == 'POST':

        formulario = ProductoForm(request.POST)

        if formulario.is_valid():

            formulario.save()

            return redirect('productos')

    else:

        formulario = ProductoForm()

    return render(
        request,
        'modulo/crear_producto.html',
        {
            'formulario': formulario
        }
    )

@login_required
def editar_producto(request, producto_id):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    producto = Producto.objects.get(id=producto_id)

    if request.method == 'POST':

        formulario = ProductoForm(
            request.POST,
            instance=producto
        )

        if formulario.is_valid():

            formulario.save()

            return redirect('productos')

    else:

        formulario = ProductoForm(instance=producto)

    return render(

        request,

        'modulo/editar_producto.html',

        {
            'formulario': formulario
        }

    )


@login_required
def eliminar_producto(request, producto_id):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    producto = Producto.objects.get(id=producto_id)

    producto.delete()

    return redirect('productos')


# =========================
# CREAR USUARIO
# =========================
def crear_usuario(request):

    if request.method == 'POST':

        formulario = RegistroForm(request.POST)

        if formulario.is_valid():

            user = formulario.save()

            Usuario.objects.create(
                user=user,
                rol='empleado'
            )

            return redirect('gestionar_roles')

    else:

        formulario = RegistroForm()

    return render(request, 'modulo/crear_usuario.html', {
        'formulario': formulario
    })


# =========================
# LOGIN
# =========================

def iniciar_sesion(request):

    if request.method == 'POST':

        formulario = LoginForm(

            request,

            data=request.POST

        )

        if formulario.is_valid():

            usuario = formulario.get_user()

            login(request, usuario)

            return redirect('dashboard')

    else:

        formulario = LoginForm()

    return render(

        request,

        'modulo/login.html',

        {
            'formulario': formulario
        }

    )


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):

    usuario = request.user.usuario

    productos_stock_bajo = Producto.objects.filter(
        stock_actual__lte=STOCK_MINIMO_GLOBAL
    )

    contexto = {

        'productos_stock_bajo': productos_stock_bajo

    }

    if usuario.rol == 'admin':

        return render(
            request,
            'modulo/dashboard_admin.html',
            contexto
        )

    return render(
        request,
        'modulo/dashboard_empleado.html',
        contexto
    )


# =========================
# LOGOUT
# =========================

def cerrar_sesion(request):

    logout(request)

    return redirect('login')

# =========================
# GESTIONAR ROLES
# =========================

@login_required
def gestionar_roles(request):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    usuarios = User.objects.all()

    return render(

        request,

        'modulo/gestionar_roles.html',

        {
            'usuarios': usuarios
        }

    )


@login_required
def cambiar_rol(request, user_id):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    usuario = User.objects.get(id=user_id)

    if usuario.username == 'admin':

        return redirect('gestionar_roles')

    if usuario == request.user:

        return redirect('gestionar_roles')

    perfil = usuario.usuario

    if perfil.rol == 'admin':

        perfil.rol = 'empleado'

    else:

        perfil.rol = 'admin'

    perfil.save()

    return redirect('gestionar_roles')


@login_required
def eliminar_usuario(request, user_id):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    usuario = User.objects.get(id=user_id)

    if usuario.username == 'admin':

        return redirect('gestionar_roles')

    if usuario == request.user:

        return redirect('gestionar_roles')

    usuario.delete()

    return redirect('gestionar_roles')


# =========================
# LISTAR CATEGORIAS
# =========================

@login_required
def lista_categorias(request):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    categorias = Categoria.objects.all()

    return render(

        request,

        'modulo/lista_categorias.html',

        {
            'categorias': categorias
        }

    )

@login_required
def crear_categoria(request):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    if request.method == 'POST':

        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():

            formulario.save()

            return redirect('categorias')

    else:

        formulario = CategoriaForm()

    return render(

        request,

        'modulo/crear_categoria.html',

        {
            'formulario': formulario
        }

    )

@login_required
def editar_categoria(request, categoria_id):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    categoria = Categoria.objects.get(id=categoria_id)

    if request.method == 'POST':

        formulario = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if formulario.is_valid():

            formulario.save()

            return redirect('categorias')

    else:

        formulario = CategoriaForm(instance=categoria)

    return render(

        request,

        'modulo/editar_categoria.html',

        {
            'formulario': formulario
        }

    )


@login_required
def eliminar_categoria(request, categoria_id):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    categoria = Categoria.objects.get(id=categoria_id)

    categoria.delete()

    return redirect('categorias')

# =========================
# LISTA PROVEEDORES
# =========================

@login_required
def lista_proveedores(request):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    proveedores = Proveedor.objects.all()

    return render(

        request,

        'modulo/lista_proveedores.html',

        {
            'proveedores': proveedores
        }

    )


@login_required
def crear_proveedor(request):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    if request.method == 'POST':

        formulario = ProveedorForm(request.POST)

        if formulario.is_valid():

            formulario.save()

            return redirect('proveedores')

    else:

        formulario = ProveedorForm()

    return render(

        request,

        'modulo/crear_proveedor.html',

        {
            'formulario': formulario
        }

    )


@login_required
def editar_proveedor(request, proveedor_id):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    proveedor = Proveedor.objects.get(id=proveedor_id)

    if request.method == 'POST':

        formulario = ProveedorForm(
            request.POST,
            instance=proveedor
        )

        if formulario.is_valid():

            formulario.save()

            return redirect('proveedores')

    else:

        formulario = ProveedorForm(instance=proveedor)

    return render(

        request,

        'modulo/editar_proveedor.html',

        {
            'formulario': formulario
        }

    )


@login_required
def eliminar_proveedor(request, proveedor_id):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    proveedor = Proveedor.objects.get(id=proveedor_id)

    proveedor.delete()

    return redirect('proveedores')

# =========================
# REGISTRAR SALIDA
# =========================

@login_required
def registrar_salida(request):

    if request.user.usuario.rol not in ['admin', 'empleado']:

        return redirect('dashboard')

    if request.method == 'POST':

        formulario = SalidaProductoForm(request.POST)

        if formulario.is_valid():

            salida = formulario.save(commit=False)

            salida.usuario = request.user

            salida.save()

            return redirect('salidas')

    else:

        formulario = SalidaProductoForm()

    return render(

        request,

        'modulo/registrar_salida.html',

        {
            'formulario': formulario
        }

    )

@login_required
def editar_salida(request, salida_id):

    if request.user.usuario.rol not in ['admin', 'empleado']:
        return redirect('dashboard')

    salida = get_object_or_404(
        SalidaProducto,
        id=salida_id
    )

    if request.method == 'POST':

        formulario = SalidaProductoForm(
            request.POST,
            instance=salida
        )

        if formulario.is_valid():
            formulario.save()
            return redirect('salidas')

    else:
        formulario = SalidaProductoForm(
            instance=salida
        )

    return render(
        request,
        'modulo/editar_salida.html',
        {
            'formulario': formulario
        }
    )


@login_required
def lista_salidas(request):

    if request.user.usuario.rol not in ['admin', 'empleado']:

        return redirect('dashboard')

    salidas = SalidaProducto.objects.all().order_by('-fecha')

    return render(

        request,

        'modulo/lista_salidas.html',

        {
            'salidas': salidas
        }

    )

# =========================
# REGISTRAR ENTRADA
# =========================

@login_required
def registrar_entrada(request):

    if request.user.usuario.rol != 'admin':
        return redirect('dashboard')

    if request.method == 'POST':

        formulario = EntradaProductoForm(request.POST)

        if formulario.is_valid():

            entrada = formulario.save(commit=False)
            entrada.usuario = request.user
            entrada.save()

            return redirect('entradas')

    else:
        formulario = EntradaProductoForm()

    return render(
        request,
        'modulo/registrar_entrada.html',
        {
            'formulario': formulario
        }
    )

@login_required
def editar_entrada(request, entrada_id):

    if request.user.usuario.rol != 'admin':
        return redirect('dashboard')

    entrada = get_object_or_404(
        EntradaProducto,
        id=entrada_id
    )

    if request.method == 'POST':

        formulario = EntradaProductoForm(
            request.POST,
            instance=entrada
        )

        if formulario.is_valid():
            formulario.save()
            return redirect('entradas')

    else:
        formulario = EntradaProductoForm(
            instance=entrada
        )

    return render(
        request,
        'modulo/editar_entrada.html',
        {
            'formulario': formulario
        }
    )


@login_required
def lista_entradas(request):

    if request.user.usuario.rol != 'admin':

        return redirect('dashboard')

    entradas = EntradaProducto.objects.all().order_by('-fecha')

    return render(

        request,

        'modulo/lista_entradas.html',

        {
            'entradas': entradas
        }

    )

