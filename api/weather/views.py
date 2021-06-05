from weather.serializers import WeatherSerializer
from weather.models import WeatherCast
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import time
from django.core.cache import cache
import requests
import os

# Create your views here.


class WeatherView(APIView):
    """
        Retrieve a weather instance.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Get Cache
        weather = cache.get('weather')
        if not weather:
            # Request Data
            city = request.GET.get('city', 'Santiago de Cali')
            country = request.GET.get('country', 'CO').lower()

            # Request to Open Weather API
            OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_KEY")
            URL = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={OPEN_WEATHER_KEY}&units=metric"
            r = requests.get(
                URL
            )
            if r.status_code != status.HTTP_200_OK:
                # Error
                return Response({"status": r.status_code, "message": "Open Weather API, Error", "data": r.json()}, status=status.HTTP_200_OK)

            # Weather Response
            weather_response = r.json()

            # Weather Cast
            weather_cast = WeatherCast(weather_response, time.time())
            weather = weather_cast.get_weather()

            # Serializer
            weather_serializer = WeatherSerializer(weather)
            weather = weather_serializer.data

            # TODO: save weather object
            # weather.save()

            # Set Cache
            cache.set('weather', weather)

        # Success
        return Response({"status": status.HTTP_200_OK, "message": "Weather", "data": weather}, status=status.HTTP_200_OK)
