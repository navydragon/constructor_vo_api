
from rest_framework.response import Response

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question, QuestionType, Task
from .serializers import QuestionSerializer, QuestionTypeSerializer, TaskSerializer
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
        question = self.get_object()
        object_id = question.id

        self.perform_destroy(question)
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

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ability_id = self.kwargs.get('ability_id')
        if ability_id is not None:
            return Task.objects.filter(ability_id=ability_id)
        return Task.objects.all()

    def create(self, request, *args, **kwargs):
        task_data = request.data['task']
        ability_id = kwargs.get('ability_id')
        task_data['ability_id'] = ability_id
        queryset = self.get_queryset()

        serializer = self.get_serializer(data=task_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, pk=None, *args, **kwargs):
        task = self.get_object()
        task_data = request.data['task']
        ability_id = kwargs.get('ability_id')
        task_data['ability_id'] = ability_id
        serializer = self.get_serializer(task, data=task_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        object_id = task.id

        self.perform_destroy(task)
        return Response({'message': 'Успешно удалено', 'id':object_id}, status=status.HTTP_200_OK)


class TaskListView (generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        program_id = self.kwargs.get('program_id')
        if program_id is not None:
            queryset = Task.objects.filter(ability__program_id=program_id)

            return queryset
        return Task.objects.none()