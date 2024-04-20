from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True
    )


class Post(models.Model):
    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.DO_NOTHING
    )
    body = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def num_of_likes(self):
        return self.likes.count()

    def __str__(self) -> str:
        return (f'{self.author} ({self.created_at:%Y-%m-%d %H:%M})'
                f': {self.body[:10]}...')
