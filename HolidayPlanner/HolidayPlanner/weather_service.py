import datetime
from typing import List

import requests
from rest_framework.response import Response

from HolidayPlanner.HolidayPlanner.models import Weather, Location


class WeatherService:
    base_url: str

    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast?latitude=%lat%&longitude=%long%&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant&start_date=%start%&end_date=%end%"
        self.codes = {0: "Clear sky",
                      1: "Mainly clear, partly cloudy, and overcast",
                      2: "Mainly clear, partly cloudy, and overcast",
                      3: "Mainly clear, partly cloudy, and overcast",
                      45: "Fog and depositing rime fog",
                      48: "Fog and depositing rime fog",
                      51: "Drizzle: Light, moderate, and dense intensity",
                      53: "Drizzle: Light, moderate, and dense intensity",
                      55: "Drizzle: Light, moderate, and dense intensity",
                      56: "Freezing Drizzle: Light and dense intensity",
                      57: "Freezing Drizzle: Light and dense intensity",
                      61: "Rain: Slight, moderate and heavy intensity",
                      63: "Rain: Slight, moderate and heavy intensity",
                      65: "Rain: Slight, moderate and heavy intensity",
                      66: "Freezing Rain: Light and heavy intensity",
                      67: "Freezing Rain: Light and heavy intensity",
                      71: "Snow fall: Slight, moderate, and heavy intensity",
                      73: "Snow fall: Slight, moderate, and heavy intensity",
                      75: "Snow fall: Slight, moderate, and heavy intensity",
                      77: "Snow grains",
                      80: "Rain showers: Slight, moderate, and violent",
                      81: "Rain showers: Slight, moderate, and violent",
                      82: "Rain showers: Slight, moderate, and violent",
                      85: "Snow showers slight and heavy",
                      86: "Snow showers slight and heavy",
                      95: "Thunderstorm: Slight or moderate",
                      96: "Thunderstorm with slight and heavy hail",
                      99: "Thunderstorm with slight and heavy hail"}

        self.cardinal_points = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    def _get_code(self, code: int) -> str:
        if code in self.codes:
            return self.codes[code]
        return self.codes[0]

    def _get_wind_direction(self, wind_direction: float) -> str:
        index = int((wind_direction / 22.5) + .5)
        return self.cardinal_points[(index % 16)]

    def parse_response(self, json, locations: List[Location]) -> List[Weather]:
        weather_days: List[Weather] = []
        for i, city in enumerate(json):
            city_data = city["daily"]
            num_days = len(city_data["time"])
            for d in range(num_days):
                if locations[i].start_date <= datetime.datetime.strptime(city_data["time"][d], "%Y-%m-%d") <= locations[i].end_date:
                    weather_day = Weather(locations[i].city_id, locations[i].city_name, city_data["time"][d], city_data["weather_code"][d],
                                          self._get_code(city_data["weather_code"][d]),
                                          city_data["temperature_2m_min"][d], city_data["temperature_2m_max"][d], city_data["precipitation_sum"][d],
                                          city_data["precipitation_probability_max"][d], city_data["wind_speed_10m_max"][d],
                                          self._get_wind_direction(city_data["wind_direction_10m_dominant"][d]))
                    weather_days.append(weather_day)
        return weather_days

    def get_forecast(self, locations: List[Location]) -> List[Weather] | None:
        start_date = min([location.start_date for location in locations])
        end_date = max([location.end_date for location in locations])

        lat = ",".join([str(location.lat) for location in locations])
        long = ",".join([str(location.long) for location in locations])
        url = self.base_url.replace("%lat%", lat).replace("%long%", long).replace("%start%", start_date.strftime("%Y-%m-%d")).replace("%end%",
                                                                                                                                      end_date.strftime("%Y-%m-%d"))
        try:
            response = requests.get(url)

            if response.ok:
                json = response.json()
                print(json)
                weather = self.parse_response(json, locations)
                return weather
            else:
                print(response.status_code)
                return Response(response.status_code)

        except Exception as ex:
            print(ex)
            raise
