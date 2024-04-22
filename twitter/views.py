from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import password_validators_help_text_html, validate_password
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import format_html, format_html_join

from .models import Post, User

# Create your views here.


def index(request: HttpRequest):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author__in=request.user.followings.all())
    else:
        posts = Post.objects
    return render(
        request,
        'twitter/index.html',
        {'posts': posts.order_by('created_at').reverse()}
    )


def register(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        try:
            validate_password(password)
        except ValidationError as error:
            message_items = format_html_join(
                '', '<li>{}</li>', ((message,) for message in error.messages)
            )
            return render(
                request,
                'twitter/register.html',
                {'message': format_html('<ul>{}</ul>', message_items)}
            )
        if password != confirmation:
            return render(
                request,
                'twitter/register.html',
                {'message': 'Passwords must match.'}
            )
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                'twitter/register.html',
                {'message': 'Username already taken.'}
            )
        login(request, user)
        return redirect('index')
    return render(
        request,
        'twitter/register.html',
        {'message': password_validators_help_text_html()}
    )


def login_view(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(
                request,
                'twitter/login.html',
                {'message': 'Invalid username and/or password.'}
            )
    return render(request, 'twitter/login.html')


def logout_view(request: HttpRequest):
    logout(request)
    return redirect('index')


def profile(request: HttpRequest, pk: int):
    user = get_object_or_404(User, id=pk)
    return render(
        request,
        'twitter/profile.html',
        {
            'profile': user,
            'posts': user.posts.order_by('created_at').reverse()
        }
    )


def search_user(request: HttpRequest):
    search = request.GET['search']
    searched = User.objects.filter(username__contains=search)
    return render(
        request,
        'twitter/search_user.html',
        {'search': search, 'searched': searched}
    )


@login_required
def follow(request: HttpRequest, pk: int):
    user = get_object_or_404(User, id=pk)
    if user == request.user:
        raise PermissionDenied
    if user in request.user.followings.all():
        request.user.followings.remove(user)
    else:
        request.user.followings.add(user)
    request.user.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def post(request: HttpRequest):
    post = Post(author=request.user, body=request.POST['body'])
    post.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def delete_post(request: HttpRequest, pk: int):
    post = get_object_or_404(Post, id=pk)
    if request.user == post.author:
        post.delete()
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    raise PermissionDenied


@login_required
def like(request: HttpRequest, pk: int):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def followings(request: HttpRequest, pk: int):
    user = get_object_or_404(User, id=pk)
    return render(
        request,
        'twitter/followings.html',
        {'users': user.followings.all(), 'profile': user}
    )


def followers(request: HttpRequest, pk: int):
    user = get_object_or_404(User, id=pk)
    return render(
        request,
        'twitter/followers.html',
        {'users': user.followers.all(), 'profile': user}
    )
