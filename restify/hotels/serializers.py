from rest_framework.serializers import ModelSerializer
from .models import Hotel, HotelAvailability, Comment

class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'description', 'capacity', 'beds', 'baths', 'rating']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content_type', 'content_object', 'rating', 'detail']

class FollowComment1(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['rating']
        
# class FollowComment2(ModelSerializer):
#     class Meta:
#         model = Comment
#         exclude = ['rating']