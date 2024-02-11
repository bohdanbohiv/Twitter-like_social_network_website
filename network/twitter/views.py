from django.contrib.auth import login
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
