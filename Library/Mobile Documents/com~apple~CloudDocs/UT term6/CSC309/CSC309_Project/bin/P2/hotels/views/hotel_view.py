from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from ..serializers import HotelSerializer, HotelAvailabilitySerializer
from ..models import Hotel, HotelAvailability


# Create your views here.

class AddHotel(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer


class AddAvailability(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelAvailabilitySerializer

    def create(self, request, *args, **kwargs):
        hotel_id = self.kwargs['pk']
        hotel = get_object_or_404(Hotel.objects.all(), pk=hotel_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(hotel=hotel)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class deleteavailability

# view hotel detail and update.
class UpdateHotel(RetrieveAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer

    def get_object(self):
        obj = get_object_or_404(Hotel, id=elf.kwargs['pk'])
        return obj

    def update(self, request, *args, **kwargs):
        hotel = self.get_object()
        if hotel.owner != self.request.user:
            raise PermissionDenied('You do not have the permission to update the hotel')
        serializer = self.get_serializer(hotel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


# class AllHotel(ListAPIView):
#     serializer_class = HotelSerializer
class UpdateAvailability(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelAvailabilitySerializer

    def get_object(self):
        obj = get_object_or_404(HotelAvailability, id=self.kwargs['pk'])
        return obj

    def update(self, request, *args, **kwargs):
        hotel_availability = self.get_object()
        hotel = hotel_availability.hotel

        if hotel.owner != self.request.user:
            raise PermissionDenied('You do not have the permission to update the hotel')
        availability_serializer = self.get_serializer(hotel_availability, data=request.data, partial=True)
        availability_serializer.is_valid(raise_exception=True)
        availability_serializer.save()


class SearchHotelAvailability(ListAPIView):
    serializer_class = HotelAvailabilitySerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        query = HotelAvailability.objects.all()
        if start_date and end_date:
            query = query.filter(start_date__lte=start_date)
            query = query_filter(end_date__gte=end_date)
        return query.distinct('hotel').values('hotel__id', 'hotel__name', 'hotel__address', 'hotel__description',
                                              'hotel__rating', 'hotel__capacity', 'hotel__beds', 'hotel__baths')


# filter and order
class SearchHotel(ListAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self):
        query = super().get_queryset()
        address = self.request.query_params.get('address', None)
        capacity = self.request.query_params.get('capacity', None)
        beds = self.request.query_params.get('beds', None)
        baths = self.request.query_params.get('baths', None)

        if address:
            query.filter(address__icontains=address)
        if capacity:
            query.filter(capacity__gte=capacity)
        if beds:
            query.filter(beds__gte=beds)
        if baths:
            query.filter(baths__gte=baths)

        return query


class DeleteHotel(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete the property")

        instance.delete()

    def get_object(self):
        hotel = get_object_or_404(Hotel.objects.all(), pk=self.kwargs['pk'])
        return hotel