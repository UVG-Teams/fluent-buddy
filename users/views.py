from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action

from users.serializers import UserSerializer
from permissions.services import APIPermissionClassFactory


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        # APIPermissionClassFactory(
        #     name = 'UserPermission',
        #     permission_configuration = {
        #         'base': {
        #             'create': True,
        #             'list': True,
        #         },
        #         'instance': {
        #             'retrieve': True,
        #             'update': True,
        #             'partial_update': True,
        #             'destroy': True,
        #         }
        #     }
        # )
    )

    @action(detail=False, url_path='create_user', methods=['POST'])
    def newUser (self, request):
        usuario = User(
            username = request.data['username'],
            email = request.data['email'],
        )
        usuario.set_password(request.data['password'])
        usuario.save()

        return Response({
            'status':'Ok'
        })
