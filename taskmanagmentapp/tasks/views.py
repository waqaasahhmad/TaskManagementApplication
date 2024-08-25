from django.shortcuts import render , redirect
from .models import Task
from .forms import TaskForm

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

def addTask(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks")

    form = TaskForm()
    return render(request,"tasks/add-tasks.html",{
        "form" : form
    })


def editTask(request,id):
    task = Task.objects.get(id=id)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks")
    return render(request,"tasks/add-tasks.html",{
        "form":form
    })


def deleteTask(request,id):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
    return render(request,"tasks/delete-task.html",{
        "task" : task
    })