from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Reservation, Hotel, HotelAvailability, Notification
from ..serializers import ReservationSerializer, UpdateReservationSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied


class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Reservation.objects.all()
        user_type = self.request.query_params.get('user_type')

        if user_type:
            if user_type == 'host':
                # queryset = queryset.filter(user__is_host=True)
                queryset = self.queryset.filter(hotel__owner=self.request.user)
            elif user_type == 'guest':
                queryset = self.queryset.filter(guest=self.request.user)
        state = self.request.query_params.get('state')
        if state:
            queryset = self.queryset.filter(state=state)
        print(queryset)
        return queryset


class ReservationReserve(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        print('start create')
        hotel_id = request.data.get('hotel')
        hotel = get_object_or_404(Hotel, id=hotel_id)

        validated_data = request.data.copy()
        validated_data['hotel'] = hotel.id
        validated_data['guest'] = request.user.id
        validated_data['state'] = 'P'

        # create and return the reservation object
        serializer = self.get_serializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        Notification.objects.create(sender=self.request.user, receiver=hotel.owner,
                                    message='Someone reserve you property')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     hotel = get_object_or_404(Hotel, id= request.data["id"])
    #     if request.user == hotel.owner:
    #         return Response({"detail": "You cannot reserve a room in your own hotel."}, status=status.HTTP_403_FORBIDDEN)
    #     if serializer.is_valid():
    #         serializer.save(guest=request.user)
    #         serializer.save(hotel=hotel)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationApprove(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateReservationSerializer
    queryset = Reservation.objects.all()

    def get_object(self):
        reservation = get_object_or_404(Reservation, id=self.kwargs['pk'])
        return reservation

    def perform_update(self, serializer):
        reservation = self.get_object()
        if reservation.hotel.owner != self.request.user:
            return PermissionDenied('You do not have permission to approve the reservation')
        Notification.objects.create(sender=self.request.user, receiver=reservation.guest,
                                    message='Your reservation is approved.')
        # reservation.state = 'A'
        print(reservation)
        serializer.save(state='A')

    # def put(self, request, pk):
    #     user = self.request.user
    #     reservation = get_object_or_404(Reservation, pk=pk)
    #     serializer = ReservationSerializer(data=request.data)
    #     if user.is_host and reservation.is_pending:
    #         reservation.approve()
    #     elif reservation.is_pending:
    #         reservation.cancel()
    #     return Response(serializer.data)


class ReservationDeny(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateReservationSerializer
    queryset = Reservation.objects.all()

    def get_object(self):
        reservation = get_object_or_404(Reservation, id=self.kwargs['pk'])
        return reservation

    def perform_update(self, serializer):
        reservation = self.get_object()
        if reservation.hotel.owner != self.request.user:
            return PermissionDenied('You do not have permission to deny the reservation')
        Notification.objects.create(sender=self.request.user, receiver=reservation.guest,
                                    message='Your reservation is denied.')
        # reservation.deny()
        # reservation.state = 'D'
        print(reservation)
        serializer.save(state='D')

    # def put(self, request, pk):
    #     serializer = ReservationSerializer(data=request.data)
    #     reservation = get_object_or_404(serializer.data, pk=pk)
    #     reservation.deny()
    #     serializer = ReservationSerializer(reservation)
    #     return Response(serializer.data)


class ReservationRequestCancel(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateReservationSerializer

    def get_object(self):
        reservation = get_object_or_404(Reservation, id=self.kwargs['pk'])
        return reservation

    def perform_update(self, serializer):
        reservation = self.get_object()
        if reservation.guest != self.request.user:
            return PermissionDenied('You do not have permission to cancel the reservation')
        Notification.objects.create(sender=self.request.user, receiver=reservation.hotel.owner,
                                    message='Someone cancel reservation.')
        reservation.request_cancel()
        print(reservation)
        serializer.save(state='PC')

    # def put(self, request, pk):
    #     reservation = get_object_or_404(Reservation, pk=pk)
    #     serializer = ReservationSerializer(data=request.data)
    #     if reservation.guest != self.request.user:
    #         return PermissionDenied('You do not have permission to cancel the reservation')
    #     # if request.user.is_guest:
    #     #     reservation.cancel()
    #     Notification.objects.create(sender=self.request.user, receiver=reservation.hotel.owner, detail='Someone cancel reservation.')
    #     return Response(serializer.data)


class ReservationApproveCancel(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateReservationSerializer

    def get_object(self):
        reservation = get_object_or_404(Reservation, id=self.kwargs['pk'])
        return reservation

    def perform_update(self, serializer):
        reservation = self.get_object()
        if reservation.hotel.owner != self.request.user:
            return PermissionDenied('You do not have permission to approve the cancel')
        Notification.objects.create(sender=self.request.user, receiver=reservation.guest,
                                    message='Your request to cancel the reservation is approved.')
        reservation.approve_cancel()
        print(reservation)
        serializer.save(state='Ca')


class ReservationDenyCancel(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateReservationSerializer

    def get_object(self):
        reservation = get_object_or_404(Reservation, id=self.kwargs['pk'])
        return reservation

    def perform_update(self, serializer):
        reservation = self.get_object()
        if reservation.hotel.owner != self.request.user:
            return PermissionDenied('You do not have permission to deny the cancel')
        Notification.objects.create(sender=self.request.user, receiver=reservation.guest,
                                    message='Your request to cancel is denied.')
        reservation.deny_cancel()
        print(reservation)
        serializer.save(state='A')


class ReservationTerminate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateReservationSerializer

    def get_object(self):
        reservation = get_object_or_404(Reservation, id=self.kwargs['pk'])
        return reservation

    def perform_update(self, serializer):
        reservation = self.get_object()
        if reservation.hotel.owner != self.request.user:
            return PermissionDenied('You do not have permission to terminate the reservation')
        Notification.objects.create(sender=self.request.user, receiver=reservation.guest,
                                    message='Your reservation is Terminated.')
        reservation.terminate()
        print(reservation)
        serializer.save(state='T')

    # def put(self, request, pk):
    #     reservation = get_object_or_404(Reservation, pk=pk)
    #     reservation.terminate()
    #     serializer = ReservationSerializer(reservation)
    #     return Response(serializer.data)
