import hmac
import hashlib
from firebase_admin import auth
from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from users.models import Tema
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings

from users.services import sendMail
from users.serializers import UserSerializer, TemaSerializer
from django.views.decorators.csrf import csrf_exempt
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
    def newUser(self, request):

        if request.data['type'] == 'normal':
            email = request.data['email']
            display_name = request.data['username']
            password = request.data['password']

            # Firebase user
            # https://firebase.google.com/docs/auth/admin/manage-users#python_4
            firebase_user = auth.create_user(
                email = email,
                email_verified = True,
                password = password,
                display_name = display_name,
                photo_url = None,
                disabled = False
            )
        else:
            email = request.data['user']['email']
            display_name = request.data['user']['name']
            # photo = request.data['user']['picture']['data']['url']
            password = hmac.new(
                msg = bytes(request.data['user']['id'], 'utf-8'),
                key = bytes(request.data['user']['id'], 'utf-8'),
                digestmod = hashlib.sha256
            ).hexdigest()

        user = User(
            username = email,
            email = email,
        )

        user.set_password(password)
        user.save()

        tema = Tema(user=user, tema='Verdes')
        tema.save()
        print(tema)
        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)

        sendMail({
            'email': email
        })

        return Response({
            'token': token
        })

    @action(detail=False, url_path='token-auth-third-party', methods=['POST'])
    def login_third_party(self, request):

        email = request.data['user']['email']

        password = hmac.new(
            msg = bytes(request.data['user']['id'], 'utf-8'),
            key = bytes(request.data['user']['id'], 'utf-8'),
            digestmod = hashlib.sha256
        ).hexdigest()

        user = authenticate(
            request,
            username = email,
            password = password
        )

        if not user:
            return Response({ "error": 'Invalid credentials' })

        if not user.is_active:
            return Response({ "error": 'User not active' })

        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)

        return Response({ "token": token })

class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer

    @action(detail=False, url_path='set_tema', methods=['PATCH'])
    def setTema (self, request):
        usuario = User.objects.get(id=request.data['user'])
        tema = Tema.objects.get(user=usuario)
        tema.tema = request.data['tema']
        tema.save()

        return Response({
            'status':'ok'
        })

    @action(detail=False, url_path='get_tema', methods=['POST'])
    def getTema (self, request):
        usuario = User.objects.get(id=request.data['user'])
        tema = Tema.objects.get(user=usuario)

        return Response({
            'theme': tema.tema
        })
