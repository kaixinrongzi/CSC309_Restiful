from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Reservation, Hotel, HotelAvailability
from ..serializers import ReservationSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated


class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        user_type = self.request.query_params.get('user_type')
        if user_type:
            if user_type == 'host':
                queryset = queryset.filter(user__is_host=True)
            elif user_type == 'guest':
                queryset = queryset.filter(user__is_guest=True)
        state = self.request.query_params.get('state')
        if state:
            queryset = queryset.filter(state=state)
        return queryset

class ReservationReserve(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        room = get_object_or_404(Hotel, id= request.data["id"])
        if request.user == room.host:
            return Response({"detail": "You cannot reserve a room in your own hotel."}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationCancel(generics.UpdateAPIView):
    def put(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = ReservationSerializer(data=request.data)
        if request.user.is_guest:
            reservation.cancel()
        return Response(serializer.data)


class ReservationApprove(APIView):
    def put(self, request, pk):
        user = self.request.user
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = ReservationSerializer(data=request.data)
        if user.is_host and reservation.is_pending:
            reservation.approve()
        elif reservation.is_pending:
            reservation.cancel()
        return Response(serializer.data)

class ReservationDeny(APIView):
    def put(self, request, pk):
        serializer = ReservationSerializer(data=request.data)
        reservation = get_object_or_404(serializer.data, pk=pk)
        reservation.deny()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

class ReservationTerminate(APIView):
    def put(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.terminate()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

