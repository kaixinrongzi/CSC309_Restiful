from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import PermissionDenied
from ..serializers import HotelSerializer, HotelAvailabilitySerializer
from ..models import Hotel, HotelAvailability
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
# Create your views here.
# from django.contrib.auth.models import User as MyUser

class AddHotel(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class AddAvailability(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelAvailabilitySerializer

    def perform_create(self, serializer):
        hotel_id = self.kwargs['pk']
        hotel = get_object_or_404(Hotel.objects.all(), pk=hotel_id)
        print(hotel)

        serializer.save(hotel=hotel)

    # def create(self, request, *args, **kwargs):
    #     hotel_id = self.kwargs['pk']
    #     hotel = get_object_or_404(Hotel.objects.all(), pk=hotel_id)
    #     print(hotel)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(hotel=hotel)
    #     headers = self.get_success_headers(serializer.data)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# class deleteavailability

# view hotel detail and update. 
class UpdateHotel(RetrieveAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer

    def get_object(self):
        obj = get_object_or_404(Hotel, id=self.kwargs['pk'])
        return obj

    def perform_update(self, serializer):
        hotel = self.get_object()
        print(hotel)
        print(hotel.owner)
        print(self.request.user)
        if hotel.owner != self.request.user:
            raise PermissionDenied('You do not have the permission to update the hotel')
        serializer.save()


# class AllHotel(ListAPIView):
#     serializer_class = HotelSerializer
class UpdateAvailability(RetrieveAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelAvailabilitySerializer

    def get_object(self):
        obj = get_object_or_404(HotelAvailability, id=self.kwargs['pk'])
        return obj

    def perform_update(self, serializer):
        hotel_availability = self.get_object()
        hotel = hotel_availability.hotel

        if hotel.owner != self.request.user:
            raise PermissionDenied('You do not have the permission to update the hotel')
        # availability_serializer = self.get_serializer(hotel_availability, data=request.data, partial=True)
        # availability_serializer.is_valid(raise_exception=True)
        serializer.save()

class SearchHotelAvailability(ListAPIView):
    serializer_class = HotelAvailabilitySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        print(self.request.query_params)
        hotel_id = self.request.query_params.get('hotel_id', None)
        start = self.request.query_params.get('start_date', None)
        end = self.request.query_params.get('end_date', None)
        max_price = self.request.query_params.get('price', None)
        print(hotel_id, start, end, max_price)
        query = HotelAvailability.objects.all()
        print(query)
        obj = HotelAvailability.objects.all().first()
        if start and end:
            query = query.filter(start_date__lte=start)
            query = query.filter(end_date__gte=end)
        if max_price:
            query = query.filter(price__lte=max_price)
        if hotel_id:
            query = query.filter(hotel=hotel_id)
        # print(query.values('hotel__id'))
        return query
        # return query.values('hotel__id', 'hotel__name', 'hotel__address', 'hotel__description', 'hotel__rating', 'hotel__capacity', 'hotel__beds', 'hotel__baths').distinct()
        # return query.values_list('hotel')

# filter and order
class SearchHotel(ListAPIView):
    serializer_class = HotelSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'rating', 'capacity']

    def get_queryset(self):
        # query_before = super().get_queryset()
        # print(query_before)
        # query = query_before.values('hotel__id', 'hotel__name', 'hotel__address', 'hotel__description', 'hotel__rating', 'hotel__capacity', 'hotel__beds', 'hotel__baths').distinct()
        # print(query)
        query = Hotel.objects.all()
        address = self.request.query_params.get('address', None)
        capacity = self.request.query_params.get('capacity', None)
        beds = self.request.query_params.get('beds', None)
        baths = self.request.query_params.get('baths', None)
        order_by = self.request.query_params.get('ordering', None)
        
        if address:
            query = query.filter(address__icontains=address)
        if capacity:
            query = query.filter(capacity__gte=capacity)
        if beds:
            query = query.filter(beds__gte=beds)
        if baths:
            query = query.filter(baths__gte=baths)
        if order_by:
            query = query.order_by(order_by)
        query = query.distinct()
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


class ViewHotel(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HotelSerializer

    def get_queryset(self):
        hotels = Hotel.objects.filter(owner=self.request.user)
        print(hotels)
        return hotels