from django.urls import path
from .views import MedicamentoAPIView , Medicamento_details

app_name = 'medicamento'

urlpatterns = [
    path("", MedicamentoAPIView.as_view(), name="medicamento"),
    path('<int:pk>/', Medicamento_details.as_view())

]