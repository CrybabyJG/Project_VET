from django.urls import path
from .views import RazaAPIView, RazaDetails

app_name = "Raza"

urlpatterns = [
    path("", RazaAPIView.as_view(), name="Raza"),
    path('<int:pk>/', RazaDetails.as_view())
]