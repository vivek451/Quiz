from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Option(models.Model):
    description = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.description} - {self.value}"


class Question(models.Model):
    description = models.CharField(max_length=100)
    options = models.ManyToManyField(Option)

    def __str__(self):
        return self.description


class Quiz(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Option, on_delete=models.CASCADE, limit_choices_to={'question': models.F('question')})

    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return self.question.description


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
