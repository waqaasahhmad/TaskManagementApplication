from django.shortcuts import render , redirect
from .models import Task
from .forms import TaskForm
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login , authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login")
def tasks(request):
    search_query = ""
    if request.GET.get("search"):
        search_query = request.GET.get("search")
    

    tasks = Task.objects.filter(Q(title__icontains=search_query) | Q(priority__icontains=search_query) | Q(status__icontains=search_query))
    return render(request,"tasks/tasks.html",{
        "tasks":tasks,
        "search_query" : search_query
    })

@login_required(login_url="login")
def task(request,id):
    profile = request.user.profile
    task = profile.task_set.get(id=id)
    # task = Task.objects.get(id=id)
    return render(request,"tasks/task.html",{
        "task" : task
    })

@login_required(login_url="login")
def addTask(request):
    profile = request.user.profile
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = profile
            form.save()
            return redirect("tasks")

    form = TaskForm()
    return render(request,"tasks/add-tasks.html",{
        "form" : form
    })

@login_required(login_url="login")
def editTask(request,id):
    profile = request.user.profile
    task = profile.task_set.get(id=id)
    # task = Task.objects.get(id=id)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks")
    return render(request,"tasks/add-tasks.html",{
        "form":form
    })

@login_required(login_url="login")
def deleteTask(request,id):
    profile = request.user.profile
    task = profile.task_set.get(id=id)
    # task = Task.objects.get(id=id)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")
    return render(request,"tasks/delete-task.html",{
        "task" : task
    })

@login_required(login_url="login")
def dashboard(request):
    profile = request.user.profile
    total_tasks = profile.task_set.all().count()
    pending_tasks = profile.task_set.filter(status="Not Started").count()
    today = timezone.now().date()
    threshold = today + timedelta(7)
    upcoming_deadlines = profile.task_set.filter(due_date__lte=threshold, due_date__gte=today)
    upcoming_deadlines = upcoming_deadlines.exclude(status="Completed")
    tasks_due_soon = upcoming_deadlines.count()
    return render(request,"tasks/dashboard.html",{
        "total_tasks" : total_tasks,
        "pending_tasks" : pending_tasks,
        "tasks_due_soon" : tasks_due_soon,
        "upcoming_deadlines" : upcoming_deadlines
        
    })


def userlogin(request):
    if request.user.is_authenticated:
        return redirect("tasks")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except:
            print("Username Doess't Exist")

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("tasks")
        else:
            print("Username or Password does not exist")

    return render(request,"tasks/login.html")


def userlogout(request):
    logout(request)
    return redirect("login")

