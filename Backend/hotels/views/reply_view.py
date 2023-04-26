from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from ..serializers import ReplySerializer
from ..models import Reply, Comment, Notification
import sys
sys.path.append("...")
from accounts.models import MyUser


class ReplyAdd(CreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        reply = request.data
        print(reply)
        if 'author' not in reply or reply['author'] == '':
            author = request.user
        else:
            author_id = reply['author']
            author = MyUser.objects.get(pk=author_id)

        if 'detail' not in reply:
            detail = ''
        else:
            detail = reply['detail']

        if 'reply_to' not in reply:
            reply_to = ''
        else:
            reply_to = reply['reply_to']

        if 'object_id' not in reply:
            object_id = ''
        else:
            object_id = reply['object_id']

        ordinary_dict = {'reply_to': reply_to,
                         'object_id': object_id,
                         'author': author.id,
                         'detail': detail}

        QueryDict('', mutable=True).update(ordinary_dict)
        serializer = self.get_serializer(data=ordinary_dict)
        serializer.is_valid(raise_exception=True)
        reply_obj = serializer.save()
        reply_obj.save()

        #find out who it is replying to
        if reply_to == '11' or reply_to == 11:    # reply to a comment
            try:
                comment = Comment.objects.get(id=reply['object_id'])
                receiver = comment.author
            except:
                return Response({"error": "The comment you are replying to does not exist"}, status=status.HTTP_403_FORBIDDEN)
        if reply_to == '12' or reply_to == 12:    # reply to a reply
            try:
                reply = Reply.objects.get(id=reply['object_id'])
                receiver = reply.author
            except:
                return Response({"error": "The reply you are replying to does not exist"}, status=status.HTTP_403_FORBIDDEN)

        # create notification
        notif = Notification.objects.create(receiver=receiver,
                                            message="reply to your comment or reply: " + str(reply['object_id']))
        receiver.get_notified()

        return Response({"sucess", "replied"}, status=status.HTTP_201_CREATED)