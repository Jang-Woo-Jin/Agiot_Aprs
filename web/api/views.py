from rest_framework import viewsets
from .serializers import *
from dashboard.models import Sensor
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable


class SensorsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return

    def get_soil(self, request):
        if request.method == "POST":
            print(request.POST['farm_id'])
        #if request.method == "POST":
        sensors = Sensor.objects.filter(farm_id=1).order_by('created_date')
        serializers = SensorSoilSerializer(sensors, many=True)
        return Response(serializers.data)
        #return Response(NotAcceptable)