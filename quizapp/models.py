from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_id = models.IntegerField()

    def __str__(self):
        return self.name


class Quiz_data(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)


class Quiz(models.Model):
    quiz_id = models.ForeignKey(Quiz_data, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    selected_answer = models.CharField(max_length=200)
    status = models.IntegerField()
