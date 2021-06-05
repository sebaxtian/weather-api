from django.db import models
import time
from datetime import datetime, timedelta
import pytz

# Create your models here.


class Weather(models.Model):
    """
        Model to represent the Weather
    """
    location_name = models.CharField(
        max_length=24, unique=False, null=False, blank=False)
    geo_coordinates = models.CharField(
        max_length=24, unique=True, null=False, blank=False)
    temperature = models.CharField(
        max_length=8, unique=False, null=False, blank=False)
    wind = models.CharField(max_length=64, unique=False,
                            null=False, blank=False)
    cloudiness = models.CharField(
        max_length=64, unique=False, null=False, blank=False)
    pressure = models.CharField(
        max_length=12, unique=False, null=False, blank=False)
    humidity = models.CharField(
        max_length=8, unique=False, null=False, blank=False)
    sunrise = models.CharField(
        max_length=8, unique=False, null=False, blank=False)
    sunset = models.CharField(
        max_length=8, unique=False, null=False, blank=False)
    requested_time = models.CharField(
        max_length=24, unique=False, null=False, blank=False)
    # forecast


class WeatherCast():

    # https://www.surfertoday.com/windsurfing/how-to-read-wind-direction
    WIND_DIRECTION = [
        "North",
        "North by East",
        "North-Northeast",
        "Northeast by North",
        "Northeast",
        "Northeast by East",
        "East-Northeast",
        "East by North",
        "East",
        "East by South",
        "East-Southeast",
        "Southeast by East",
        "Southeast",
        "Southeast by South",
        "South-Southeast",
        "South by East",
        "South",
        "South by West",
        "South-Southwest",
        "Southwest by South",
        "Southwest",
        "Southwest by West",
        "West-Southwest",
        "West by South",
        "West",
        "West by North",
        "West-Northwest",
        "Northwest by West",
        "Northwest",
        "Northwest by North",
        "North-Northwest",
        "North by West",
    ]

    weather_response = {}
    requested_time = time.time()

    def __init__(self, weather_response, requested_time):
        self.weather_response = weather_response
        self.requested_time = requested_time

    def cast_location_name(self):
        name = self.weather_response.get('name')
        country_code = self.weather_response.get('sys').get('country')
        return f"{name.title()}, {country_code.upper()}"

    def cast_geo_coordinates(self):
        lat = self.weather_response.get('coord').get('lat')
        lon = self.weather_response.get('coord').get('lon')
        return f"[{lat}, {lon}]"

    def cast_temperature(self):
        temp = self.weather_response.get('main').get('temp')
        return f"{temp} °C"

    def cast_wind(self):
        weather_desc = self.weather_response.get(
            'weather')[0].get('main')
        wind_speed = self.weather_response.get('wind').get('speed')
        wind_deg = self.weather_response.get('wind').get('deg')
        # https://www.surfertoday.com/windsurfing/how-to-read-wind-direction
        wind_dir = self.WIND_DIRECTION[round(
            wind_deg / (360 / len(self.WIND_DIRECTION)))]
        return f"{weather_desc.title()}, {wind_speed} m/s, {wind_dir}"

    def cast_cloudiness(self):
        clouds = self.weather_response.get('clouds').get('all')
        if clouds in range(11, 26):
            clouds = 'Few clouds'
        elif clouds in range(25, 51):
            clouds = 'Scattered clouds'
        elif clouds in range(50, 85):
            clouds = 'Broken clouds'
        elif clouds in range(85, 101):
            clouds = 'Broken clouds'
        else:
            clouds = 'Unreconized'
        return clouds.title()

    def cast_pressure(self):
        pressure = self.weather_response.get('main').get('pressure')
        return f"{pressure} hpa"

    def cast_humidity(self):
        humidity = self.weather_response.get('main').get('humidity')
        return f"{humidity}%"

    def cast_sunrise(self):
        sunrise = self.weather_response.get('sys').get('sunrise')
        sunrise = self._get_datetime_timezone(sunrise)
        return sunrise.strftime('%H:%M')

    def cast_sunset(self):
        sunset = self.weather_response.get('sys').get('sunset')
        sunset = self._get_datetime_timezone(sunset)
        return sunset.strftime('%H:%M')

    def cast_requested_time(self):
        dtvalue = self._get_datetime_timezone(self.requested_time)
        return dtvalue.strftime('%Y-%m-%d %H:%M:%S')

    def _get_datetime_timezone(self, timestamp):
        timezone = self.weather_response.get('timezone')
        utc_offset = timedelta(seconds=timezone)
        dtvalue = datetime.fromtimestamp(timestamp)
        tznames = {tz.zone for tz in map(
            pytz.timezone, pytz.all_timezones_set) if dtvalue.astimezone(tz).utcoffset() == utc_offset}
        return datetime.now(pytz.timezone(list(tznames)[0]))

    def get_weather(self):
        weather = Weather(
            location_name=self.cast_location_name,
            geo_coordinates=self.cast_geo_coordinates,
            temperature=self.cast_temperature,
            wind=self.cast_wind,
            cloudiness=self.cast_cloudiness,
            pressure=self.cast_pressure,
            humidity=self.cast_humidity,
            sunrise=self.cast_sunrise,
            sunset=self.cast_sunset,
            requested_time=self.cast_requested_time
        )
        return weather
