from django.urls import path
from .views import display_visitor_region_data

urlpatterns = [
    path('', display_visitor_region_data, name='display_vistor_region_data'),
]
