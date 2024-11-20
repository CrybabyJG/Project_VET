from django.urls import path
from .views import EnfermedadesAPIView, EnfermedadesDetails

app_name = "enfermedades"

urlpatterns = [
    path("", EnfermedadesAPIView.as_view(), name="enfermedades"),
    path('<int:pk>/', EnfermedadesDetails.as_view())
]