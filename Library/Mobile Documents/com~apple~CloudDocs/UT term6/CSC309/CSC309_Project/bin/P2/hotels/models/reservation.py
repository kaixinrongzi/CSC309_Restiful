from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User
from .hotel import Hotel
# import sys
# sys.path.append('bin/P2/')
# from accounts.models import MyUser
import sys

sys.path.append('...')
import accounts


class Reservation(models.Model):
    STATUS = [
        ('A', 'Approved'),
        ('P', 'Pending'),
        ('Ca', 'Cancelled'),
        ('D', 'Denied'),
        ('E', 'Expired'),
        ('T', 'Terminated'),
        ('F', 'Finished'),
    ]
    guest = models.ForeignKey(accounts.models.MyUser, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    state = models.CharField(choices=STATUS)
