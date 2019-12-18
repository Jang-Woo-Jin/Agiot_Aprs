from rest_framework import viewsets
from .serializers import *
from dashboard.models import Sensor
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
import datetime
from datetime import date
import subprocess

class SensorsViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return

    def get_soil(self, request):
        if request.method == "GET":
            print(request.GET['farm_id'])
        today = date.today()
        sensors = Sensor.objects.filter(farm_id=1).order_by('created_date')
        serializers = SensorSoilSerializer(sensors, many=True)
        datas = serializers.data
        today_data = []
        for data in datas:
            if data['created_date'].split("T")[0] == str(today):
                today_data.append(data)

        index = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
                 "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

        today_hours_max_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for data in today_data:
            day = (str)(data['created_date'].split("T")[1]).split(":")[0]
            today_hours_max_data[int(day)] = data['soil_humidity']

        chart_data = {
            'index': index,
            'data': today_hours_max_data
        }
        return Response(chart_data)
    
    def send_actuator(self, request):
        print(request.GET["value"])
        subprocess.call('mosquitto_pub -d -t web -m "!' + request.GET["value"] + '"', shell=True)
    
