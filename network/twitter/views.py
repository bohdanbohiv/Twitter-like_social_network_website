from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .models import User

# Create your views here.

def index(request: HttpRequest):
    return render(request, 'twitter/index.html')

def register(request: HttpRequest):
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

def login_view(request: HttpRequest):
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

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('index')

def profile(request: HttpRequest, pk: int):
    user = get_object_or_404(User, id=pk)
    return render(request, 'twitter/profile.html', {'profile': user})

def search_user(request: HttpRequest):
    search = request.GET['search']
    searched = User.objects.filter(username__contains=search)
    return render(request, 'twitter/search_user.html', {'search': search, 'searched': searched})

def follow(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=pk)
        request.user.followings.add(user)
        request.user.save()
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    return redirect('login')

def unfollow(request: HttpRequest, pk: int):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=pk)
        request.user.followings.remove(user)
        request.user.save()
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    return redirect('login')
