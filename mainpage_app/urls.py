from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # 루트 URL에서 대시보드 데이터를 보여줌
    path(
        "update-dashboard/", views.update_dashboard, name="update_dashboard"
    ),  # AJAX 요청을 처리할 URL
]
