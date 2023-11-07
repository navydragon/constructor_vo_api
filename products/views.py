from rest_framework import generics

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer

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


    def create(self, request, *args, **kwargs):
        program_id = kwargs.get('program_id')
        product_data = request.data['product']
        queryset = self.get_queryset()
        position = queryset.count() + 1

        if program_id is not None:
            product_data['program'] = program_id
            print(product_data)
            serializer = self.get_serializer(data=product_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(position=position)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response(
                {"detail": "Missing program_id."},
                status=status.HTTP_400_BAD_REQUEST
            )

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