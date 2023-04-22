from django.contrib import admin
from . import models
# from .models import Hotel, HotelAvailability, Comment, Notification, Reservation

# Register your models here.
admin.site.register(models.Comment)
admin.site.register(models.Hotel)
admin.site.register(models.HotelAvailability)
admin.site.register(models.Notification)
admin.site.register(models.Reservation)
