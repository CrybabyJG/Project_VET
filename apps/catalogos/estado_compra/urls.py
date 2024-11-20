from django.urls import path
from .views import EstadodeCompraAPIView,EstadodeCompraDetails

app_name = "Estados_de_Compra"

urlpatterns = [
    path("", EstadodeCompraAPIView.as_view(), name="Estados_de_Compra"),
    path('<int:pk>/', EstadodeCompraDetails.as_view())
]