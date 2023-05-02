from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer
from .models import Hotel, HotelAvailability, Comment, Reservation, Notification, Reply
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'description', 'capacity', 'beds', 'baths', 'rating', 'owner', 'image1', 'image2', 'image3']


class HotelAvailabilitySerializer(ModelSerializer):
    beds = IntegerField(read_only=True, source='hotel.beds')
    baths = IntegerField(read_only=True, source='hotel.baths')

    class Meta:
        model = HotelAvailability
        # fields = '__all__'
        fields = ['id', 'hotel', 'start_date', 'end_date', 'price', 'beds', 'baths']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','rating', 'detail', 'author', 'receiver', 'content_type', 'object_id']

    def create(self, validated_data):
        oi = self.context['request'].data['object_id']
        ct = self.context['request'].data['content_type']
        validated_data['object_id'] = oi
        validated_data['content_type'] = ContentType.objects.get(model=ct)

        if not validated_data.get('author'):
            validated_data['author'] = self.request.User
        return super().create(validated_data)


class CommentAddSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content_type', 'object_id', 'rating', 'detail', 'author', 'receiver']

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


class UpdateReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['start_date', 'end_date']


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'
        # widgets = {
        #     'reply_to': serializers.ChoiceField(choices=ContentType.objects.all())
        # }
