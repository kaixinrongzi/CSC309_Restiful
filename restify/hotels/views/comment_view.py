from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class AddComment(CreateAPIView):
    permission_class = [IsAuthenticated]

class GetComment(ListAPIView):
    pass
# host reply to the public comment about his property. 
class FollowComment1(CreateAPIView):
    pass
# guest reply to the host's comment
class FollowComment2(CreateAPIView):
    pass
