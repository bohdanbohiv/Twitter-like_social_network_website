from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('search_user', views.search_user, name='search_user'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('post', views.post, name='post'),
    path('post/delete/<int:pk>', views.delete_post, name='delete_post'),
    path('post/<int:pk>/like', views.like, name='like'),
    path('profile/<int:pk>/followings', views.followings, name='followings'),
    path('profile/<int:pk>/followers', views.followers, name='followers')
]
