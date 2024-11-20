from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MedicamentoSerializer, DetalleMedicamentoSerializer
from .models import Medicamento, DetalleMedicamento, Presentacion, UnidadMedida
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from ...movimientos.cita.models import Cita
from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)


class MedicamentoAPIView(PaginationMixin,APIView):


    permission_classes = [IsAuthenticated, CustomPermission]
    model = Medicamento

    @swagger_auto_schema(responses={200: MedicamentoSerializer()})
    def get(self, request):

        logger.info("Peticion GET para listar todos los medicamentos")
        medicamento = Medicamento.objects.all().order_by('ID_Medicamento')
        page = self.paginate_queryset(medicamento, request)

        if page is not None:
            serializer = MedicamentoSerializer(page, many=True)
            logger.info("Respuesta paginada para medicamento")
            return self.get_paginated_response(serializer.data)

        serializer = MedicamentoSerializer(medicamento, many=True)
        logger.error("Mostrando todas los medicamentos sin paginacion")
        return Response(serializer.data)


    @swagger_auto_schema(request_body=MedicamentoSerializer)
    def post(self, request):
        # Inicializa el serializer con los datos del request
        logger.info("Peticicion POST para crear una nuevo medicamento")
        serializer = MedicamentoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Inicia una transacción atómica
                with transaction.atomic():
                    # Obtiene la presentacion y unidad de medida usando el ID proporcionado en los datos validados
                    presentacion = get_object_or_404(Presentacion, pk=serializer.validated_data['ID_Presentacion'].ID_Presentacion)
                    unidadmedida = get_object_or_404(UnidadMedida, pk=serializer.validated_data['ID_Unidad_Medida'].ID_Unidad_Medida)
                    # Crea la instancia de medicamento
                    medicamento = Medicamento.objects.create(
                        Codigo_Medicamento=serializer.validated_data['Codigo_Medicamento'],
                        Nombre_Medicamento=serializer.validated_data['Nombre_Medicamento'],
                        Precio=serializer.validated_data['Precio'],
                        ID_Presentacion=presentacion,
                        ID_Unidad_Medida=unidadmedida
                    )
                    # Procesa cada detalle en los datos validados
                    for detalle_data in serializer.validated_data['detalles']:
                        cantidad = detalle_data['Cantidad']
                        descripcion = detalle_data['Descripcion']
                        # Obtieneel medicamento relacionado o devuelve 404 si no existe
                        cita = get_object_or_404(Cita, pk=detalle_data['ID_Cita'].ID_Cita)
                        # Crea el detalle del medicamento con la información relevante
                        DetalleMedicamento.objects.create(
                            ID_Medicamento=medicamento,
                            ID_Cita=cita,
                            Cantidad=cantidad,
                            Descripcion=descripcion
                        )
                # Serializa el medicamento con los detalles incluidos para la respuesta
                medicamento_serializer = MedicamentoSerializer(medicamento)
                logger.info("Medicamento creado exitosamente")
                return Response(medicamento_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Devuelve un error en caso de excepción
                logger.error("No se pudo crear el medicamento: %s", serializer.errors)
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Devuelve errores de validación si los datos no son válidos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Medicamento_details(APIView):

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Medicamento

    @swagger_auto_schema(responses={200: MedicamentoSerializer()})
    def get(self, request, pk):
        # Obtiene el medicamento por ID
        medicamento = get_object_or_404(Medicamento, pk=pk)
        serializer = MedicamentoSerializer(medicamento)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk=None):
        # Busca el medicamento específico por su ID
        medicamento = get_object_or_404(Medicamento, pk=pk)
        logger.info("Solicitud DELETE para eliminar un medicamento con ID: %s", pk)
        try:
            # Usa una transacción para asegurar que la eliminación sea atómica
            with transaction.atomic():
                self.check_object_permissions(request, medicamento) #Verificación de permisos
                # Elimina primero los detalles relacionados
                DetalleMedicamento.objects.filter(ID_Medicamento=medicamento).delete()
                # Luego, elimina el medicamento
                medicamento.delete()
                logger.info("Medicamento eliminado exitosamente con ID: %s", pk)

            return Response({"message": "Medicamento eliminada con éxito."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            # Devuelve un error detallado en caso de falla
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
