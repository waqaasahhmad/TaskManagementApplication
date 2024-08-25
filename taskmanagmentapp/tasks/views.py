from django.shortcuts import render
from .models import Task

# Create your views here.

def tasks(request):
    tasks = Task.objects.all()
    return render(request,"tasks/tasks.html",{
        "tasks":tasks
    })

def task(request,id):
    task = Task.objects.get(id=id)
    return render(request,"tasks/task.html",{
        "task" : task
    })