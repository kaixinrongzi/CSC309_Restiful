from django.db import models
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.forms import UserCreationForm
from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import MyUser


class UserSerializer(ModelSerializer):
    # phone_number = models.CharField(max_length=100)
    # rating = models.CharField(max_length=3)

    class Meta:
        model = MyUser
        fields = '__all__'

    def validate(self, data):
        print("to validate")
        password = data['password']
        username = data['username']
        # email = data['email']

        # check for username
        old_user = self.Meta.model.objects.filter(username=username).first()
        if old_user is not None:
            raise serializers.ValidationError({"username": 'username already used, please try a different one'})

        errors = {}
        allow_specials = ['@', '/', './', '+', '-', '_']
        alpha_count = 0
        number_count = 0
        for char in username:
            if char.isalpha():
                alpha_count += 1
                continue
            if char.isdigit():
                number_count += 1
                continue
            if char not in allow_specials:
                errors['username'] = ['username can only contains alpha, number, or special characters of @ / ./ + - _']
                # raise serializers.ValidationError({"username": 'username can only contains alpha, number, or special characters of @ / ./ + - _'})
        if alpha_count == 0 or number_count == 0:
            if username not in errors:
                errors['username'] = []
            errors['username'].append("username must contain at least one alpha and one number")
            # raise serializers.ValidationError({"username": "username must contain at least one alpha and one number"})

        # check for the password
        if len(password) < 8:
            errors['password'] = ['password cannot be shorter than 8 characters']
            # raise serializers.ValidationError({"password": 'password cannot be shorter than 8 characters'})
        # check for digit
        if not any(char.isdigit() for char in password):
            if 'password' not in errors:
                errors['password'] = []
            errors['password'].append('Password must contain at least 1 digit.')
            # raise serializers.ValidationError({"password": 'Password must contain at least 1 digit.'})
        # check for letter
        if not any(char.isalpha() for char in password):
            if 'password' not in errors:
                errors['password'] = []
            errors['password'].append('Password must contain at least 1 letter.')
            # raise serializers.ValidationError({'password': 'Password must contain at least 1 letter.'})

        if errors != {}:
            raise serializers.ValidationError(errors)

        return data


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'password']

    # def validate(self, data):
    #     username = data['username']
    #     password = data["password"]
    #

