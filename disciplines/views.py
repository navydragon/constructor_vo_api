from rest_framework.views import APIView
from rest_framework.response import Response

from competenceprofile.models import Knowledge
from programs.models import Program
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Discipline
from .serializers import DisciplineSerializer
from django.db.models import F


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        if program_id is not None:
            return Discipline.objects.filter(program_id=program_id).prefetch_related('disciplineknowledge_set').order_by(
                'position')
        return Discipline.objects.all()

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
        current_knowledge_count = discipline.knowledges.count()
        obj, created = discipline.knowledges.through.objects.get_or_create(
            knowledge_id=knowledge.id,
            discipline_id=discipline.id,
            defaults={'position': current_knowledge_count + 1}
        )
        discipline = Discipline.objects.prefetch_related('knowledges').get(pk=discipline_id)
        serializer = DisciplineSerializer(discipline, context={'knowledges': True})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetachKnowledgeFromDisciplineView(APIView):
    def delete(self, request, discipline_id, knowledge_id):
        discipline = get_object_or_404(Discipline, pk=discipline_id)
        knowledge = get_object_or_404(Knowledge, pk=knowledge_id)

        discipline.knowledges.remove(knowledge)

        discipline = Discipline.objects.prefetch_related('knowledges').get(pk=discipline_id)
        serializer = DisciplineSerializer(discipline, context={'knowledges': True})
        return Response(serializer.data, status=status.HTTP_200_OK)