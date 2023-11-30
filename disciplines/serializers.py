from rest_framework import serializers
from .models import Discipline, DisciplineKnowledge, Knowledge

from competenceprofile.serializers import KnowledgeSerializer, AbilitySerializer, AbilityKnowledgeSerializer


class DisciplineKnowledgeSerializer(serializers.ModelSerializer):
    dk_position = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(source='knowledge.id', read_only=True)
    name = serializers.CharField(source='knowledge.name', read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='knowledge.disciplines', read_only= True, many=True)
    class Meta:
        model = DisciplineKnowledge
        fields = ['id', 'name','dk_position','parent_id']

class DisciplineAbilitySerializer(serializers.ModelSerializer):
    da_position = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(source='ability.id', read_only=True)
    name = serializers.CharField(source='ability.name', read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='ability.disciplines', read_only= True, many=True)
    knowledges = AbilityKnowledgeSerializer(source='ability.abilityknowledge_set', many=True, read_only= True)
    class Meta:
        model = DisciplineKnowledge
        fields = ['id', 'name','da_position','parent_id','knowledges']

class DisciplineSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    position = serializers.IntegerField(read_only=True)
    program_id = serializers.IntegerField()
    knowledges = DisciplineKnowledgeSerializer(many=True, read_only=True, source='disciplineknowledge_set')
    abilities = DisciplineAbilitySerializer(many=True, read_only=True,
                                               source='disciplineability_set')

    class Meta:
        model = Discipline
        # ields = '__all__'
        fields = ('id', 'name', 'position', 'program_id', 'knowledges','abilities')



