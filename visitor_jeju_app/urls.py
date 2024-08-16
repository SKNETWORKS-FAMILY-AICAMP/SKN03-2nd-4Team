from django.urls import path
from .views import display_visitor_data

urlpatterns = [
    path('', display_visitor_data, name='display_visitor_data'),
]
