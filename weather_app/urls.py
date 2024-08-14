from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_weather_data, name='display_weather_data'),
]
