from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
# Create your views here.

class AddHotel(CreateAPIView):
    pass

class AllHotel(ListAPIView):
    pass

# filter and order by
class SearchHotel(ListAPIView):
    pass

class DeleteHotel(DestroyAPIView):
    pass