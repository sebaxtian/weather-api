from weather.models import Weather
from rest_framework import serializers

# Create your serializers here.


class WeatherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weather
        # fields = '__all__'
        exclude = ('id',)
