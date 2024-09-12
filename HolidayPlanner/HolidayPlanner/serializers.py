from rest_framework import serializers

from HolidayPlanner.HolidayPlanner.models import Customer, City, Schedule, Stop, Weather, Location


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone", "create_date"]


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "lat", "long", "description", "create_date"]


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    customer_id = CustomerSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = ["id", "name", "customer_id", "create_date"]


class StopSerializer(serializers.HyperlinkedModelSerializer):
    schedule_id = ScheduleSerializer(many=True, read_only=True)
    city_id = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Stop
        fields = ["id", "schedule_id", "city_id", "date_arrive", "date_leave"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "city_id", "city_name", "lat", "long", "start_date", "end_date"]


class WeatherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather
        fields = ["city_id", "city", "date", "code", "description", "temp_min", "temp_max", "precip", "precip_prob", "wind_speed", "wind_direction"]
