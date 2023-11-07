from rest_framework import serializers
from .models import Product

# from django.contrib.auth import get_user_model
# User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name','program', 'position')