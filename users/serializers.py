from dj_rest_auth.serializers import TokenSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from dj_rest_auth.serializers import UserDetailsSerializer


from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomTokenSerializer(TokenSerializer):
    token_type = serializers.CharField(source="get_token_type")

    def get_token_type(self, obj):
        return "Bearer"

    class Meta:
        model = Token
        fields = ('key', 'token_type')

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    id = serializers.IntegerField(source='pk')

    class Meta(UserDetailsSerializer.Meta):
        fields = ('id', 'email', 'first_name', 'last_name', 'role')


class UserShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name')

    def get_name(self, obj):
        # Возвращает соединенные имя и фамилию
        return f"{obj.first_name} {obj.last_name}"