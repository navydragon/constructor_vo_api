from rest_framework import serializers
from .models import Product, LifeStage, Process
from programs.models import Program

# from django.contrib.auth import get_user_model
# User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)
    program = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Program.objects.all())
    class Meta:
        model = Product
        fields = ('id', 'name', 'program', 'position')


class LifeStageSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)

    class Meta:
        model = LifeStage
        fields = ('id', 'name', 'product', 'position')


class ProcessSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)

    class Meta:
        model = Process
        fields = ('id', 'name', 'stage', 'position')
