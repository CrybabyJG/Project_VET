from django.urls import path, include

urlpatterns = [
    path('enfermedades/', include('apps.catalogos.enfermedades.urls')),
    path('estado_compra/', include('apps.catalogos.estado_compra.urls')),
    path('estado_de_cita/', include('apps.catalogos.estado_de_cita.urls')),
    path('estado_venta/', include('apps.catalogos.estado_venta.urls')),
    path('mascota/', include('apps.catalogos.mascota.urls')),
    path('medicamento/', include('apps.catalogos.medicamento.urls')),
    path('presentacion/', include('apps.catalogos.presentacion.urls')),
    path('proveedor/', include('apps.catalogos.proveedor.urls')),
    path('raza/', include('apps.catalogos.raza.urls')),
    path('tipo_mascota/', include('apps.catalogos.tipo_mascota.urls')),
    path('unidad_medida/', include('apps.catalogos.unidad_medida.urls')),
]