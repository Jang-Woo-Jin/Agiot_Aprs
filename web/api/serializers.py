from rest_framework import serializers
from dashboard.models import Sensor


class SensorSoilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('soil_humidity', 'created_date',)
