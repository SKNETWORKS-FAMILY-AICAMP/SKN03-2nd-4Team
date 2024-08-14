from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_consumption_region_data, name='display_consumption_region_data'),
]
