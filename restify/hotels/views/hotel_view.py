from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class AddHotel(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer

# class AllHotel(ListAPIView):
#     serializer_class = HotelSerializer

# filter and order by
class SearchHotel(ListAPIView):
    serializer_class = HotelSerializer

    def get_query_set(self):

        Hotel.objects.filter()

class DeleteHotel(DestroyAPIView):
    permission_class = [IsAuthenticated]
    serializer_class = HotelSerializer

    def 