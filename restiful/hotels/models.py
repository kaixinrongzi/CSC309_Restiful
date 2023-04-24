from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User as MyUser
import sys
sys.path.append('..')
from accounts.models import MyUser


# Create your models here.

# def default_available_date():
#     return date.today() + timedelta(days=30)

# content_type=ContentType.objects.get_for_model(Hotel)
# two types of comment, one from guest to property, another from host to guest
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    detail = models.CharField(max_length=1000)
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.detail}"


# class Comment(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
#     detail = models.CharField(max_length=1000)
#     author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.detail}"


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(MyUser, on_delete=models.SET_NULL, related_name='owner', null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    capacity = models.IntegerField(validators=[MinValueValidator(0)])
    beds = models.IntegerField(validators=[MinValueValidator(0)])
    baths = models.IntegerField(validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    comments = GenericRelation(Comment, related_query_name='hotel', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class HotelAvailability(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.hotel} available from {self.start_date} to {self.end_date}"


# Pending: the user makes a request to reserve a property on one or more consecutive dates.
# Denied: the host, i.e., the owner of the property, declines the reservation request.
# Expired: the host did not respond to a reservation request within a user-defined time window.
# Approved: the reservation request is approved.
# Canceled: the reservation was approved but later canceled by the user.
# Terminated: the reservation was approved but later canceled by the host.
# Finished: the reservation is realized, i.e., the user went to the property and stayed there.


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

    guest = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    state = models.CharField(choices=STATUS, max_length=100, default='P')
    guests = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"reservation {self.state} from {self.start_date} to {self.end_date} by {self.guest.username}"

    @property
    def is_host(self):
        return self.user.is_host

    @property
    def is_guest(self):
        return self.user.is_guest

    @property
    def is_pending(self):
        print("It is pending!")
        return self.state == 'P'

    @property
    def is_approved(self):
        return self.state == 'A'

    @property
    def is_denied(self):
        return self.state == 'D'

    @property
    def is_cancelled(self):
        return self.state == 'C'

    # @is_guest
    def reserve(self):
        self.state = 'P';
        self.save()

    # @is_guest
    def request_cancel(self):
        if self.is_approved:
            print('change to P')
            self.state = 'P'
        self.save()

    def approve_cancel(self):
        if self.is_pending:
            self.state = 'Ca'
        self.save()

    def deny_cancel(self):
        if self.is_pending:
            print('Deny cancel')
            self.state = 'A'
        self.save()

    # @is_host
    def approve(self):
        if self.is_pending:
            self.state = 'A'
        self.save()

    # @is_host
    def deny(self):
        if self.is_pending:
            self.state = 'D'
        self.save()

    # @is_host
    def terminate(self):
        if self.is_approved:
            self.state = 'T'
            self.save()


# class Notification(models.Model):
#     reciever = models.ForeignKey(MyUser, on_delete=models.CASCADE)
#     read = models.BooleanField(default=False)
#     date = models.DateTimeField(null=True, blank=True)


class Notification(models.Model):
    receiver = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(null=True, blank=True)
    message = models.TextField()

    def get_map(self):
        return {"receiver": self.receiver,
                "read": self.read,
                "date": self.date,
                "message": self.message}


class Reply(models.Model):
    reply_to = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    author = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    detail = models.TextField(max_length=200, null=True,  blank=True)



