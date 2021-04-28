from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
from django.contrib.auth.models import User
from support.models import Contact
from support.serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @action(detail=False, url_path='save_message', methods=['POST'])
    def saveMessage (self, request):
        print(request.data)
        usuario = User.objects.get(id=request.data['id'])
        message = Contact(user=usuario, message=request.data['message'])
        message.save()

        return Response({
            'status':'ok'
        })