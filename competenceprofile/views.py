# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ability
from products.models import Process
from rest_framework import status
from django.shortcuts import get_object_or_404


class AbilityView(APIView):
    # Ваши методы для работы со списком способностей процесса
    def post (self, request, process_id):
        return Response({"status": "kek"})


class AttachAbilityView(APIView):
    def post(self, request, process_id, ability_id):
        process = get_object_or_404(Process, pk=process_id)
        ability = get_object_or_404(Ability, pk=ability_id)
        # Логика для прикрепления способности
        return Response({"status": "Способность прикреплена"})


class DetachAbilityView(APIView):
    def delete(self, request, process_id, ability_id):
        process = get_object_or_404(Process, pk=process_id)
        ability = get_object_or_404(Ability, pk=ability_id)
        # Логика для откр
