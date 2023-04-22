from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import NotificationSerializer
from ..models import Notification


# class NotificationsCreateView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = NotificationSerializer


class NotificationsViewAll(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)


class NotificationView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        notif_id = self.kwargs['pk']
        returned_notification = Notification.objects.filter(id=notif_id)
        if not returned_notification:
            return returned_notification
        else:
            #delete the notification
            notification = returned_notification
            notification.first().delete()
            # unnotify the user
            self.request.user.get_unnotified()
            # notification.first().destroy()
            return returned_notification




