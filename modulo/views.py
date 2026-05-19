from django.shortcuts import render, redirect

from .models import Producto
from .forms import ProductoForm


def inicio(request):

    return render(request, 'index.html')


def lista_productos(request):

    productos = Producto.objects.all()

    return render(
        request,
        'productos/lista_productos.html',
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
        'productos/crear_producto.html',
        {
            'formulario': formulario
        }
    )