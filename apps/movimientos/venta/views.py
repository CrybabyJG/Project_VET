from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VentaSerializer, DetalleVentaSerializer, UpdateEstadoVentaSerializer
from .models import Venta, DetalleVenta, Clientes, Medicamento
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from ...catalogos.estado_venta.models import EstadodeVenta
from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class VentaAPIView(PaginationMixin,APIView):

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Venta

    @swagger_auto_schema(responses={200: VentaSerializer()})
    def get(self, request):
        logger.info("Peticion GET para listar todas las ventas")
        venta = Venta.objects.all().order_by('ID_Venta')
        page = self.paginate_queryset(venta, request)

        if page is not None:
            serializer = VentaSerializer(page, many=True)
            logger.info("Respuesta paginada para venta")
            return self.get_paginated_response(serializer.data)

        serializer = VentaSerializer(venta, many=True)
        logger.error("Mostrando todas las ventas sin paginacion")
        return Response(serializer.data)


    @swagger_auto_schema(request_body=VentaSerializer)
    def post(self, request):
        # Inicializa el serializer con los datos del request
        logger.info("Peticicion POST para crear una nueva venta")
        serializer = VentaSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Inicia una transacción atómica
                with transaction.atomic():
                    # Obtiene el cliente usando el ID proporcionado en los datos validados
                    cliente = get_object_or_404(Clientes, pk=serializer.validated_data['ID_Cliente'].ID_Cliente)
                    estadoventa = get_object_or_404(EstadodeVenta, pk=serializer.validated_data['ID_EstadoVenta'].ID_EstadoVenta)
                    # Crea la instancia de Venta
                    venta = Venta.objects.create(
                        Codigo_Venta=serializer.validated_data['Codigo_Venta'],
                        ID_Cliente=cliente,
                        Descripcion=serializer.validated_data['Descripcion'],
                        ID_EstadoVenta=estadoventa
                    )

                    # Procesa cada detalle en los datos validados
                    for detalle_data in serializer.validated_data['detalles']:
                        cantidad = detalle_data['Cantidad']
                        # Obtiene el medicamento relacionado o devuelve 404 si no existe
                        medicamento = get_object_or_404(Medicamento, pk=detalle_data['ID_Medicamento'].ID_Medicamento)
                        preciototal = medicamento.Precio * cantidad
                        # Crea el detalle de la venta con la información relevante
                        DetalleVenta.objects.create(
                            ID_Venta=venta,
                            ID_Medicamento=medicamento,
                            Cantidad=cantidad,
                            Precio=preciototal  # Asigna el precio del medicamento actual
                        )

                # Serializa la venta con los detalles incluidos para la respuesta
                venta_serializer = VentaSerializer(venta)
                logger.info("Venta creada exitosamente")
                return Response(venta_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Devuelve un error en caso de excepción
                logger.error("No se pudo crear la venta: %s", serializer.errors)
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Devuelve errores de validación si los datos no son válidos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VentaDetails(APIView):

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Venta

    @swagger_auto_schema(responses={200: VentaSerializer()})
    def get(self, request, pk):
        # Obtiene la venta por ID
        venta = get_object_or_404(Venta, pk=pk)
        serializer = VentaSerializer(venta)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VentaEstadoUpdateAPIView(APIView):
    @swagger_auto_schema(
        request_body=UpdateEstadoVentaSerializer,
        responses={200: "Estado de venta actualizado con éxito.", 404: "Venta o EstadoVenta no encontrado.",
                   400: "Datos inválidos."}
    )
    def patch(self, request, pk):
        logger.info("Solicitud PATCH para actualizar parcialmente el estado de la venta ID: %s", pk)
        serializer = UpdateEstadoVentaSerializer(data=request.data)
        if serializer.is_valid():
            venta = get_object_or_404(Venta, pk=pk)
            estado_venta = get_object_or_404(EstadodeVenta, pk=serializer.validated_data['ID_EstadoVenta'])
            venta.ID_EstadoCompra = estado_venta
            venta.save()
            logger.info("Estado de venta parcialmente actualizado exitosamente con ID: %s", pk)
            return Response({"message": "Estado de venta actualizado con éxito."}, status=status.HTTP_200_OK)
        logger.error("No se pudo actualizar el estado de la venta: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
        def delete(self, request, pk=None):
            # Busca la venta específica por su ID
            venta = get_object_or_404(Venta, pk=pk)

            try:
                # Usa una transacción para asegurar que la eliminación sea atómica
                with transaction.atomic():
                    #self.check_object_permissions(request, cita) #Verificación de permisos
                    # Elimina primero los detalles relacionados
                    DetalleVenta.objects.filter(ID_Venta=venta).delete()

                    # Luego, elimina la venta
                    venta.delete()

                return Response({"message": "Venta eliminada con éxito."}, status=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                # Devuelve un error detallado en caso de falla
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        """