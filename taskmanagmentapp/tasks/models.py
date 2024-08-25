from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = {
        "High" : "High",
        "Medium" : "Medium",
        "Low" : "Low", 
    }
    STATUS_CHOICES = {
        "Completed" : "Completed",
        "In Progress" : "In Progress",
        "Not Started" : "Not Started"
    }


    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    assigned_to = models.CharField(max_length=200,blank=True,null=True)
    priority = models.CharField(max_length=100,choices=PRIORITY_CHOICES,null=True,blank=True)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,null=True,blank=True)
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


