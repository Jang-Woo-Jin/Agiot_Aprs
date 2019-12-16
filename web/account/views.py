from django.shortcuts import render

def register(request):
    return render(request, 'account/register.html', {})

def login(request):
    return render(request, 'account/login.html', {})

def logout(request):
    return render(request, 'account/login.html', {})