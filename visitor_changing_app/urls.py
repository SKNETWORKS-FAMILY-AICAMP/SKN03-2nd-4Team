from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_visitor_changing_data, name='display_visitor_changing_data'),
]
