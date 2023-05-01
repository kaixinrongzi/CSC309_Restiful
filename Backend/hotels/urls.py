from django.urls import include, path
from .views.hotel_view import *
from .views.reservation_view import *
from .views.comment_view import *
from .views.notification_view import *
from .views.reply_view import *

app_name = 'hotels'
urlpatterns = [
    path('view/', ViewHotel.as_view(), name="viewhotels"),
    path('add/', AddHotel.as_view(), name="addhotel"),
    path('<int:pk>/view/', HotelDetail, name='hoteldetail'),
    path('add/<int:pk>/availability/', AddAvailability.as_view(), name="addavailability"),
    path('<int:pk>/update/', UpdateHotel.as_view(), name="updatehotel"),
    path('update/<int:pk>/availability/', UpdateAvailability.as_view(), name='updateavailability'),
    path('<int:pk>/delete/', DeleteHotel.as_view(), name='deletehotel'),
    path('search/', SearchHotel.as_view(), name='searchhotel'),
    path('search/availability/', SearchHotelAvailability.as_view(), name='hotelavailability'),
    path('reservation/list/', ReservationList.as_view(), name='reservationlist'),
    path('reservation/<int:pk>/approve/', ReservationApprove.as_view(), name='reservation_approve'),
    path('reservation/<int:pk>/deny/', ReservationDeny.as_view(), name='reservation_deny'),
    path('reservation/<int:pk>/terminate/', ReservationTerminate.as_view(), name='reservation_terminate'),
    path('reservation/<int:pk>/cancel/', ReservationRequestCancel.as_view(), name='reservation_cancel'),
    path('reservation/<int:pk>/approvecancel/', ReservationApproveCancel.as_view(), name='reservation_approvecancel'), # approve the cancellation
    path('reservation/<int:pk>/denycancel/', ReservationDenyCancel.as_view(), name='reservation_denycancel'), # deny the cancellation
    path('reservation/reserve/', ReservationReserve.as_view(), name='reservation_create'),
    path('reservation/<int:pk>/finish/', ReservationFinish.as_view(), name='reservation_finish'),
    path('comment/add/', AddComment.as_view(), name="addcomment"),
    path('comments/view/', GetComments.as_view(), name='viewcomments'),
    path('comment/<int:pk>/view/', GetComment.as_view(), name='viewcomments'),
    path('comment/<int:pk>/delete/', DeleteComment.as_view(), name='deletecomments'),
    path('notifications/view/', NotificationsViewAll.as_view(), name='viewallnotifications'),
    path('notifications/<int:pk>/view/', NotificationView.as_view(), name='viewnotification'),
    path('reply/add/', ReplyAdd.as_view(), name='addreply'),
    path('reply/<int:pk>/view/', ReplyView.as_view(), name='viewreply'),
    path('hotel/<int:pk>/comments/view/', GetCommentsforHotel.as_view(), name='viewcommentsforhotel'),
    path('commentsforme/view/', GetCommentsforMyself.as_view(), name='viewcommentsformyself'),
    path('commentforme/<int:pk>/view/', GetCommentforMyself.as_view(), name='viewcommentformyself')
]






