from wsgiref.util import request_uri
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .models import User

# Create your views here.

def index(request):
    return render(request, 'twitter/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'twitter/register.html',
                          {'message': 'Passwords must match.'})
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'twitter/register.html',
                        {'message': 'Username already taken.'})
        login(request, user)
        return redirect('index')
    return render(request, 'twitter/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'twitter/login.html',
                          {'message': 'Invalid username and/or password.'})
    return render(request, 'twitter/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')
