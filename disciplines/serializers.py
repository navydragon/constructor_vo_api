from rest_framework import serializers
from .models import Discipline, DisciplineKnowledge, Knowledge, SemesterDiscipline

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



class SemesterDisciplineSerializer(serializers.ModelSerializer):
    semester_number = serializers.IntegerField(source='semester.number')
    name = serializers.CharField(source='discipline.name')
    id = serializers.IntegerField(source='discipline.id')
    class Meta:
        model = SemesterDiscipline
        fields = ('id','name','semester_number', 'zet', 'control')

class DisciplineShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = ('id', 'name', 'semesters')



class SemesterShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = ('id', 'number', 'name')

    def get_name(self, instance):
        return "Семестр №" + str(instance.id)


class SemesterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    disciplines = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = ('id', 'name', 'disciplines')

    def get_name(self, instance):
        return "Семестр №" + str(instance.number)

    def get_disciplines(self, instance):
        semester_disciplines = SemesterDiscipline.objects.filter(semester=instance)
        return SemesterDisciplineSerializer(semester_disciplines, many=True).data
