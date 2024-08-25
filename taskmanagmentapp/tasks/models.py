from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = {
        "High" : "high",
        "Medium" : "medium",
        "Low" : "low", 
    }
    STATUS_CHOICES = {
        "Completed" : "completed",
        "In Progress" : "in_progress",
        "Not Started" : "not_started"
    }


    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    priority = models.CharField(max_length=100,choices=PRIORITY_CHOICES,null=True,blank=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,null=True,blank=True)
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


