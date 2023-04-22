from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
# Create your views here.

# make by guest, result pending
class AddReservation(CreateAPIView):
    pass

# made by guest, result cancelled
class CancelReservation(UpdateAPIView):
    pass

# made by host, result approved
class ApproveReservation(UpdateAPIView):
    pass

# made by host, result denied
class DenyReservation(UpdateAPIView):
    pass

# made by host, before approved, result terminated
class TerminateReservation(UpdateAPIView):
    pass

# made by host, before approved, result finished
class CompleteReservation(UpdateAPIView):
    pass

# how to add expired???