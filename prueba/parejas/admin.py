from django.contrib import admin
from .models import Pareja, MiembroPareja, Seccion, Archivo, Nota


@admin.register(Pareja)
class ParejaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'creador', 'clave_union', 'fecha_creacion')
    search_fields = ('codigo', 'creador__username')


@admin.register(MiembroPareja)
class MiembroParejaAdmin(admin.ModelAdmin):
    list_display = ('pareja', 'usuario', 'fecha_union')
    search_fields = ('pareja__codigo', 'usuario__username')


@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pareja', 'creado_por', 'fecha_creacion')
    search_fields = ('nombre', 'pareja__codigo')


@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'pareja', 'usuario', 'seccion', 'favorito', 'fecha_subida')
    search_fields = ('tipo', 'pareja__codigo', 'usuario__username')


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('pareja', 'autor', 'fecha')
    search_fields = ('pareja__codigo', 'autor__username')