from django.urls import path
from .views import map_view, new_page1

urlpatterns = [
    path('', map_view, name='display_weather_data'),
    path('new_page1/', new_page1, name='new_page1'),
]
