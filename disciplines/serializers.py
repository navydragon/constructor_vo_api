from rest_framework import serializers
from .models import Discipline, DisciplineKnowledge, Knowledge

from competenceprofile.serializers import KnowledgeSerializer, AbilitySerializer, AbilityKnowledgeSerializer
from .models import Semester
from products.models import Process


class DisciplineKnowledgeSerializer(serializers.ModelSerializer):
    dk_position = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(source='knowledge.id', read_only=True)
    name = serializers.CharField(source='knowledge.name', read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='knowledge.disciplines', read_only=True, many=True)

    class Meta:
        model = DisciplineKnowledge
        fields = ['id', 'name', 'dk_position', 'parent_id']


class DisciplineAbilitySerializer(serializers.ModelSerializer):
    da_position = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(source='ability.id', read_only=True)
    name = serializers.CharField(source='ability.name', read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='ability.disciplines', read_only=True, many=True)
    knowledges = AbilityKnowledgeSerializer(source='ability.abilityknowledge_set', many=True, read_only=True)

    class Meta:
        model = DisciplineKnowledge
        fields = ['id', 'name', 'da_position', 'parent_id', 'knowledges']


class DisciplineSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    position = serializers.IntegerField(read_only=True)
    program_id = serializers.IntegerField()
    abilities = DisciplineAbilitySerializer(many=True, read_only=True, source='disciplineability_set')

    class Meta:
        model = Discipline
        fields = ('id', 'name', 'position', 'program_id', 'abilities', 'knowledges')


class DisciplineCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    id = serializers.IntegerField(read_only=True)
    process_id = serializers.IntegerField(required=False)
    program_id = serializers.IntegerField()
    semesters = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    processes = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Discipline
        fields = ('id', 'name', 'program_id', 'process_id', 'semesters', 'processes')


class DisciplineShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ('id', 'name')


class SemesterShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = ('id', 'number', 'name')

    def get_name(self, instance):
        return "Семестр №" + str(instance.id)


class SemesterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    disciplines = DisciplineShortSerializer(many=True, read_only=True)

    class Meta:
        model = Semester
        fields = ('__all__')

    def get_name(self, instance):
        return "Семестр №" + str(instance.id)

    def to_representation(self, instance):
        print("Serializer context:", self.context)

        data = super().to_representation(instance)

        if 'x' in self.context:
            # Добавляем 'x' в представление
            data['x'] = 'x'
            disciplines = DisciplineShortSerializer(many=True, read_only=True, context=self.context)
        return data
