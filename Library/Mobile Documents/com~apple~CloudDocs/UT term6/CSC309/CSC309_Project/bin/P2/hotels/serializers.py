from rest_framework.serializers import ModelSerializer
from django.contrib.contenttypes.models import ContentType
# import sys
# sys.path.append('bin/P2/')
# from ..models.hotelavailability import HotelAvailability
# from ..models.comment import Comment
# from ..models.reservation import Reservation
# from ..models.notification import Notification
from .models import *


class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'description', 'capacity', 'beds', 'baths', 'rating']


class HotelAvailabilitySerializer(ModelSerializer):
    class Meta:
        model = HotelAvailability
        fields = ['id', 'hotels', 'start_date', 'end_date', 'price']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['rating', 'detail', 'author']

    # def create(self, validated_data):
    #     oi = self.context['request'].data['object_id']
    #     ct = self.context['request'].data['content_type']
    #     validated_data['object_id'] = oi
    #     validated_data['content_type'] = ContentType.objects.get(model=ct)
    #
    #     if not validated_data.get('author'):
    #         validated_data['author'] = self.request.User
    #     return super().create(validated_data)


# class FollowComment1(ModelSerializer):
#     class Meta:
#         model = Comment
#         exclude = ['rating']

# class FollowComment2(ModelSerializer):
#     class Meta:
#         model = Comment
#         exclude = ['rating']

class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationViewSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
