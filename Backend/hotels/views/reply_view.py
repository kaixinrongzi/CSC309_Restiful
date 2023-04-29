from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from ..serializers import ReplySerializer, NotificationSerializer
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

        if 'reply_to' not in reply or reply['reply_to'] == '':
            reply_to = ''
        else:
            reply_to = reply['reply_to']

        if 'object_id' not in reply or reply['object_id'] == '':
            object_id = ''
        else:
            object_id = reply['object_id']

        if 'detail' not in reply or reply['detail'] == '':
            detail = ''
        else:
            detail = reply['detail']

        ordinary_dict = {'reply_to': reply_to,
                         'object_id': object_id,
                         'author': author.id,
                         'detail': detail}

        QueryDict('', mutable=True).update(ordinary_dict)
        serializer = self.get_serializer(data=ordinary_dict)
        serializer.is_valid(raise_exception=True)
        reply_obj = serializer.save()

        # find out who it is replying to
        if reply_to == '11' or reply_to == 11:  # reply to a comment
            try:
                comment = Comment.objects.get(id=object_id)
                receiver = comment.author

                # create notification
                notif_data = {'receiver': receiver.id,
                              'message': "a reply to your comment " + str(comment.id),
                              'content_type': 12,
                              'object_id': reply_obj.id}

                notif_serializer = NotificationSerializer(data=notif_data)

                if notif_serializer.is_valid(raise_exception=True):
                    notif_serializer.save()
                    receiver.get_notified()

                else:
                    return Response({"error": "no choice for content_type"}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                print(e)
                return Response({"error": "The comment you are replying to does not exist"},
                            status=status.HTTP_403_FORBIDDEN)

        if reply_to == '12' or reply_to == 12:  # reply to a reply
            try:
                reply = Reply.objects.get(id=reply['object_id'])
                receiver = reply.author
                # create notification
                notif_data = {'receiver': receiver.id,
                              'message': "a reply to your reply " + reply.id,
                              'content_type': 12,
                              'object_id': reply_obj.id}

                notif_serializer = NotificationSerializer(data=notif_data)
                if notif_serializer.is_valid(raise_exception=True):
                    notif_serializer.save()
                    receiver.get_notified()
                else:
                    return Response({"error": "no choice for content_type"}, status=status.HTTP_403_FORBIDDEN)
            except:
                return Response({"error": "The reply you are replying to does not exist"},
                                status=status.HTTP_403_FORBIDDEN)


        return Response({"sucess", "replied"}, status=status.HTTP_201_CREATED)


class ReplyView(RetrieveAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        reply = get_object_or_404(Reply, id=self.kwargs['pk'])
        return reply
