from django.urls import path
from .views import EstadodeCitaAPIView, EstadodeCitaDetails

app_name = "Estados_de_Cita"

urlpatterns = [
    path("", EstadodeCitaAPIView.as_view(), name="Estados_de_Cita"),
    path('<int:pk>/', EstadodeCitaDetails.as_view())
]