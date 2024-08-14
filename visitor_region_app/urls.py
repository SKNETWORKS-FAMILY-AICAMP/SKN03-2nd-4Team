from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_visitor_region_data, name='display_vistor_region_data'),
]
