from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_consumption_industry_data, name='display_consumption_industry_data'),
]
