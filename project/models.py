import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    question_title = models.CharField(max_length=50)
    question_author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_title

    @property
    def total_votes(self):
        return self.choice_set.aggregate(models.Sum("votes"))["votes__sum"]

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class TimeVoting(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time_voting = models.DateTimeField()

    def __str__(self):
        return f"{self.users}_{self.question}_{self.time_voting}"
