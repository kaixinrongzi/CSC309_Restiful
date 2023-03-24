from django.urls import include, path
from . import views

app_name = 'hotels'
urlpatterns = [
    path('add/', views.AddHotel.as_view(), name="addhotel"),
    path('add/<int:pk>/availability/', views.AddAvailability.as_view(), name="addavailability"),
    path('<int:pk>/update/', views.UpdateHotel.as_view(), name="updatehotel"),
    path('update/<int:pk>/availability/', views.UpdateAvailability.as_view(), name='updateavailability'),
    path('<int:pk>/delete/', views.DeleteHotel.as_view(), name='deletehotel'),
    path('search/', views.SearchHotel.as_view(), name='searchhotel'), 
    path('search/availability/', views.SearchHotelAvailability.as_view(), name='hotelavailability'),
    path('reservation/list/', views.ReservationList.as_view(), name='reservationlist'), 
    path('reservation/<int:pk>/approve/', views.ReservationApprove.as_view(), name='reservation_approve'), 
    path('reservation/<int:pk>/deny/', views.ReservationDeny.as_view(), name='reservation_deny'), 
    path('reservation/<int:pk>/terminate/', views.ReservationTerminate.as_view(), name='reservation_terminate'), 
    path('reservation/<int:pk>/cancel/', views.ReservationCancel.as_view(), name='reservation_cancel'),
    path('reservation/reserve/', views.ReservationReserve.as_view(), name='reservation_create'), 
    
]