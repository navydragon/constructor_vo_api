from rest_framework import serializers
from .models import Ability, Knowledge
from products.serializers import ProcessSerializer

class AbilitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    position = serializers.IntegerField(read_only=True)
    program_id = serializers.IntegerField()
    processes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Ability
        fields = ('id', 'name', 'position', 'program_id', 'processes')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # if instance.program:
        #     representation['program'] = instance.program.id  # Или используйте ProgramSerializer для полной информации
        if 'processes' in self.context:  # Проверка, загружены ли процессы
            representation['processes'] = ProcessSerializer(instance.processes.all(), many=True).data

        return representation


class KnowledgeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    position = serializers.IntegerField(read_only=True)
    program_id = serializers.IntegerField()
    abilities = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Knowledge
        fields = ('id', 'name', 'position', 'program_id', 'abilities')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'abilities' in self.context:
            representation['abilities'] = AbilitySerializer(instance.abilities.all(), many=True).data

        return representation
