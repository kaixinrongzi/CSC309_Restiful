from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User
# import sys
# sys.path.append('bin/P2/')
# from accounts.models import MyUser
import sys
sys.path.append('...')
import accounts


class Notification(models.Model):
    receiver = models.ForeignKey(accounts.models.MyUser, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(null=True, blank=True)
    message = models.TextField()

    def get_map(self):
        return {"receiver": self.receiver,
                "read": self.read,
                "date": self.date,
                "message": self.message}