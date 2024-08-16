from django.urls import path
from .views import display_weather_data

urlpatterns = [
    path('', display_weather_data, name='display_weather_data'),
]
