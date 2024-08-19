from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mainpage_app.urls")),
    path("weather/", include("weather_app.urls")),
    path("keyword/", include("keyword_app.urls")),
    path("visitor_region/", include("visitor_region_app.urls")),
    path("visitor_jeju/", include("visitor_jeju_app.urls")),
    path("visitor_changing/", include("visitor_changing_app.urls")),
    path("consumption_region/", include("consumption_region_app.urls")),
    path("consumption_industry/", include("consumption_industry_app.urls")),
    path("map/", include("map_app.urls")),
]
