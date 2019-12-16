from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import Farm


@login_required
def dash_farm(request):
    user = request.user
    farms = Farm.objects.filter(user=user.username)
    print(farms)
    return render(request, 'dashboard/dash_farm.html', {'user': user, 'farms': farms})