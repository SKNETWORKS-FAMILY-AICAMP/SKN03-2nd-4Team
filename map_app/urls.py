from django.urls import path
from .views import map_view

urlpatterns = [
    path('', map_view, name='display_weather_data'),
]
