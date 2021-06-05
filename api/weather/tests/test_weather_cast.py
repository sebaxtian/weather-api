from weather.models import WeatherCast
import requests
from rest_framework import status
import time
import os
from dotenv import load_dotenv
from pathlib import Path
from shutil import copyfile

# Check dotenv
if not os.path.exists(Path('../') / '.env'):
    copyfile(Path('../') / 'example.env', Path('../') / '.env')
# Load dotenv
load_dotenv(dotenv_path=Path('../') / '.env')


# TODO: Create factory
def get_weather_response():
    OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
    URL = f"http://api.openweathermap.org/data/2.5/weather?q=New York,us&appid={OPEN_WEATHER_KEY}&units=metric"
    r = requests.get(
        URL
    )
    # print(r.status_code)
    if r.status_code != status.HTTP_200_OK:
        raise NameError('Open Weather API, Error')
    return r.json()


# TODO: Create factory
weather_cast = WeatherCast(get_weather_response(), time.time())


def test_cast_location_name():
    location_name = weather_cast.cast_location_name()
    assert location_name
    assert len(location_name.split(',')) == 2
    assert len(location_name.split(',')[1].strip()) == 2


def test_cast_geo_coordinates():
    geo_coordinates = weather_cast.cast_geo_coordinates()
    assert geo_coordinates
    assert '[' in geo_coordinates
    assert ']' in geo_coordinates
    geo_coordinates = geo_coordinates[1:-1]
    assert len(geo_coordinates.split(',')) == 2
    assert float(geo_coordinates.split(',')[0].strip())
    assert float(geo_coordinates.split(',')[1].strip())


def test_cast_temperature():
    temperature = weather_cast.cast_temperature()
    assert temperature
    assert temperature[-2:] == '°C'


def test_cast_wind():
    wind = weather_cast.cast_wind()
    assert wind
    assert len(wind.split(',')) == 3
    assert float(wind.split(',')[1].strip().split()[0])
    assert wind.split(',')[1].strip().split()[1] == 'm/s'


def test_cast_cloudiness():
    cloudiness = weather_cast.cast_cloudiness()
    assert cloudiness
    # TODO: Use static variable on WeatherCast
    assert cloudiness in ['Few Clouds',
                          'Scattered Clouds', 'Broken Clouds', 'Broken Clouds', 'Unreconized']


def test_cast_pressure():
    pressure = weather_cast.cast_pressure()
    assert pressure
    assert len(pressure.split()) == 2
    assert int(pressure.split()[0])
    assert pressure.split()[1].strip() == 'hpa'


def test_cast_humidity():
    humidity = weather_cast.cast_humidity()
    assert humidity
    assert humidity[-1:] == '%'
    assert int(humidity[0])


def test_cast_sunrise():
    sunrise = weather_cast.cast_sunrise()
    assert sunrise
    assert len(sunrise.split(':')) == 2
    assert len(sunrise.split(':')[0]) == 2
    assert len(sunrise.split(':')[1]) == 2


def test_cast_sunset():
    sunset = weather_cast.cast_sunset()
    assert sunset
    assert len(sunset.split(':')) == 2
    assert len(sunset.split(':')[0]) == 2
    assert len(sunset.split(':')[1]) == 2


def test_cast_requested_time():
    requested_time = weather_cast.cast_requested_time()
    assert requested_time
    assert len(requested_time.split()) == 2
    assert len(requested_time.split()[0].split('-')) == 3
    assert len(requested_time.split()[1].split(':')) == 3
