from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

class User(models.Model):
    id = models.AutoField(primary_key=True)

def validate_sat(value):
    if value < 0 or value > 5:
        raise ValidationError(
            gettext_lazy('%(value)s is outside of range.'),
            params={'value': value},
        )

class Tentative_Task(models.Model):
    WORK = "W"
    LEISURE = "L"
    EXERCISE = "E"
    task_types = [(WORK, "Work"),
                  (LEISURE, "Leisure"),
                  (EXERCISE, "Exercise"),]
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=task_types)

class Task(models.Model):
    WORK = "W"
    LEISURE = "L"
    EXERCISE = "E"
    task_types = [(WORK, "Work"),
                  (LEISURE, "Leisure"),
                  (EXERCISE, "Exercise"),]
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=task_types)
    satisfaction = models.IntegerField(validators=[validate_sat], null=True)

class Suggestion(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Tentative_Task, on_delete=models.CASCADE)
    new_start = models.DateTimeField()
    new_end = models.DateTimeField()
    rule = models.PositiveIntegerField()