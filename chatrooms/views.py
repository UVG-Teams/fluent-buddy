from rest_framework import viewsets
from firebase_admin import firestore, auth
from chatrooms.models import Chatroom
from rest_framework.decorators import action
from rest_framework.response import Response


class ChatroomViewSet(viewsets.ModelViewSet):
    queryset = Chatroom.objects.all()
    serializer_class = None
    permission_classes = ()

    @action(detail=False, url_path='create', methods=['POST'])
    def create_chatroom(self, request):
        firestore_db = firestore.client()

        bot_uid = '{}-{}'.format(request.data['language'], request.data['gender'])
        current_user = auth.get_user_by_email(request.user.email)

        chatroom_data = {
            'last_message': {
                'sent_by': '',
                'sent_at': '',
                'text': '',
            },
            'members_uids': [bot_uid, current_user.uid],
            'members': {
                bot_uid: {
                    'full_name': request.data['name']
                },
                current_user.uid: {
                    'full_name': '{} {}'.format(request.user.first_name, request.user.last_name)
                }
            }
        }

        firestore_db.collection('chatrooms').add(chatroom_data)

        return Response({
            'status': 'ok'
        })
