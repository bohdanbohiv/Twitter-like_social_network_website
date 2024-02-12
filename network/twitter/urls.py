from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('search_user', views.search_user, name='search_user'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('post', views.post, name='post')
]
