from rest_framework import serializers
from programs.models import EducationLevel, Direction, Program, ProgramRole, \
    ProgramUser
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from users.serializers import UserShortSerializer
from products.serializers import ProductSerializer

User = get_user_model()


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ['id', 'name']


class EducationDirectionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Direction
        fields = ['id', 'code', 'name', 'level']

    def get_name(self, obj):
        # Объединяем значения полей code и name
        return f"{obj.code} {obj.name}"



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
    direction = EducationDirectionSerializer(source
                                             ='direction_id',
                                             read_only=True)
    level = EducationLevelSerializer(source='level_id', read_only=True)
    participants = ProgramUserSerializer(many=True, read_only=True)
    authorId = serializers.IntegerField(source='author_id', read_only=True)
    my_role = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ('id', 'profile', 'annotation', 'direction', 'level','participants','my_role','authorId')

    def validate(self, attrs):
        direction_data = self.initial_data.get('direction')
        lavel_data = self.initial_data.get('level')
        direction = get_object_or_404(Direction, id=direction_data.get('id'))
        level = get_object_or_404(EducationLevel, id=lavel_data.get('id'))

        attrs['direction_id'] = direction
        attrs['level_id'] = level
        return attrs

    def get_my_role(self, obj):
        user_id = self.context['request'].user.id
        roles = ProgramUser.objects.filter(user_id=user_id)
        name = roles.first().role_id.name if roles.exists() else ''
        return name

class ProgramInformationSerializer(serializers.ModelSerializer):
    participants = ProgramUserSerializer(many=True, read_only=True)
    level = EducationLevelSerializer(source='level_id')
    name = serializers.SerializerMethodField()
    my_role = serializers.SerializerMethodField()
    direction = EducationDirectionSerializer(source='direction_id')
    authorId = serializers.IntegerField(source='author_id', read_only=True)

    class Meta:
        model = Program
        fields = ('id', 'profile', 'annotation', 'direction', 'level','participants','name', 'authorId', 'my_role')

    def get_name(self, obj):
        return f"{obj.direction_id.code} {obj.direction_id.name} {obj.profile} ({obj.level_id.name})"

    def get_my_role(self, obj):
        user_id = self.context['request'].user.id
        roles = ProgramUser.objects.filter(user_id=user_id)
        name = roles.first().role_id.name if roles.exists() else ''
        return name


class ProgramProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True,many=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ('id', 'products', 'name')
    def get_name(self, obj):
        return f"{obj.direction_id.code} {obj.direction_id.name} {obj.profile} ({obj.level_id.name})"
