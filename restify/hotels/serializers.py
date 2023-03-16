from rest_framework.serializers import ModelSerializer
from .models import Hotel, HotelAvailability, Comment

class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'description', 'capacity', 'beds', 'baths', 'rating']

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


class FollowComment1(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['rating']
        
# class FollowComment2(ModelSerializer):
#     class Meta:
#         model = Comment
#         exclude = ['rating']