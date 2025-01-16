# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import NsiType, Ministry, Nsi, Program
from .serializers import NsiTypeSerializer, MinistrySerializer, NsiSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import status

class NsiTypeViewSet(viewsets.ModelViewSet):
    queryset = NsiType.objects.filter(active=True).order_by('name')
    serializer_class = NsiTypeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        #data.insert(0, data.pop())
        return Response(data)



class MinistryViewSet(viewsets.ModelViewSet):
    queryset = Ministry.objects.all()
    serializer_class = MinistrySerializer

class NsiViewSet(viewsets.ModelViewSet):
    queryset = Nsi.objects.all()
    serializer_class = NsiSerializer

    def get_queryset(self):
        program_id = self.kwargs['program_id']
        return Nsi.objects.filter(program_id=program_id)

    def create(self, request, *args, **kwargs):
        nsi_data = request.data['nsi']
        program_id = kwargs.get('program_id')
        author = self.request.user
        try:
            program = Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            raise ValidationError(f'Program with id {program_id} does not exist')

        nsi_data['program'] = program_id
        nsi_data['type'] = nsi_data['type_id']
        serializer = self.get_serializer(data=nsi_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(program=program,author=author)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        program_id = self.kwargs['program_id']
        nsi_data = request.data.get('nsi', {})

        try:
            program = Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            raise ValidationError(f'Program with id {program_id} does not exist')

        serializer = self.get_serializer(instance, data=nsi_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(program=program)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Успешно удалено', 'id':instance.id}, status=status.HTTP_200_OK)