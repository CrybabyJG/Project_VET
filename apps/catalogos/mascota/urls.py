from django.urls import path
from .views import MascotaAPIView, MascotaDetails

app_name = "Mascota"

urlpatterns = [
    path("", MascotaAPIView.as_view(), name="Mascota"),
    path('<int:pk>/', MascotaDetails.as_view())
]