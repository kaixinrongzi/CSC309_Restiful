from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import PermissionsMixin


# Create your models here.


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, email, phone_number, **extra_fields):
        values = [username, password, email, phone_number, extra_fields]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email, phone_number):
        print("create user")
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        extra_fields = {"is_staff": False, "is_active": True, "is_superuser": False}
        return self._create_user(username, password, email, phone_number, **extra_fields)

    def create_superuser(self, username, password, email, phone_number):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')
        extra_fields = {"is_staff": True, "is_active": True, "is_superuser": True}

        return self._create_user(username, password, email, phone_number, **extra_fields)


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=120, unique=True)
    password = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    rating = models.CharField(max_length=3, null=True, blank=True)
    comments = models.CharField(max_length=200, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    # booking_notification = models.BooleanField(default=False)
    # comment_notification = models.BooleanField(default=False)
    # rating_notification = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'email', 'phone_number']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username.split()[0]

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_map(self):
        return {"username: ": self.username,
                "password": self.password,
                "email": self.email,
                "phone_number": self.phone_number}

    def get_notified(self, notification_type):
        send_mail('new ' + notification_type,
                  'You have a new ' + notification_type,
                  'restiful@example.com',
                  [self.email])
