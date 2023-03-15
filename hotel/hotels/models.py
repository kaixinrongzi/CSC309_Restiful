from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    avaliable_data = models.DateField()  # to do
    detail = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='owner', null=True)
    address = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidatior(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.name}"

# content_type=ContentType.objects.get_for_model(Hotel)
# one for hote, one for customer
# object_id=hotel.id
class Comment(models.Model):
    comment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    comment_object = GenericForeignKey('content_type', 'object_id')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    detail = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.detail}"