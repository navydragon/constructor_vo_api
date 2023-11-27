
from rest_framework.response import Response

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question, QuestionType
from .serializers import QuestionSerializer, QuestionTypeSerializer
from django.db.models import F


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        knowledge_id = self.kwargs.get('knowledge_id')
        if knowledge_id is not None:
            return Question.objects.filter(knowledge_id=knowledge_id)
        return Question.objects.all()

    def create(self, request, *args, **kwargs):
        question_data = request.data['question']
        knowledge_id = kwargs.get('knowledge_id')
        question_data['knowledge_id'] = knowledge_id
        queryset = self.get_queryset()

        serializer = self.get_serializer(data=question_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, pk=None, *args, **kwargs):
        question = self.get_object()
        question_data = request.data['question']
        knowledge_id = kwargs.get('knowledge_id')
        question_data['knowledge_id'] = knowledge_id
        serializer = self.get_serializer(question, data=question_data, partial=True)
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


class QuestionTypeListView(generics.ListAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer

# class AttachKnowledgeToDisciplineView(APIView):
#     def post(self, request, discipline_id, knowledge_id):
#         discipline = get_object_or_404(Discipline, pk=discipline_id)
#         knowledge = get_object_or_404(Knowledge, pk=knowledge_id)
#         obj, created = discipline.knowledges.through.objects.get_or_create(
#             knowledge_id=knowledge.id,
#             discipline_id=discipline.id
#         )
#         discipline = Discipline.objects.prefetch_related('knowledges').get(pk=discipline_id)
#         serializer = DisciplineSerializer(discipline, context={'knowledges': True})
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class DetachKnowledgeFromDisciplineView(APIView):
#     def delete(self, request, discipline_id, knowledge_id):
#         discipline = get_object_or_404(Discipline, pk=discipline_id)
#         knowledge = get_object_or_404(Knowledge, pk=knowledge_id)
#
#         discipline.knowledges.remove(knowledge)
#
#         discipline = Discipline.objects.prefetch_related('knowledges').get(pk=discipline_id)
#         serializer = DisciplineSerializer(discipline, context={'knowledges': True})
#         return Response(serializer.data, status=status.HTTP_200_OK)