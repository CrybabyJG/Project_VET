from django.urls import path
from .views import CitaAPIView, CitaDetails, CitaEstadoUpdateAPIView

app_name = 'cita'

urlpatterns = [
    path("", CitaAPIView.as_view(), name="cita"),
    path("<int:pk>/", CitaDetails.as_view()),
    path("<int:pk>/estado/", CitaEstadoUpdateAPIView.as_view(), name="cita_estado_update"),
]