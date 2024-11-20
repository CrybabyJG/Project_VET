from django.urls import path
from .views import TipoMascotaAPIView, TipoMascotaDetails

app_name = "Tipo_Mascota"

urlpatterns = [
    path("", TipoMascotaAPIView.as_view(), name="Tipo_Mascota"),
    path('<int:pk>/', TipoMascotaDetails.as_view())
]