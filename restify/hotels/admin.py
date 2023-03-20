from django.contrib import admin
from .models import Hotel, HotelAvailability, Comment, Notification, Reservation

# Register your models here.
admin.site.register(Hotel)
admin.site.register(HotelAvailability)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Reservation)