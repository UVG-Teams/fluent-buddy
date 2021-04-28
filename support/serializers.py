from rest_framework import serializers

from support.models import Contact
from users.serializers import UserSerializer

class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Contact
        fields = (
            'id',
            'user',
            'message',
        )