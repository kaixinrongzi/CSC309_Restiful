from django.urls import include, path
# from .views import 

app_name = 'hotels'
url_patterns = [
    path('add/', AddHotel.as_view(), name="addhotel"),
]