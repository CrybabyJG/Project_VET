from django.urls import path, include

urlpatterns = [
    path('cita/', include('apps.movimientos.cita.urls')),
    path('compra/', include('apps.movimientos.compra.urls')),
    path('venta/', include('apps.movimientos.venta.urls')),
]