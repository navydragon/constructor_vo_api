from rest_framework import generics
from programs.models import EducationLevel, Direction, Program, ProgramRole, \
    ProgramUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .serializers import EducationLevelSerializer, EducationDirectionSerializer, \
    ProgramSerializer, ProgramRoleSerializer, ProgramUserSerializer,\
    ProgramInformationSerializer

User = get_user_model()


class EducationLevelListView(generics.ListAPIView):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer


class EducationDirectionListView(generics.ListAPIView):
    queryset = Direction.objects.all()
    serializer_class = EducationDirectionSerializer


class ProgramRoleListView(generics.ListAPIView):
    queryset = ProgramRole.objects.all()
    serializer_class = ProgramRoleSerializer

class ProgramInformationView(generics.RetrieveAPIView):
    queryset = Program.objects.prefetch_related('participants')
    serializer_class = ProgramInformationSerializer

class MyProgramsListView(generics.ListAPIView):
    serializer_class = ProgramInformationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user_id = self.request.user.id
        return Program.objects.filter(
            participants__user_id=user_id).distinct().prefetch_related(
            'participants')

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset().prefetch_related('participants')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        program = self.get_object()
        serializer = self.get_serializer(program)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['program'])
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, pk=None):
        program = self.get_object()
        data = request.data.get('program')
        serializer = self.get_serializer(program, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        program = self.get_object()
        program.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], name='Add Participant')
    def add_participant(self, request, pk=None):
        program = self.get_object()
        data =  request.data.get('participant', {})

        user_id = get_object_or_404(User, id=data.get('user_id'))
        role_id = get_object_or_404(ProgramRole, id=data.get('role_id'))

        # Проверяем, существует ли уже участник с такой ролью в программе
        if ProgramUser.objects.filter(program_id=program, user_id=user_id).exists():
            return Response(
                {'error': 'Пользователь уже имеет роль в этой программе.'},
                status=status.HTTP_400_BAD_REQUEST)

        ProgramUser.objects.create(program_id=program, user_id=user_id,
                                   role_id=role_id)

        program_users = ProgramUser.objects.filter(program_id=program)
        serializer = ProgramUserSerializer(program_users, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'],
            url_path='remove_participant/(?P<participant_id>[^/.]+)',
            name='Remove Participant')
    def remove_participant(self, request, pk=None, participant_id=None):
        program = self.get_object()
        # Здесь должна быть логика проверки, что пользователь может удалять участников

        ProgramUser.objects.filter(program_id=program,
                                   user_id=participant_id).delete()
        program_users = ProgramUser.objects.filter(program_id=program)
        serializer = ProgramUserSerializer(program_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], name='Update Participant')
    def update_participant(self, request, pk=None):
        program = self.get_object()
        data = request.data.get('participant', {})

        user_id = get_object_or_404(User, id=data.get('user_id'))
        role_id = get_object_or_404(ProgramRole, id=data.get('role_id'))

        ProgramUser.objects.update_or_create(
            program_id=program, user_id=user_id,
            defaults={'role_id': role_id}
        )

        program_users = ProgramUser.objects.filter(program_id=program)
        serializer = ProgramUserSerializer(program_users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)