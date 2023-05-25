from django.utils import timezone
from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_due = models.DateTimeField('date due', null=True)
    date_completed = models.DateTimeField('date completed', null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def is_overdue(self):
        now = timezone.now()
        return self.date_due < now
    
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, default="def")
    def __str__(self):
        return self.name

