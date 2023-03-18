"""P2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import UsersCreate, UsersUpdate, UsersLogin, UsersLogout, UsersProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", UsersCreate.as_view(), name="register"),
    path("token/api/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('login/', UsersLogin.as_view(), name='login'),
    path("profile/update/", UsersUpdate.as_view(), name="update"),
    path("logout/", UsersLogout.as_view(), name="logout"),
    path("profile/view/", UsersProfileView.as_view(), name="view")
]
