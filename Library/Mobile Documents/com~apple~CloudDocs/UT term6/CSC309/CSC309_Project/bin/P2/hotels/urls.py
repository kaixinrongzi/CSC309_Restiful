from django.urls import include, path
from .views.hotel_view import AddHotel, AddAvailability, UpdateHotel, UpdateAvailability, DeleteHotel
from .views.notification_view import NotificationsViewAll

# app_name = 'hotels'
urlpatterns = [

    path('notification/view/', NotificationsViewAll.as_view(), name='viewnotification'),
    path('add/', AddHotel.as_view(), name="addhotel"),
    path('add/<int:pk>/availability/', AddAvailability.as_view(), name="addavailability"),
    path('<int:pk>/update/', UpdateHotel.as_view(), name="updatehotel"),
    path('/update/<int:pk>/availability/', UpdateAvailability.as_view(), name='updateavailability'),
    path('<int:pk>/delete/', DeleteHotel.as_view(), name='deletehotel')
]


