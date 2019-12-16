from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dash_farm(request):
    return render(request, 'dashboard/dash_farm.html', {})