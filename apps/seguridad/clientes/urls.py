from django.urls import path
from .views import ClientesAPIView, ClientesDetails

app_name = "Clientes"

urlpatterns = [
    path("", ClientesAPIView.as_view(), name="Raza"),
    path('<int:pk>/', ClientesDetails.as_view())
]