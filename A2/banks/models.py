from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Bank(models.Model):
    # TODO: to add fields
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    inst_num = models.CharField(max_length=200)
    swift_code = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="owner", null=True)

    def __str__(self):
        return self.name + str(self.pk)


class Branch(models.Model):
    name = models.CharField(max_length=200)
    transit_num = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True, default="admin@utoronto.ca")
    capacity = models.PositiveIntegerField(null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="branches", null=True)
    last_modified = models.DateTimeField(default=timezone.now, null=True, blank=True)







