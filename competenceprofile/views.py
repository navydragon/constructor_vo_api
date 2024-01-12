# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ability, Knowledge
from products.models import Process
from programs.models import Program
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import AbilitySerializer, KnowledgeSerializer
from django.db.models import F
from django.db import transaction


class AbilityViewSet(viewsets.ModelViewSet):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        if program_id is not None:
            return Ability.objects.filter(program_id=program_id).order_by(
                'position').prefetch_related('knowledges__questions','knowledges__abilities','knowledges__disciplines','processes','disciplines')
        return Ability.objects.all()

    def create(self, request, *args, **kwargs):
        ability_data = request.data['ability']
        program_id = kwargs.get('program_id')
        ability_data['program_id'] = program_id
        queryset = self.get_queryset()
        position = queryset.count() + 1
        serializer = self.get_serializer(data=ability_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(position=position)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, pk=None, *args, **kwargs):
        ability = self.get_object()
        ability_data = request.data['ability']
        program_id = kwargs.get('program_id')
        ability_data['program_id'] = program_id
        serializer = self.get_serializer(ability, data=ability_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        ability = self.get_object()
        object_id = ability.id
        position_to_update = ability.position
        Ability.objects.filter(position__gt=position_to_update).update(
            position=F('position') - 1)

        processes = ability.processes.all()
        with transaction.atomic():
            for process in processes:
                pa_position = process.abilities.through.objects.get(
                    process_id=process.id,
                    ability_id=ability.id
                ).pa_position
                process.update_pa_positions(pa_position)
        self.perform_destroy(ability)

        return Response({'message': 'Успешно удалено', 'id':object_id}, status=status.HTTP_200_OK)


class AttachAbilityView(APIView):
    def post(self, request, process_id, ability_id):
        process = get_object_or_404(Process, pk=process_id)
        ability = get_object_or_404(Ability, pk=ability_id)

        obj, created = process.abilities.through.objects.get_or_create(
            process_id=process.id,
            ability_id=ability.id,
            defaults={'pa_position': process.abilities.count() + 1}
        )
        # process.abilities.add(ability, through_defaults={'pa_position': process.abilities.count() + 1})
        serializer = AbilitySerializer(ability)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetachAbilityView(APIView):
    def delete(self, request, process_id, ability_id):
        process = get_object_or_404(Process, pk=process_id)
        ability = get_object_or_404(Ability, pk=ability_id)

        # Получаем позицию перед отсоединением
        pa_position = process.abilities.through.objects.get(
            process_id=process.id,
            ability_id=ability.id
        ).pa_position

        # Отсоединяем способность
        process.abilities.remove(ability)

        # Вызываем метод для обновления pa_position
        process.update_pa_positions(pa_position)

        serializer = AbilitySerializer(ability)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CreateAbilityFromProcess(APIView):
    def post(self, request, process_id):
        process = get_object_or_404(Process, pk=process_id)
        program = process.stage.product.program
        ability_data = request.data['ability']

        ability_data['program_id'] = int(program.id)

        serializer = AbilitySerializer(data=ability_data)
        serializer.is_valid(raise_exception=True)
        ability = serializer.save(position=program.abilities.count() + 1)

        process.abilities.add(ability, through_defaults={'pa_position': process.abilities.count() + 1})

        serializer = AbilitySerializer(ability)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class KnowledgeViewSet(viewsets.ModelViewSet):
    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        if program_id is not None:
            return Knowledge.objects.filter(program_id=program_id).prefetch_related('abilities','questions','disciplines').order_by(
                'position')
        return Knowledge.objects.all()

    def create(self, request, *args, **kwargs):
        knowledge_data = request.data['knowledge']
        program_id = kwargs.get('program_id')
        knowledge_data['program_id'] = program_id
        queryset = self.get_queryset()
        position = queryset.count() + 1
        serializer = self.get_serializer(data=knowledge_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(position=position)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, pk=None, *args, **kwargs):
        ability = self.get_object()
        knowledge_data = request.data['knowledge']
        program_id = kwargs.get('program_id')
        knowledge_data['program_id'] = program_id
        serializer = self.get_serializer(ability, data=knowledge_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        knowledge = self.get_object()
        object_id = knowledge.id
        position_to_update = knowledge.position
        Knowledge.objects.filter(position__gt=position_to_update).update(
            position=F('position') - 1)

        abilities = knowledge.abilities.all()
        with transaction.atomic():
            for ability in abilities:
                ak_position = ability.knowledges.through.objects.get(
                    ability_id=ability.id,
                    knowledge_id=knowledge.id
                ).ak_position
                ability.update_ak_positions(ak_position)

        self.perform_destroy(knowledge)
        return Response({'message': 'Успешно удалено', 'id':object_id}, status=status.HTTP_200_OK)


class AttachKnowledgeView(APIView):
    def post(self, request, ability_id, knowledge_id):
        ability = get_object_or_404(Ability, pk=ability_id)
        knowledge = get_object_or_404(Knowledge, pk=knowledge_id)
        obj, created = ability.knowledges.through.objects.get_or_create(
            knowledge_id=knowledge.id,
            ability_id=ability.id,
            defaults={'ak_position': ability.knowledges.count() + 1}
        )

        serializer = KnowledgeSerializer(knowledge)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetachKnowledgeView(APIView):
    def delete(self, request, ability_id, knowledge_id):
        ability = get_object_or_404(Ability, pk=ability_id)
        knowledge = get_object_or_404(Knowledge, pk=knowledge_id)

        # Получаем позицию перед отсоединением
        ak_position = ability.knowledges.through.objects.get(
            ability_id=ability.id,
            knowledge_id=knowledge.id
        ).ak_position

        # Отсоединяем знание
        ability.knowledges.remove(knowledge)

        # Вызываем метод для обновления ak_position
        ability.update_ak_positions(ak_position)

        serializer = KnowledgeSerializer(knowledge)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateKnowledgeFromAbility(APIView):
    def post(self, request, ability_id):
        ability = get_object_or_404(Ability, pk=ability_id)
        program = ability.program
        knowledge_data = request.data['knowledge']

        knowledge_data['program_id'] = int(program.id)

        serializer = KnowledgeSerializer(data=knowledge_data)
        serializer.is_valid(raise_exception=True)
        knowledge = serializer.save(position=program.knowledges.count() + 1)

        ability.knowledges.add(knowledge, through_defaults={'ak_position': ability.knowledges.count() + 1})

        serializer = KnowledgeSerializer(knowledge)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
