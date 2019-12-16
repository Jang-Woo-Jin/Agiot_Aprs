from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def register(request):
    if request.method == "POST":
        if request.POST["user_pw"] == request.POST["user_pw_confirm"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password"], email=request.POST["contact"],
            )
            auth.login(request, user)
            return redirect('test')
        return render(request, '/account/register.html')
    return render(request, 'account/register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('test')
        return render(request, '/account/login.html', {'error': 'username or password is incorrect'})
    return render(request, 'account/login.html', {})

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('login')
    return render(request, 'account/login.html', {})