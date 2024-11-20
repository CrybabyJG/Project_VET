from django.urls import path
from .views import CompraAPIView, CompraDetails, CompraEstadoUpdateAPIView

app_name = 'compra'

urlpatterns = [
    path("", CompraAPIView.as_view(), name="compra"),
    path("<int:pk>/", CompraDetails.as_view()),
    path("<int:pk>/estado/", CompraEstadoUpdateAPIView.as_view(), name="compra_estado_update"),
]