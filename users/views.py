from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action

from users.serializers import UserSerializer
from permissions.services import APIPermissionClassFactory
from users.services import sendMail
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    message = 'El correo fue enviado con éxito'
    messageError = 'El correo <strong>no</strong> fue enviado con éxito'
    try:
        sendMail(request)
        return render(
        request,
        'signup/response.html',
            {
                'message': message,
                'direccion': request.POST['email']
            }
        )
    except:
        return render(
        request,
        'signup/resopnseError.html',
            {
                'message': message,
                'direccion': request.POST['email']
            }
        )


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
        sendMail(request)
        return Response({
            'status':'Ok'
        })
