from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField(
        'self',
        through='FollowRelation',
        related_name='followers',
        symmetrical=False,
        blank=True
    )


class FollowRelation(models.Model):
    follower = models.ForeignKey(
        User, models.CASCADE, related_name='follower'
    )
    followee = models.ForeignKey(
        User, models.CASCADE, related_name='followee'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('follower', 'followee'), name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F('followee')),
                name='prevent_reflexivity'
            )
        ]


class Post(models.Model):
    author = models.ForeignKey(User, models.DO_NOTHING, related_name='posts')
    body = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self) -> str:
        return (f'{self.author} ({self.created_at:%Y-%m-%d %H:%M})'
                f': {self.body[:10]}...')
