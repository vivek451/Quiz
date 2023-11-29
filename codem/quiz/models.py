from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    question = models.CharField(max_length=200)

    Q1_OPTIONS = [
        (0, 'Never'),
        (1, 'Sometimes'),
        (2, 'Often'),
    ]
    response = models.IntegerField(choices=Q1_OPTIONS)

    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return self.question


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username