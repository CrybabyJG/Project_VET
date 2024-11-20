from django.urls import path
from .views import PresentacionAPIView, PresentacionDetails

app_name = "Presentacion"

urlpatterns = [
    path("", PresentacionAPIView.as_view(), name="Presentacion"),
    path('<int:pk>/', PresentacionDetails.as_view())
]