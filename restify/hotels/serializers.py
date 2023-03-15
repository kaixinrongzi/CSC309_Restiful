from rest_framework.serializers import ModelSerializer
from .models import Hotel, HotelAvailability, Comment

class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'detail', 'description', 'beds', 'baths', 'rating']

