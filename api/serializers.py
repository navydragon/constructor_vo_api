from rest_framework import serializers
from programs.models import EducationLevel, Direction, Program, ProgramRole, \
    ProgramUser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from users.serializers import UserShortSerializer

User = get_user_model()


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['id', 'name']


class EducationDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ['id', 'code', 'name', 'level']


class ProgramRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramRole
        fields = ['id', 'name']


class ProgramUserSerializer(serializers.ModelSerializer):
    role = ProgramRoleSerializer(source='role_id')
    user = UserShortSerializer(source='user_id')
    class Meta:
        model = ProgramUser
        fields = ['id', 'user', 'role', 'program_id']


class ProgramSerializer(serializers.ModelSerializer):
    direction = EducationDirectionSerializer(source='direction_id',
                                             read_only=True)
    level = EducationLevelSerializer(source='level_id', read_only=True)
    participants = ProgramUserSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = ('id', 'profile', 'annotation', 'direction', 'level','participants')

    def validate(self, attrs):
        direction_data = self.initial_data.get('direction')
        lavel_data = self.initial_data.get('level')
        direction = get_object_or_404(Direction, id=direction_data.get('id'))
        level = get_object_or_404(EducationLevel, id=lavel_data.get('id'))

        attrs['direction_id'] = direction
        attrs['level_id'] = level
        return attrs


class ProgramInformationSerializer(serializers.ModelSerializer):
    participants = ProgramUserSerializer(many=True, read_only=True)
    level = EducationLevelSerializer(source='level_id')
    name = serializers.SerializerMethodField()
    direction = EducationDirectionSerializer(source='direction_id')
    authorId = serializers.IntegerField(source='author_id', read_only=True)

    class Meta:
        model = Program
        fields = ('id', 'profile', 'annotation', 'direction', 'level','participants','name', 'authorId')

    def get_name(self, obj):
        return f"{obj.direction_id.code} {obj.direction_id.name} {obj.profile} ({obj.level_id.name})"


