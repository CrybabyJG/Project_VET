from django.urls import path, include

urlpatterns = [
    path('clientes/', include('apps.seguridad.clientes.urls')),
    path('usuarios/', include('apps.seguridad.usuarios.urls')),
]