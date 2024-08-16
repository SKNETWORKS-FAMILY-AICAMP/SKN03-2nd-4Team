from django.urls import path
from .views import display_keyword_data

urlpatterns = [
    path('', display_keyword_data, name='display_keyword_data'),
]
