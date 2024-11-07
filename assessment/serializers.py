from rest_framework import serializers
from .models import Question, QuestionType, Answer, Task
from competenceprofile.serializers import KnowledgeSerializer
from competenceprofile.models import Knowledge, Ability


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text','text2', 'is_correct')


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ('id', 'name', 'type')


class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True, allow_blank=False)
    knowledge_id = serializers.IntegerField()
    question_type = QuestionTypeSerializer(read_only=True)
    question_type_id = serializers.PrimaryKeyRelatedField(
        queryset=QuestionType.objects.all(), write_only=True)
    answers = AnswerSerializer(many=True)

    # knowledge = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        question_type_id = validated_data.pop('question_type_id')
        answers_data = validated_data.pop('answers', [])
        question = Question.objects.create(question_type=question_type_id,
                                           **validated_data)
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        question_type_id = validated_data.get('question_type_id', None)
        if question_type_id: question_type_id = question_type_id.id
        instance.question_type_id = question_type_id
        instance.save()

        instance.answers.all().delete()
        answers_data = validated_data.pop('answers', [])
        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)
        return instance

    class Meta:
        model = Question
        fields = (
        'id', 'text', 'knowledge_id', 'question_type_id', 'question_type',
        'answers')

class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    description = serializers.CharField(required=True, allow_blank=False)
    ability_id = serializers.IntegerField()

    class Meta:
        model = Task
        fields = (
        'id', 'name', 'description', 'ability_id',
        )

    def create(self, validated_data):
        return Task.objects.create(**validated_data)