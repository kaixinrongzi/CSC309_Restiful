from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, Form
# from .models import MyUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


# class RegisterForm(ModelForm):
#     class Meta:
#         model = _User
#         fields = ['__all__']
#
#     def clean(self):
#         cleaned_data = super(RegisterForm, self).clean()
#         password1 = self.cleaned_data.get('password')
#         password2 = self.cleaned_data.get('password2')
#
#         if password1 != password2:

# Sign Up Form

class RegisterForm(UserCreationForm):    # UserCreationForm is a subclass of ModelForm
    email = forms.EmailField(required=False, max_length=120)
    first_name = forms.CharField(required=False, max_length=120)
    last_name = forms.CharField(required=False, max_length=120)

    class Meta:
        model = User
        # fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
        fields = ['username', 'password1', 'password2']
        # labels = {'username': "Username",
        #           'email': "Email",
        #           'first_name': "First Name",
        #           'last_name': "Last Name"}

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("username")
        password1 = cleaned.get("password1")
        # password2 = cleaned.get("password2")
        # email = cleaned.get("email")
        # first_name = cleaned.get("first_name")
        # last_name = cleaned.get("last_name")
        # if len(username) == '':
        #     raise ValidationError("A user with that username already exists")
        errors = {}
        if username is not None and len(username) > 120:
            errors["username"] = ["The username cannot contain more than 120 characters"]


        if password1 is not None and len(password1) < 8:
            errors["password1"] = ["This password is too short. It must contain at least 8 characters"]
        if password1 is not None and len(password1) > 120:
            if "password1" not in errors:
                errors["password1"].append("The password cannot contain more than 120 characters")
            else:
                errors["password1"]=["The password cannot contain more than 120 characters"]
        # if email is not None and len(email) > 120:
        #     errors["email"] = ["The email cannot contain more than 120 characters"]

        if errors != {}:
            raise ValidationError(errors)

        cleaned['user'] = cleaned
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()
        errors = {}
        if 'username' not in data or 'password' not in data:
            raise ValidationError({})
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError({
                "username": 'Username or password is invalid'}
            )
        data['user'] = user
        return data


class ProfileForm(ModelForm):    #对应{{ form }}
    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # email = forms.CharField()
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # labels = {'first_name': 'First Name',
        #           'last_name': 'Last Name',
        #           'email': "Email",}

    def clean(self):     # called when {{form}} in html is being rendered
        print("to clean")
        cleaned = super().clean()
        first_name = cleaned.get('first_name')
        last_name = cleaned.get('last_name')
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')
        email = cleaned.get('email')
        # if password1 == "":
        #     cleaned["user"] = cleaned
        #     return cleaned
        errors = {}
        if password1 != "":
            if password1 != password2:
                errors["password2"] = ["The two password fields didn't match"]
            if len(password1) > 120:
                errors["password1"] = ["The password cannot contain more than 120 characters"]
            if len(password1) < 8:
                if "password1" not in errors:
                    errors["password1"] = ["This password is too short. It must contain at least 8 characters"]
                else:
                    errors["password1"].append("This password is too short. It must contain at least 8 characters")
        # if email != "":
        #     try:
        #         validate_email(email)
        #     except ValidationError:
        #         errors["email"] = ["Enter a valid email address"]
        # if email is None:  #email is filtered but invalid
        #     errors["email"] = ["Enter a valid email address"]
        if email is not None and len(email) > 120:
            errors["email"] = ["The email cannot contain more than 120 characters"]

        if len(first_name) > 120:
            errors["first_name"] = ["The first_name cannot contain more than 120 characters"]
        if len(last_name) > 120:
            errors["last_name"] = ["The last_name cannot contain more than 120 characters"]

        if errors != {}:
            raise ValidationError(errors)
        else:
            cleaned["user"] = cleaned
            return cleaned


    # def is_valid(self):
    #     if cleaned['password1'] != cleaned['password2']:
    #         raise ValidationError("The two password fields didn't match")
    #     if len(cleaned['password1']) < 8:
    #         raise ValidationError("This password is too short. It must contain at least 8 characters")
    #     return True








