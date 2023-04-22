from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User
from .comment import Comment
# import sys
# sys.path.append('bin/P2/')

import sys
sys.path.append('...')
import accounts
# from accounts.models import MyUser


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(accounts.models.MyUser, on_delete=models.SET_NULL, related_name='owner', null=True)
    address = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(5)])
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    beds = models.IntegerField(validators=[MinValueValidator(0)])
    baths = models.IntegerField(validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    comments = GenericRelation(Comment, related_query_name='hotels')

    def __str__(self):
        return f"{self.name}"