from django import forms
from categorias.models import Categoria
from aviones.models import Avion
from cuentas.models import Cuenta
from tienda.models import Producto, StockAvion



class StockAvionForm(forms.ModelForm):
    class Meta:
        model = StockAvion
        fields = ['cantidad_disponible', 'cantidad_Minima']
        widgets = {
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_Minima': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, avion, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.avion = avion

    def save(self, producto):
        instance = super().save(commit=False)
        instance.avion = self.avion
        instance.producto = producto
        instance.save()

class MovimientoProductoForm(forms.Form):
    producto = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='Producto')
    avion_origen = forms.ModelChoiceField(queryset=Avion.objects.all(), label='Avión de origen')
    stock_origen = forms.IntegerField(label='Stock Origen', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    avion_destino = forms.ModelChoiceField(queryset=Avion.objects.all(), label='Avión de destino')
    cantidad = forms.IntegerField(label='Cantidad')

    def __init__(self, *args, **kwargs):
        producto = kwargs.pop('producto', None)
        super(MovimientoProductoForm, self).__init__(*args, **kwargs)
        if producto:
            self.fields['producto'].initial = producto.nombre_producto
            self.fields['stock_origen'].initial = 0  # Valor por defecto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'descripcion', 'precio', 'imagen', 'categoria']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre_categoria','slug', 'descripcion', 'cat_imagen']
        
class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ['nombre', 'descripcion']
        


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese Password',
        'class': 'form-control',
    }))
    
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar Password',
        'class': 'form-control',
    }))

    class Meta:
        model = Cuenta
        fields = ['Nombre', 'Apellido', 'phone_number', 'email', 'password', 'avion', 'es_administrador', 'es_tripulante']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        if password != confirmar_password:
            raise forms.ValidationError("El password no coincide!")
        
        return cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['Nombre', 'Apellido', 'phone_number', 'email', 'avion', 'es_administrador', 'es_tripulante']