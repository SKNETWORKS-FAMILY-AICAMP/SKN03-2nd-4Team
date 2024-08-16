from django.urls import path
from .views import map_test_view

urlpatterns = [
    path('', map_test_view, name='get_location_data'),
]
