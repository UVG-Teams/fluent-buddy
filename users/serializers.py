from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Tema

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        )

class TemaSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Tema
        fields = (
            'id',
            'user',
            'tema',
        )