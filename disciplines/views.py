from rest_framework.views import APIView
from rest_framework.response import Response

from competenceprofile.models import Knowledge, Ability
from programs.models import Program
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Discipline, Semester, SemesterDiscipline
from .serializers import DisciplineSerializer, DisciplineShortSerializer
from competenceprofile.serializers import KnowledgeSerializer, AbilitySerializer
from django.db.models import F


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    #serializer_class =
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        if program_id is not None:
            queryset = Discipline.objects.filter(program_id=program_id)
            queryset = queryset.prefetch_related(
                'disciplineability_set__ability__disciplines',
                'disciplineability_set__ability__abilityknowledge_set__knowledge__abilities',
                'disciplineknowledge_set__knowledge__disciplines',
                'knowledges',
                'abilities',
                #'disciplineknowledge_set__'
            )
            # queryset = queryset.prefetch_related('knowledges__disciplines','abilities__disciplines')
            queryset = queryset.order_by('position')
            return queryset

    def get_serializer_class(self):

        if self.request.query_params.get('short'):
            return DisciplineShortSerializer

        return DisciplineSerializer

    def get_serializer_context(self):
        # Получаем базовый контекст сериализатора
        context = super().get_serializer_context()

        # Добавляем свои данные в контекст, например, x
        context['x'] = 'with_semesters'  # Замените 'your_value' на актуальное значение

        return context
    def create(self, request, *args, **kwargs):
        discipline_data = request.data['discipline']
        program_id = kwargs.get('program_id')
        discipline_data['program_id'] = program_id
        queryset = self.get_queryset()
        position = queryset.count() + 1
        serializer = self.get_serializer(data=discipline_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(position=position)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, pk=None, *args, **kwargs):
        discipline = self.get_object()
        discipline_data = request.data['discipline']
        program_id = kwargs.get('program_id')
        discipline_data['program_id'] = program_id
        serializer = self.get_serializer(discipline, data=discipline_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        discipline = self.get_object()
        object_id = discipline.id
        position_to_update = discipline.position
        Discipline.objects.filter(position__gt=position_to_update).update(
            position=F('position') - 1)
        self.perform_destroy(discipline)
        return Response({'message': 'Успешно удалено', 'id':object_id}, status=status.HTTP_200_OK)


class AttachKnowledgeToDisciplineView(APIView):
    def post(self, request, discipline_id, knowledge_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        knowledge = get_object_or_404(Knowledge, pk=knowledge_id)
        obj, created = discipline.knowledges.through.objects.get_or_create(
            knowledge_id=knowledge.id,
            discipline_id=discipline.id,
            defaults={'dk_position': discipline.knowledges.count() + 1}
        )
        # discipline = Discipline.objects.prefetch_related('knowledges').get(pk=discipline_id)
        serializer = KnowledgeSerializer(knowledge)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetachKnowledgeFromDisciplineView(APIView):
    def delete(self, request, discipline_id, knowledge_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        knowledge = get_object_or_404(Knowledge, pk=knowledge_id)

        discipline.knowledges.remove(knowledge)

        # discipline = Discipline.objects.prefetch_related('knowledges').get(pk=discipline_id)
        serializer = KnowledgeSerializer(knowledge)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttachAbilityToDisciplineView(APIView):
    def post(self, request, discipline_id, ability_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        ability = get_object_or_404(Ability, pk=ability_id)
        obj, created = discipline.abilities.through.objects.get_or_create(
            ability_id=ability.id,
            discipline_id=discipline.id,
            defaults={'da_position': discipline.abilities.count() + 1}
        )

        for knowledge in ability.knowledges.all():
            obj, created = discipline.knowledges.through.objects.get_or_create(
                knowledge_id=knowledge.id,
                discipline_id=discipline.id,
                defaults={'dk_position': discipline.knowledges.count() + 1}
            )

        serializer = AbilitySerializer(Ability.objects.prefetch_related('disciplines','processes').get(pk=ability_id))
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetachAbilityFromDisciplineView(APIView):
    def delete(self, request, discipline_id, ability_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        ability = get_object_or_404(Ability, pk=ability_id)

        discipline.abilities.remove(ability_id)

        serializer = AbilitySerializer(ability)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttachDisciplineToSemester (APIView):
    def post(self, request, semester_id, discipline_id):
        semester = get_object_or_404(Semester, pk=semester_id)
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        obj, created = semester.disciplines.through.objects.get_or_create(
            semester_id=semester.id,
            discipline_id=discipline.id,
        )

        serializer = DisciplineShortSerializer(discipline)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetachDisciplineFromSemester (APIView):
    def delete(self, request, semester_id, discipline_id):
        semester = get_object_or_404(Semester, pk=semester_id)
        discipline = get_object_or_404(Discipline, pk=discipline_id)

        semester.disciplines.remove(discipline_id)

        serializer = DisciplineShortSerializer(discipline)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MoveDiscipline (APIView):

    def patch(self, request, discipline_id, source_id, destination_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        source_semester = get_object_or_404(Semester, pk=source_id)
        destination_semester = get_object_or_404(Semester, pk=destination_id)

        SemesterDiscipline.objects.filter(discipline=discipline, semester=source_semester).delete()
        SemesterDiscipline.objects.create(discipline=discipline, semester=destination_semester)

        serializer = DisciplineShortSerializer(discipline)
        return Response(serializer.data, status=status.HTTP_200_OK)