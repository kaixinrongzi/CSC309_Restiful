from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import login, logout, authenticate
from django.http import QueryDict
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .serializer import UserSerializer, UserLoginSerializer, UserUpdateSerializer
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
        new_user = request.data
        serializer = self.get_serializer(data=new_user)
        serializer.is_valid(raise_exception=True)
        print("29")
        self.perform_create(serializer)
        # new_user = MyUser.objects.create_user(new_user["username"], new_user["password"], new_user["email"], new_user["phone_number"])
        # new_user.save()
        # serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UsersLogin(ListAPIView):
    serializer_class = UserLoginSerializer
   

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request):
        login_user = request.data
        print(login_user)
        username = login_user['username']
        password = login_user['password']
        # print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            return Response({"error": "Invalid combination of username and password"})
        login(request, user)

        response = {
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number
        }

        return Response(response, status=status.HTTP_200_OK)


# class UsersLogin(ListAPIView, CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UserLoginSerializer

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

# def retrieve(self):
#     user = self.request.data
#     serializer = self.get_serializer(data=user)
#     serializer.is_valid(raise_exception=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
# def get_queryset(self):
#     user = self.request.data
#     if user == {}:
#         return None
#     username = user['username']
#     password = user['password']
#     return MyUser.objects.filter(username=username, password=password)

# def create(self, request, *args, **kwargs):
#     print("to login")
#     user = request.data
#     # check if the user exists in the model
#     username = user['username']
#     password = user['password']
#     serializer = self.get_serializer(data=user)
#     user = MyUser.objects.filter(username=username,password=password).first()
#     if user is None:
#
#     serializer.is_valid(raise_exception=True)
#     headers = self.get_success_headers(serializer.data)
#     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UsersUpdate(UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]

    # authentication_classes = (TokenAuthentication)

    def update(self, request, *args, **kwargs):
        user = request.user
        exist_user = MyUser.objects.filter(username=request.data['username']).first()
        print('exist_user:', exist_user)
        if user.username != request.data['username'] and exist_user is not None:
            return Response({"message": "failed", "details": 'username already exists'})

        # user = MyUser.objects.get(pk=user.pk)
        # delete = False
        # if user.username == request.data['username']:  # keeps the new username
        #     user.delete()
        #     self.destroy(request)
        #     print("delete_user")
        #     delete = True
        # if delete:
        #     user = request.user

        data = request.data
        username_change = True
        ordinary_dict = {'username': request.data['username'],
                         'password': request.data['password'],
                         'email': request.data['email'],
                         'phone_number': request.data['phone_number']}
        if user.username == request.data['username']:  # keep the username
            print("no change for the username")
            ordinary_dict.pop('username')
            # query_dict = QueryDict('', mutable=True)
            # query_dict.update(ordinary_dict)
            # data = ordinary_dict
            username_change = False

        email_change = True
        if user.email == request.data['email']:  # keep the email
            print("no change for the email")
            ordinary_dict.pop('email')
            # query_dict = QueryDict('', mutable=True)
            # query_dict.update(ordinary_dict)
            # data = ordinary_dict
            email_change = False

        query_dict = QueryDict('', mutable=True)
        query_dict.update(ordinary_dict)
        data = ordinary_dict

        serializer = self.get_serializer(data=data, partial=True)
        # data = serializer.validate(request.data)
        # print(data)
        # else:
        #     if len(request.data['username']) > 120:
        #         return Response({"message": "failed", "details": 'username must contain no more than 120 characters'})
        #     if len(request.data['password']) > 120:
        #         return Response({"message": "failed", "details": 'password must contain no more than 120 characters'})
        #     try:
        #         validate_email(request.data['email'])
        #     except ValidationError as e:
        #         return Response({"message": "failed", "details": e})
        #     if (len(request.data['phone_number'])) > 20:
        #         return Response({"message": "failed", "details": 'phone number must contain no more than 20 characters'})
        # serializer = self.get_serializer(data=request.data)
        # print(serializer)
        # user.username = ''   # delete the user
        # print("user is deleted")
        if serializer.is_valid(raise_exception=True):
            print("valid")
            if not username_change or not email_change:
                # serializer = self.get_serializer(request.data)
                user = MyUser.objects.get(username=user.username)
                print("178")
                user.delete()
                if MyUser.objects.filter(username=request.user.username).first() is None:
                    print("delete successfully")
                else:
                    print("fail to delete")
                update_user = MyUser.objects.create_user(request.data['username'], request.data['password'],
                                                         request.data['email'], request.data['phone_number'])
                update_user.set_password(request.data['password'])
                user = update_user
                serializer = self.get_serializer(data=request.data, partial=True)
                if serializer.is_valid():
                    print("188")
                    serializer.save()
            else:
                serializer.save()
            # update_user = MyUser.objects.create_user(request.data['username'], request.data['password'], request.data['email'], request.data['phone_number'])
            # update_user.set_password(request.data['password'])
            # update_user.save()
            # user.username = request.data['username']
            # print("request.user:", request.user)
            # if delete:
            #     user = MyUser.objects.create_user(request.data['username'],
            #                                       request.data['password'],
            #                                       request.data['email'],
            #                                       request.data['phone_number'])
            user.save()
            return Response(user.get_map())
            # user.username = request.data['username']
            # user.set_password(request.data['username'])
            # user.email = request.data['email']
            # user.phone_number = request.data['phone_number']
            # user.save()
            # update serializer
        else:
            print("invalid")
            # user = request.user
            # user = MyUser.objects.create_user(user.username, user.password, user.email, user.phone_number)
            # user.save()
            # serializer2 = self.get_serializer(data=request.data)
            # serializer2.save()
            # user.username = request.data['username']
            # print("request.user:", request.user)
            # if delete:
            #     user = MyUser.objects.create_user(request.data['username'],
            #                                       request.data['password'],
            #                                       request.data['email'],
            #                                       request.data['phone_number'])
            #     user.save()
            # serializer = self.get_serializer(data=user.get_map(), partial=True)
            # serializer.save()
            return Response({"error": serializer.errors})

        # serializer.is_valid()
        # user = serializer.validated_data
        # print("user", user)
        # if serializer.is_valid():
        #     print("valid")
        #     # serializer.set_username = serializer.data['username']
        #     # serializer.set_password = serializer.data['password']
        #     # serializer.set_email = serializer.data['email']
        #     # serializer.set_phone_number = serializer.data['phone_number']
        #     # user.set_username = serializer.validated_data['username']
        #     # user.set_password = serializer.validated_data['password']
        #     # user.set_email = serializer.validated_data['email']
        #     # user.set_phone_number = serializer.validated_data['phone_number']
        #     # user.save()
        #     serializer.save()
        #     print(user.username, user.password, user.email, user.phone_number)
        #     return Response({"message": "user updated successfully",
        #                      "username": serializer.data['username'],
        #                      'email': serializer.data['email'],
        #                      'phone_number': serializer.data['phone_number']})
        # else:
        #     return Response({"message": "failed", "details": serializer.errors})

    def get_queryset(self):
        user = self.request.user
        print(user)
        return MyUser.objects.filter(username=user.username)

    def get(self, request, *args, **kwargs):
        print(request.user)
        return Response({"username": 'please enter your username',
                         'password': 'please enter your password',
                         'email': 'please enter your email',
                         'phone_number': 'please enter your phone number'})

    # def destroy(self, request, *args, **kwargs):
    #     user = request.user
    #     user_to_destroy = MyUser.objects.get(username=user.username)
    #     user_to_destroy.delete()
    #     print("succesfully delete")
    #     self.perform_destroy(user_to_destroy)


class UsersLogout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        logout(request)
        return Response({username: "logout"})


class UsersProfileView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self):
        user = self.request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        return MyUser.objects.filter(username=user.username)
