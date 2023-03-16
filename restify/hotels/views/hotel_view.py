from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
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
    pass

class DeleteHotel(DestroyAPIView):
    permission_class = [IsAuthenticated]
    serializer_class = HotelSerializer

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete the property")

        instance.delete()

    def get_object(self):
        hotel = get_object_or_404(Hotel.objects.all(), pk=self.kwargs['pk'])
        return hotel