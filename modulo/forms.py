from django import forms
from .models import Producto
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Categoria
from .models import Proveedor
from .models import SalidaProducto
from .models import EntradaProducto
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(UserCreationForm):

    class Meta:

        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

        widgets = {

            'username': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Nombre de usuario'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Correo electrónico'
            }),

        }

    email = forms.EmailField(

        widget=forms.EmailInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Correo electrónico'
        })

    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Nombre de usuario'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Contraseña'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Confirmar contraseña'
        }
        
)


class ProductoForm(forms.ModelForm):

    class Meta:

        model = Producto

        fields = [
            'nombre',
            'descripcion',
            'precio',
            'categoria'
        ]

        widgets = {

            'nombre': forms.TextInput(attrs={
                'class': 'auth-input'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'auth-input'
            }),

            'precio': forms.NumberInput(attrs={
                'class': 'auth-input'
            }),

            'categoria': forms.Select(attrs={
                'class': 'auth-input'
            }),

        }

class CategoriaForm(forms.ModelForm):

    class Meta:

        model = Categoria

        fields = [
            'nombre',
            'descripcion'
        ]

        widgets = {

            'nombre': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Nombre de la categoría'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'auth-input',
                'placeholder': 'Descripción'
            }),

        }

class ProveedorForm(forms.ModelForm):

    class Meta:

        model = Proveedor

        fields = [
            'nombre',
            'contacto',
            'telefono',
            'email',
            'direccion'
        ]

        widgets = {

            'nombre': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Nombre del proveedor'
            }),

            'contacto': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Persona de contacto'
            }),

            'telefono': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Teléfono'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Correo electrónico'
            }),

            'direccion': forms.Textarea(attrs={
                'class': 'auth-input',
                'placeholder': 'Dirección'
            }),

        }

class SalidaProductoForm(forms.ModelForm):

    class Meta:

        model = SalidaProducto

        fields = [
            'producto',
            'cantidad',
            'motivo',
            'observaciones'
        ]

        widgets = {

            'producto': forms.Select(attrs={
                'class': 'auth-input'
            }),

            'cantidad': forms.NumberInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Cantidad'
            }),

            'motivo': forms.TextInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Motivo de salida'
            }),

            'observaciones': forms.Textarea(attrs={
                'class': 'auth-input',
                'placeholder': 'Observaciones'
            }),

        }

class EntradaProductoForm(forms.ModelForm):

    class Meta:

        model = EntradaProducto

        fields = [
            'producto',
            'proveedor',
            'cantidad',
            'precio_compra'
        ]

        widgets = {

            'producto': forms.Select(attrs={
                'class': 'auth-input'
            }),

            'proveedor': forms.Select(attrs={
                'class': 'auth-input'
            }),

            'cantidad': forms.NumberInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Cantidad'
            }),

            'precio_compra': forms.NumberInput(attrs={
                'class': 'auth-input',
                'placeholder': 'Precio de compra'
            }),

        }

class LoginForm(AuthenticationForm):

    username = forms.CharField(

        widget=forms.TextInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Usuario'
        })

    )

    password = forms.CharField(

        widget=forms.PasswordInput(attrs={
            'class': 'auth-input',
            'placeholder': 'Contraseña'
        })

    )