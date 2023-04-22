from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import NotificationSerializer
from ..models import Notification


class NotificationsCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer


class NotificationsViewAll(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)


class NotificationReadView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get(self, request):
        notif_id = request.get_full_path().split('/')[-1]
        notif = Notification.objects.get(id=notif_id)
        res = notif.get_map()
        notif.delete()
        self.destroy(request)

        return Response(notif.get_map(), status.HTTP_200_OK)
