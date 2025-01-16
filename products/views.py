from rest_framework import generics

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from programs.models import Nsi
from .models import Product, LifeStage, Process, ProcessResult
from .serializers import (ProductSerializer, LifeStageSerializer, ProcessSerializer, ProcessCompetenceSerializer,
                          LifeStageDisciplineSerializer, ProcessResultSerializer)
from django.db.models import F

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Переопределение метода для фильтрации продуктов по program_id.
        """
        program_id = self.kwargs.get('program_id')
        if program_id is not None:
            return Product.objects.filter(program_id=program_id).order_by('position')
        return Product.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'kwargs': self.kwargs
        })
        return context

    def create(self, request, *args, **kwargs):
        product_data = request.data['product']
        program_id = kwargs.get('program_id')
        product_data['program'] = program_id
        queryset = self.get_queryset()
        position = queryset.count() + 1

        serializer = self.get_serializer(data=product_data)
        serializer.is_valid(raise_exception=True)

        product = serializer.save(position=position)
        if product_data['nsis']:
            nsis = Nsi.objects.filter(id__in=product_data['nsis'])
            product.nsis.set(nsis)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


    def partial_update(self, request, pk=None, *args, **kwargs):
        product = self.get_object()
        product_data = request.data['product']
        program_id = kwargs.get('program_id')
        product_data['program'] = program_id
        # program_id = kwargs.get('program_id')
        # product_data['program'] = program_id
        serializer = self.get_serializer(product, data=product_data)

        if serializer.is_valid():
            serializer.save()
            if product_data['nsis']:
                product.nsis.clear()
                nsis = Nsi.objects.filter(id__in=product_data['nsis'])
                product.nsis.set(nsis)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        object_id = product.id
        position_to_update = product.position

        self.perform_destroy(product)

        Product.objects.filter(position__gt=position_to_update).update(
            position=F('position') - 1)

        return Response({'message': 'Успешно удалено', 'id':object_id}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='reorder')
    def reorder(self, request, program_id=None):
        products_order = request.data.get('products')
        with transaction.atomic():  # Используем атомарные транзакции для обеспечения консистентности
            for position, product_id in enumerate(products_order, start=1):
                Product.objects.filter(id=product_id).update(position=position)

        products = Product.objects.filter(id__in=products_order).order_by('position')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='sync_nsis')
    def sync_nsis(self, request,program_id, pk):
        nsis_ids = request.data.get("nsis", [])
        product = get_object_or_404(Product, id=pk)

        product.nsis.clear()
        nsis = Nsi.objects.filter(id__in=nsis_ids)
        product.nsis.set(nsis)  # Устанавливаем только указанные связи

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LifeStageViewSet(viewsets.ModelViewSet):
    queryset = LifeStage.objects.all()
    serializer_class = LifeStageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset = LifeStage.objects.all()

        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)

        return queryset.order_by('position')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'kwargs': self.kwargs
        })
        return context

    def create(self, request, *args, **kwargs):
        stage_data = request.data['stage']
        product_id = kwargs.get('product_id')
        stage_data['product'] = product_id
        queryset = self.get_queryset()
        position = queryset.count() + 1

        serializer = self.get_serializer(data=stage_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(position=position)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


    def partial_update(self, request, pk=None, *args, **kwargs):
        stage = self.get_object()
        stage_data = request.data['stage']
        product_id = kwargs.get('product_id')
        stage_data['product'] = product_id

        serializer = self.get_serializer(stage, data=stage_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        stage = self.get_object()
        position_to_update = stage.position
        object_id = stage.id
        self.perform_destroy(stage)

        LifeStage.objects.filter(position__gt=position_to_update).update(
            position=F('position') - 1)

        return Response({'message': 'Успешно удалено', 'id':object_id}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='reorder')
    def reorder(self, request, product_id=None):
        stages_order = request.data.get('stages')
        for stage_id in stages_order:
            get_object_or_404(LifeStage, id=stage_id)
        with transaction.atomic():
            for position, stage_id in enumerate(stages_order, start=1):
                LifeStage.objects.filter(id=stage_id).update(position=position)

        stages = LifeStage.objects.filter(id__in=stages_order).order_by('position')
        serializer = LifeStageSerializer(stages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        stage_id = self.kwargs.get('stage_id')
        if stage_id is not None:
            return Process.objects.filter(stage_id=stage_id).order_by('position')
        return Process.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'kwargs': self.kwargs})
        return context

    def create(self, request, *args, **kwargs):
        process_data = request.data['process']
        stage_id = kwargs.get('stage_id')
        process_data['stage'] = stage_id
        queryset = self.get_queryset()
        position = queryset.count() + 1

        serializer = self.get_serializer(data=process_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(position=position)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


    def partial_update(self, request, pk=None, *args, **kwargs):
        process = self.get_object()
        process_data = request.data['process']
        stage_id = kwargs.get('stage_id')
        process_data['stage'] = stage_id

        serializer = self.get_serializer(process, data=process_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        process = self.get_object()
        object_id = process.id
        position_to_update = process.position

        self.perform_destroy(process)

        Process.objects.filter(position__gt=position_to_update).update(
            position=F('position') - 1)

        return Response({'message': 'Успешно удалено', 'id':object_id}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='reorder')
    def reorder(self, request, stage_id=None):
        processes_order = request.data.get('processes')
        for process_id in processes_order:
            get_object_or_404(Process, id=process_id)
        with transaction.atomic():
            for position, process_id in enumerate(processes_order, start=1):
                Process.objects.filter(id=process_id).update(position=position)

        processes = Process.objects.filter(id__in=processes_order).order_by('position')
        serializer = ProcessSerializer(processes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProcessResultViewSet(viewsets.ModelViewSet):
    queryset = ProcessResult.objects.all()
    serializer_class = ProcessResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        process_id = self.kwargs.get('process_id')
        if process_id is not None:
            return ProcessResult.objects.filter(process_id=process_id).order_by('position')
        return ProcessResult.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'kwargs': self.kwargs})
        return context

    def create(self, request, *args, **kwargs):
        result_data = request.data['result']
        process_id = kwargs.get('process_id')
        result_data['process'] = process_id
        queryset = self.get_queryset()
        position = queryset.count() + 1

        serializer = self.get_serializer(data=result_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(position=position)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, pk=None, *args, **kwargs):
        result = self.get_object()
        result_data = request.data['result']
        process_id = kwargs.get('process_id')
        result_data['process'] = process_id

        serializer = self.get_serializer(result, data=result_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        result = self.get_object()
        object_id = result.id
        position_to_update = result.position

        self.perform_destroy(result)

        ProcessResult.objects.filter(position__gt=position_to_update).update(
            position=F('position') - 1)

        return Response({'message': 'Успешно удалено', 'id': object_id}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='reorder')
    def reorder(self, request, process_id=None):
        results_order = request.data.get('results')
        for result_id in results_order:
            get_object_or_404(ProcessResult, id=result_id)
        with transaction.atomic():
            for position, result_id in enumerate(results_order, start=1):
                ProcessResult.objects.filter(id=result_id).update(position=position)

        results = ProcessResult.objects.filter(id__in=results_order).order_by('position')
        serializer = ProcessResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProcessListView(ListAPIView):
    serializer_class = ProcessCompetenceSerializer
    queryset = Process.objects.all()

    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        if program_id is not None:
            queryset = Process.objects.filter(stage__product__program_id=program_id)
            queryset = queryset.prefetch_related(
                'processability_set__ability__abilityknowledge_set__knowledge__abilities',
                'processability_set__ability__processes'
            )

            queryset = queryset.select_related('stage__product')

            queryset = queryset.order_by('stage__product__position','stage__position','position')
            return queryset
        return Process.objects.none()

    def list(self, request, *args, **kwargs):
        program_id = self.kwargs.get('program_id')
        if program_id is None:
            return Response({'detail': 'Program ID is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print (serializer.data)
        return Response(serializer.data)

class StageListView(ListAPIView):
    serializer_class = LifeStageDisciplineSerializer
    queryset = LifeStage.objects.all()

    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        if program_id is not None:
            queryset = LifeStage.objects.filter(product__program_id=program_id)
            queryset = queryset.order_by('product__position','position')
            return queryset
        return LifeStage.objects.none()

    def list(self, request, *args, **kwargs):
        program_id = self.kwargs.get('program_id')
        if program_id is None:
            return Response({'detail': 'Program ID is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)