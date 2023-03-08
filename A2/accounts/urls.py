from django.urls import path, include
from .views import UserRegister, UserLogin, UserLogout, UserProfileEdit, UserProfileView
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name="accounts"
urlpatterns = [
    path('register/', UserRegister.as_view(), name="register"),    # both get + post; get: template_name, post: form_valid
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('profile/view/', UserProfileView.as_view(), name="viewprofile"),
    path('profile/edit/', UserProfileEdit.as_view(), name="editprofile"),
    # path('reset-pwd/', PasswordResetView.as_view(), name="resetpwd"),
]