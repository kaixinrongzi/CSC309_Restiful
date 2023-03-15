from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
# Create your views here.

class AddComment(CreateAPIView):
    pass
class GetComment(ListAPIView):
    pass