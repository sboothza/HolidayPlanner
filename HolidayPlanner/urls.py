
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from HolidayPlanner.HolidayPlanner.views import CustomerViewSet, CityViewSet, ScheduleViewSet, StopViewSet, WeatherView

router = DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'city', CityViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'stop', StopViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('weather/', WeatherView.as_view(), name="weather")
]
