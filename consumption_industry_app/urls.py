from django.urls import path
from .views import display_consumption_industry_data

urlpatterns = [
    path('', display_consumption_industry_data, name='display_consumption_industry_data'),
]
