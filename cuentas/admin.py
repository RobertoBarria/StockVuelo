from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cuenta
#from .models import PerfilUsuario
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'Nombre','Apellido','username','last_login','date_joined','is_active')
    list_display_link = ('email', 'Nombre','Apellido')
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets =  ()
    
                      
admin.site.register(Cuenta,AccountAdmin)
