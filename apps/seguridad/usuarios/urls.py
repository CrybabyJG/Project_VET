from django.urls import path
from .views import UsuariosAPIView, UsuariosDetails

urlpatterns = [
    path("", UsuariosAPIView.as_view(), name="usuarios"),
    path('<int:pk>/', UsuariosDetails.as_view())
]