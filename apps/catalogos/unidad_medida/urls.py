from django.urls import path
from .views import UnidadMedidaAPIView, UnidadMedidaDetails

app_name = "Unidad_Medida"

urlpatterns = [
    path("", UnidadMedidaAPIView.as_view(), name="Unidad_Medida"),
    path('<int:pk>/', UnidadMedidaDetails.as_view())
]