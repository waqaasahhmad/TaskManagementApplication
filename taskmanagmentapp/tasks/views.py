from django.shortcuts import render , redirect
from .models import Task
from .forms import TaskForm
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

# Create your views here.

def tasks(request):
    search_query = ""
    if request.GET.get("search"):
        search_query = request.GET.get("search")
    

    tasks = Task.objects.filter(Q(title__icontains=search_query) | Q(priority__icontains=search_query) | Q(status__icontains=search_query))
    return render(request,"tasks/tasks.html",{
        "tasks":tasks,
        "search_query" : search_query
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


def dashboard(request):
    total_tasks = Task.objects.all().count()
    pending_tasks = Task.objects.filter(status="Not Started").count()
    today = timezone.now().date()
    threshold = today + timedelta(7)
    upcoming_deadlines = Task.objects.filter(due_date__lte=threshold, due_date__gte=today)
    tasks_due_soon = upcoming_deadlines.count()
    return render(request,"tasks/dashboard.html",{
        "total_tasks" : total_tasks,
        "pending_tasks" : pending_tasks,
        "tasks_due_soon" : tasks_due_soon,
        "upcoming_deadlines" : upcoming_deadlines
        
    })

today = timezone.now().date()
print(today)

threshold = today + timedelta(7)
print(threshold)