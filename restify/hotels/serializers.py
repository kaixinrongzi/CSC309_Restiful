from rest_framework.serializers import ModelSerializer, IntegerField
from django.contrib.contenttypes.models import ContentType
from .models import Hotel, HotelAvailability, Comment, Reservation, Notification

class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'description', 'capacity', 'beds', 'baths', 'rating', 'owner']

        # def create(self, validated_data):
        #     print(self.context['request'].user)
        #     return super().create(validated_data)

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
        fields = ['rating', 'detail', 'author']

    def create(self, validated_date):
        oi = self.context['request'].data['object_id']
        ct = self.context['request'].data['content_type']
        validated_data['object_id'] = oi
        validated_data['content_type'] = ContentType.objects.get(model=ct)

        if not validated_data.get('author'):
            validated_date['author'] = self.request.User
        return super().create(validated_data)


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
