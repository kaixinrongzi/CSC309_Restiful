from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

# def default_available_date():
#     return date.today() + timedelta(days=30)

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='owner', null=True)
    address = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidatior(0), MaxValueValidator(5)])
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    beds = models.IntegerField(validators=[MinValueValidator(0)])
    baths = models.IntegerField(validators=[MinValueValidator(0)])
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.name}"

class HotelAvailability(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = model.DecimalField(decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.hotel} available from {self.start_date} to {self.end_date}"


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