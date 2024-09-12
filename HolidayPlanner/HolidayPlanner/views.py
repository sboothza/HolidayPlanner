from django.db import connection
from django.http import Http404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from HolidayPlanner.HolidayPlanner.models import Customer, City, Schedule, Stop, Location
from HolidayPlanner.HolidayPlanner.serializers import CustomerSerializer, CitySerializer, ScheduleSerializer, StopSerializer
from HolidayPlanner.HolidayPlanner.weather_service import WeatherService


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]


class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    permission_classes = [permissions.IsAuthenticated]


class WeatherView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        schedule_id = request.query_params.get("schedule_id")
        print(schedule_id)
        if schedule_id is None:
            raise Http404

        sql = """select c.id as id, c.id as city_id, c.name as city_name, c.lat, c.long, st.date_arrive as start_date, st.date_leave as end_date 
from HolidayPlanner_schedule s
inner join HolidayPlanner_stop st
on st.schedule_id_id = s.id 
inner join HolidayPlanner_city c
on c.id  = st.city_id_id 
where s.id = %s"""

        # loc_query = Location.objects.raw(sql, [schedule_id])
        # print(loc_query)
        # locations = LocationSerializer(loc_query, many=True).data
        #
        # return locations

        with connection.cursor() as cursor:
            cursor.execute(sql, [schedule_id])
            loc_data = cursor.fetchall()
            # loc_query = Location.objects.raw(sql, [schedule_id])
            # print(loc_query)
            # locations = LocationSerializer(loc_data, many=True).data
            locations = []
            for loc in loc_data:
                obj = Location()
                obj.load(loc)
                locations.append(obj)

            weather = WeatherService()
            if len(locations) == 0:
                raise Http404
            weather_result = weather.get_forecast(locations)
            res = []
            for location in weather_result:
                dic = {k: v for (k, v) in location.__dict__.items() if
                       k in ["city_id", "city", "date", "code", "description", "temp_min", "temp_max", "precip", "precip_prob", "wind_speed", "wind_direction"]}
                res.append(dic)

            return Response(res)
