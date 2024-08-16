from django.urls import path
from .views import display_consumption_region_data

app_name = 'consumption_region'
urlpatterns = [
    path('', display_consumption_region_data, name='display_consumption_region_data'),
]
