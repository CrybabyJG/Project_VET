from django.urls import path
from .views import EstadodeVentaAPIView,EstadodeVentaDetails

app_name = "Estados_de_Venta"

urlpatterns = [
    path("", EstadodeVentaAPIView.as_view(), name="Estados_de_Venta"),
    path('<int:pk>/', EstadodeVentaDetails.as_view())
]