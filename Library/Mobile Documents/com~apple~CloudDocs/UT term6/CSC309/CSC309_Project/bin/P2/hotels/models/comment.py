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


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    detail = models.CharField(max_length=1000)
    author = models.ForeignKey(accounts.models.MyUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.detail}"