from django.contrib import admin
from .models import Avion

class AvionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

admin.site.register(Avion, AvionAdmin)






