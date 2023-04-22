from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .forms import UserSerializer, UserLoginSerializer
from .models import MyUser
# from django.contrib.auth.models import UserProfile


# Create your views here.
class UsersCreate(CreateAPIView):
    serializer_class = UserSerializer
    queryset = MyUser.objects.all()

    def get(self, request, *args, **kwargs):
        return Response({"username": 'please enter your username',
                         'password': 'please enter your password',
                         'email': 'please enter your email',
                         'phone_number': 'please enter your phone number'})

    def create(self, request, *args, **kwargs):
        print("to create")
        new_user = request.data
        print(new_user)
        serializer = self.get_serializer(data=new_user)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()    # save the user
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UsersLogin(ListAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLoginSerializer

    # def get(self, request):
    #     return Response({"username": "username", "password": "password"})

    # def post(self, request):
    #     user = request.data
    #     serializer = self.get_serializer(data=user)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()  # save the user
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def create(self, request, *args, **kwargs):
    #     print("to login")

    def retrieve(self):
        user = self.request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.data
        if user == {}:
            return None
        username = user['username']
        password = user['password']
        return MyUser.objects.filter(username=username, password=password)

    # def create(self, request, *args, **kwargs):
    #     print("to login")
    #     user = request.data
    #     # check if the user exists in the model
    #     username = user['username']
    #     password = user['password']
    #     serializer = self.get_serializer(data=user)
    #     user = MyUsers.objects.filter(username=username,password=password).first()
    #     if user is None:
    #
    #     serializer.is_valid(raise_exception=True)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
