from rest_framework import serializers
from .models import Discipline
from competenceprofile.serializers import KnowledgeSerializer

class DisciplineSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    position = serializers.IntegerField(read_only=True)
    program_id = serializers.IntegerField()
    knowledges = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Discipline
        fields = ('id', 'name', 'position', 'program_id', 'knowledges')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'knowledges' in self.context:
            representation['knowledges'] = KnowledgeSerializer(
                instance.knowledges.all(), many=True).data
        return representation

