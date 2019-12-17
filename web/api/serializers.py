from rest_framework import serializers
from dashboard.models import Sensor


class SensorSoilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ('farm_id', 'soil_humidity', 'created_date',)
