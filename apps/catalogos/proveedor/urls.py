from django.urls import path
from .views import ProveedorAPIView, ProveedorDetails

app_name = "Proveedor"

urlpatterns = [
    path("", ProveedorAPIView.as_view(), name="Mascota"),
    path('<int:pk>/', ProveedorDetails.as_view())
]