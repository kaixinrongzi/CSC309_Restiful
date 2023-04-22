from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User
from .hotel import Hotel
# import sys
# sys.path.append('bin/P2/')
# from accounts.models import MyUser
from ... import accounts


class HotelAvailability(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(decimal_places=2, validators=[MinValueValidator(0)], max_digits=10000)

    def __str__(self):
        return f"{self.hotel} available from {self.start_date} to {self.end_date}"