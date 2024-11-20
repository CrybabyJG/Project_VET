from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CompraSerializer, UpdateEstadoCompraSerializer
from .models import Compra, DetalleCompra, Medicamento
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from ...catalogos.estado_compra.models import EstadodeCompra
from ...catalogos.proveedor.models import Proveedor
from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class CompraAPIView(PaginationMixin,APIView):

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Compra

    @swagger_auto_schema(responses={200: CompraSerializer()})
    def get(self, request):
        logger.info("Peticion GET para listar todas las compras")
        compra = Compra.objects.all().order_by('ID_Compra')
        page = self.paginate_queryset(compra, request)

        if page is not None:
            serializer = CompraSerializer(page, many=True)
            logger.info("Respuesta paginada para compra")
            return self.get_paginated_response(serializer.data)

        serializer = CompraSerializer(compra, many=True)
        logger.error("Mostrando todas las compras sin paginacion")
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=CompraSerializer)
    def post(self, request):
        # Inicializa el serializer con los datos del request
        logger.info("Peticicion POST para crear una nueva compra")
        serializer = CompraSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Inicia una transacción atómica
                with transaction.atomic():
                    # Obtiene el proveedor usando el ID proporcionado en los datos validados
                    proveedor = get_object_or_404(Proveedor, pk=serializer.validated_data['ID_Proveedor'].ID_Proveedor)
                    estadocompra = get_object_or_404(EstadodeCompra, pk=serializer.validated_data['ID_EstadoCompra'].ID_EstadoCompra)
                    # Crea la instancia de Venta
                    compra = Compra.objects.create(
                        Codigo_Compra=serializer.validated_data['Codigo_Compra'],
                        Descripcion=serializer.validated_data['Descripcion'],
                        ID_Proveedor=proveedor,
                        ID_EstadoCompra=estadocompra
                    )

                    # Procesa cada detalle en los datos validados
                    for detalle_data in serializer.validated_data['detalles']:
                        cantidad = detalle_data['Cantidad']
                        # Obtiene el medicamento relacionado o devuelve 404 si no existe
                        medicamento = get_object_or_404(Medicamento, pk=detalle_data['ID_Medicamento'].ID_Medicamento)
                        preciototal = medicamento.Precio * cantidad
                        # Crea el detalle de la venta con la información relevante
                        DetalleCompra.objects.create(
                            ID_Compra=compra,
                            ID_Medicamento=medicamento,
                            Cantidad=cantidad,
                            Precio=preciototal  # Asigna el precio del medicamento actual
                        )

                # Serializa la venta con los detalles incluidos para la respuesta
                compra_serializer = CompraSerializer(compra)
                logger.info("Compra creada exitosamente")
                return Response(compra_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Devuelve un error en caso de excepción
                logger.error("No se pudo crear la compra: %s", serializer.errors)
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Devuelve errores de validación si los datos no son válidos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompraDetails(APIView):

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Compra

    @swagger_auto_schema(responses={200: CompraSerializer()})
    def get(self, request, pk):
        # Obtiene la compra por ID
        compra = get_object_or_404(Compra, pk=pk)
        serializer = CompraSerializer(compra)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CompraEstadoUpdateAPIView(APIView):
    @swagger_auto_schema(
        request_body=UpdateEstadoCompraSerializer,
        responses={200: "Estado de compra actualizado con éxito.", 404: "Compra o EstadoCompra no encontrado.",
                   400: "Datos inválidos."}
    )
    def patch(self, request, pk):
        logger.info("Solicitud PATCH para actualizar parcialmente el estado de la compra ID: %s", pk)
        serializer = UpdateEstadoCompraSerializer(data=request.data)
        if serializer.is_valid():
            compra = get_object_or_404(Compra, pk=pk)
            estado_compra = get_object_or_404(EstadodeCompra, pk=serializer.validated_data['ID_EstadoCompra'])
            compra.ID_EstadoCompra = estado_compra
            compra.save()
            logger.info("Estado de compra parcialmente actualizado exitosamente con ID: %s", pk)
            return Response({"message": "Estado de compra actualizado con éxito."}, status=status.HTTP_200_OK)
        logger.error("No se pudo actualizar el estado de la compra: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk=None):
        # Busca la compra específica por su ID
        compra = get_object_or_404(Compra, pk=pk)
        try:
            # Usa una transacción para asegurar que la eliminación sea atómica
            with transaction.atomic():
                #self.check_object_permissions(request, compra) #Verificación de permisos
                # Elimina primero los detalles relacionados
                DetalleCompra.objects.filter(ID_Compra=compra).delete()
                # Luego, elimina la compra
                compra.delete()

            return Response({"message": "Compra eliminada con éxito."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            # Devuelve un error detallado en caso de falla
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """