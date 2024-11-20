from django.urls import path
from .views import VentaAPIView , VentaDetails, VentaEstadoUpdateAPIView

app_name = 'venta'

urlpatterns = [
    path("", VentaAPIView.as_view(), name="venta"),
    path('<int:pk>/', VentaDetails.as_view()),
    path('<int:pk>/estado/', VentaEstadoUpdateAPIView.as_view(), name="venta_estado_update"),
]