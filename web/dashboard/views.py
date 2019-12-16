from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboard.models import *


@login_required
def dash_farm(request):
    user = request.user
    farms = Farm.objects.filter(user=user.username)
    print(farms)
    return render(request, 'dashboard/dash_farm.html', {'user': user, 'farms': farms})


@login_required
def farm_create(request):
    if request.method == "POST":
        farm = Farm()
        farm.user = request.user
        farm.name = request.POST["name"]
        farm.location = request.POST["location"]
        farm.type = request.POST["type"]
        farm.save()
        return redirect('dash_farm')
    return render(request, 'dashboard/farm_create.html')


@login_required
def farm_detail(request, id):
    sensors = Sensor.objects.filter(farm_id=id).order_by('created_date')
    current_value = sensors[0]
    return render(request, 'dashboard/farm_detail.html', {'sensors': sensors, 'current': current_value})
