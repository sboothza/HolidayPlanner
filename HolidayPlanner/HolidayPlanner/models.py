import datetime

from django.db import models


class Customer(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    long = models.FloatField()
    description = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    customer_id = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Stop(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    schedule_id = models.ForeignKey(Schedule, related_name="schedule", on_delete=models.CASCADE)
    city_id = models.ForeignKey(City, related_name="city", on_delete=models.CASCADE)
    date_arrive = models.DateTimeField()
    date_leave = models.DateTimeField()

    def __str__(self):
        return self.date_arrive


class Location(models.Model):
    class Meta:
        managed = False

    id: models.IntegerField(primary_key=True)
    city_id: models.IntegerField()
    city_name: models.CharField(max_length=50)
    lat: models.FloatField()
    long: models.FloatField()
    start_date: models.DateTimeField()
    end_date: models.DateTimeField()

    def load(self, row):
        print(row)
        self.id = row[0]
        self.city_id = row[1]
        self.city_name = row[2]
        self.lat = row[3]
        self.long = row[4]
        self.start_date = row[5]
        self.end_date = row[6]

    def __str__(self):
        return f"city_id:{self.city_id}, city:{self.city_name}, lat:{self.lat}, long:{self.long}, start:{self.start_date}, stop:{self.end_date}"


class Weather(models.Model):
    class Meta:
        managed = False

    id = models.IntegerField(primary_key=True)
    city_id = models.IntegerField()
    city = models.CharField(max_length=50)
    date = models.DateTimeField()
    code = models.IntegerField()
    description = models.CharField(max_length=200)
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    precip = models.FloatField()
    precip_prob = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.CharField(max_length=20)

    def __init__(self, city_id: int, city: str, date: datetime.datetime, code: int, description: str, temp_min: float, temp_max: float, precip: float, precip_prob: float,
                 wind_speed: float,
                 wind_direction: str,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city_id = city_id
        self.city = city
        self.date = date
        self.code = code
        self.description = description
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.precip = precip
        self.precip_prob = precip_prob
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

    def __str__(self):
        return f"city:{self.city} date:{self.date}"
