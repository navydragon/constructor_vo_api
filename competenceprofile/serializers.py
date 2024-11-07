from rest_framework import serializers
from .models import Ability, Knowledge, ProcessAbility, AbilityKnowledge


class KnowledgeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    position = serializers.IntegerField(read_only=True)
    program_id = serializers.IntegerField()
    questions_count = serializers.SerializerMethodField(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='abilities',read_only=True, many=True)
    discipline_id = serializers.PrimaryKeyRelatedField(source='disciplines',read_only=True, many=True)
    class Meta:
        model = Knowledge
        fields = ('id', 'name', 'position', 'program_id', 'questions_count','parent_id','discipline_id')

    def get_questions_count(self, obj):
        # Получаем количество вопросов для данного объекта Knowledge
        return obj.questions.count()
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'abilities' in self.context:
            representation['abilities'] = AbilitySerializer(instance.abilities.all(), many=True).data

        return representation


class AbilityKnowledgeSerializer(serializers.ModelSerializer):
    ak_position = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(source='knowledge.id', read_only=True)
    name = serializers.CharField(source='knowledge.name', read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='knowledge.abilities',many=True, read_only=True)
    class Meta:
        model = AbilityKnowledge
        fields = ['id', 'name','ak_position','parent_id']


class ProcessAbilitySerializer(serializers.ModelSerializer):
    pa_position = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(source='ability.id', read_only=True)
    name = serializers.CharField(source='ability.name', read_only=True)
    knowledges = AbilityKnowledgeSerializer(source='ability.abilityknowledge_set', many=True, read_only=True)

    parent_id = serializers.PrimaryKeyRelatedField(source='ability.processes',many=True, read_only=True)
    class Meta:
        model = ProcessAbility
        fields = ['id', 'name','pa_position','knowledges','parent_id']





class AbilitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    position = serializers.IntegerField(read_only=True)
    program_id = serializers.IntegerField()
    knowledges = KnowledgeSerializer(read_only=True, many=True)
    parent_id = serializers.PrimaryKeyRelatedField(source='processes',
                                                   many=True, read_only=True)
    discipline_id = serializers.PrimaryKeyRelatedField(source='disciplines',
                                                   many=True, read_only=True)

    tasks_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Ability
        fields = ('id', 'name', 'position', 'program_id', 'knowledges','parent_id','discipline_id', 'tasks_count')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # if instance.program:
        #     representation['program'] = instance.program.id  # Или используйте ProgramSerializer для полной информации
        if 'processes' in self.context:  # Проверка, загружены ли процессы
            from products.serializers import ProcessSerializer
            representation['processes'] = ProcessSerializer(instance.processes.all(), many=True).data

        return representation

    def get_tasks_count(self, obj):
        # Получаем количество вопросов для данного объекта Knowledge
        return obj.tasks.count()





