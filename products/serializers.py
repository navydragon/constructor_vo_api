from rest_framework import serializers
from .models import Product, LifeStage, Process, ProcessResult
from programs.models import Program
from competenceprofile.serializers import ProcessAbilitySerializer
# from django.contrib.auth import get_user_model
# User = get_user_model()

class ProcessResultSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)
    product = serializers.IntegerField(read_only=True, source='process.stage.product.id')
    stage = serializers.IntegerField(read_only=True, source='process.stage.id')
    class Meta:
        model = ProcessResult
        fields = ('id', 'name','position','process','product','stage','description','base')

class ProcessResultShortSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProcessResult
        fields = ('id', 'name','position','description','base')

class ProcessSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)
    product = serializers.IntegerField(read_only=True, source='stage.product.id')
    results = ProcessResultSerializer(many=True, read_only=True)
    class Meta:
        model = Process
        fields = ('id', 'name', 'stage', 'position','product','results')

class LifeStageSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)
    processes = ProcessSerializer(many=True, read_only=True)
    class Meta:
        model = LifeStage
        fields = ('id', 'name', 'product', 'position','processes')


class LifeStageShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeStage
        fields = ('id', 'name'  )

class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')

class ProductSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)
    program = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Program.objects.all())
    stages = LifeStageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'program', 'stages', 'position')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['stages'] = sorted(data['stages'], key=lambda x: x.get('position', 0))
        return data

class ProcessCompetenceSerializer(serializers.ModelSerializer):
    abilities = ProcessAbilitySerializer(many=True, read_only=True, source='processability_set')
    stage = LifeStageShortSerializer()
    product = ProductShortSerializer(source='stage.product')
    class Meta:
        model = Process
        fields = ('id', 'name', 'position', 'abilities','stage', 'product')


class ProcessDisciplineSerializer(serializers.ModelSerializer):
    results = ProcessResultShortSerializer(many=True, read_only=True)
    class Meta:
        model = Process
        fields = ('id','name','disciplines','results')
class LifeStageDisciplineSerializer (serializers.ModelSerializer):
    processes = ProcessDisciplineSerializer(many=True, read_only=True)
    class Meta:
        model = LifeStage
        fields = ('id', 'name', 'processes')