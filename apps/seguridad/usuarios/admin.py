from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin


from apps.seguridad.usuarios.models import Usuarios
@admin.register(Usuarios)
class UsuariosAdmin(UserAdmin):
    pass