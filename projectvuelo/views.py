from django.http import HttpResponse
from django.shortcuts import render
from tienda.models import Producto	
from django.shortcuts import redirect

def home(request):
    return redirect('tienda')

#def home(request):
 #   productos = Producto.objects.all().filter(is_available=True)
 #   context ={
 #       'productos':productos,
 #   }
 #   return render(request,'home.html',context)
    




    