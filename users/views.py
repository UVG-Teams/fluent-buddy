from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action

from users.serializers import UserSerializer
from permissions.services import APIPermissionClassFactory

import hmac
import hashlib
from firebase_admin import auth


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

        if request.data['type'] == 'normal':
            email = request.data['email']
            display_name = request.data['username']
            photo = None
            password = request.data['password']
        else:
            email = request.data['user']['email']
            display_name = request.data['user']['name']
            photo = request.data['user']['picture']['data']['url']
            password = hmac.new(
                msg = bytes(request.data['user']['id'], 'utf-8'),
                key = bytes(request.data['user']['id'], 'utf-8'),
                digestmod = hashlib.sha256
            ).hexdigest()

        print("email: ", email)
        print("password: ", password)
        print("display_name: ", display_name)
        print("photo: ", photo)

        usuario = User(
            username = email,
            email = email,
        )

        usuario.set_password(password)
        usuario.save()

        # Firebase user
        # https://firebase.google.com/docs/auth/admin/manage-users#python_4
        # firebase_user = auth.create_user(
        #     email = email,
        #     email_verified = True,
        #     password = password,
        #     display_name = display_name,
        #     photo_url = photo,
        #     disabled = False
        # )

        return Response({
            'status':'Ok'
        })
