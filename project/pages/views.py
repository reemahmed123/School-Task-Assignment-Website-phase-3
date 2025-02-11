from django.shortcuts import render, redirect
from .models import signup,Task
from .forms import TaskForm
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.dispatch import receiver
# from pages.models import AdminUser, TeacherUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
# Create your views here.
def Signup(request):  ##mariam
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    status = request.POST.get('status')
    data = signup(username= username, password= password, email= email, status= status)
    userExist = signup.objects.filter(username=username).count() > 0
    if request.method == 'POST' and not userExist:
        data.save()
        return redirect('login')
    elif userExist:
        print(username)
        context = {
            'message': "This username is  already used!",
            'userExist' : userExist,
        }
        messages.error(request, "This username is  already used!")
        return render(request,'pages/signup_page.html', context)
    return render(request,'pages/signup_page.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = signup.objects.get(username=username, password=password)
           
            if user is not None:
                request.session['new_user'] = user.username
                request.session['status1'] = user.status
                return redirect('tasklist')  # Redirect to tasklist
        except signup.DoesNotExist:
            return render(request, 'pages/login_page.html', {'error_message': 'Invalid username or password.'})
            

    # If request method is not POST, just render the login page
    return render(request, 'pages/login_page.html')

def tasklist(request):
   if(request.session.get('status1','Guest')=='admin') :
        myTasks=Task.objects.filter(creator=request.session.get('new_user', 'Guest'))
        context = {
        'myTasks': myTasks,
        'username': request.session.get('new_user', 'Guest'), 
        'status': request.session.get('status1','Guest')
        }
        return render(request,'pages/TaskList.html',context)
   else:
        myTasks=Task.objects.filter(teacher_name=request.session.get('new_user', 'Guest'))
        context = {
        'myTasks': myTasks,
        'username': request.session.get('new_user', 'Guest'),
        'status': request.session.get('status1','Guest'),
        'Completed_Tasks' : "Completed Tasks",
        }
        return render(request,'pages/TaskList.html',context)

def add_task(request):
    if Task.objects.count() == 0:
        request.session["currID"] = 1
    currID = request.session.get("currID", 1)
    teacherName = request.POST.get('teacherName')
    title = request.POST.get('taskTitle')
    priority = request.POST.get('priority')
    description = request.POST.get('description')
    creator = request.session.get('new_user', 'Guest')

    if request.method == 'POST':
        data = Task(task_id=currID, teacher_name= teacherName, task_title= title,
            priority= priority, description = description,creator = creator)
    
        currID = currID +1
        request.session["currID"] = currID
        data.save()
        return redirect('tasklist')
    return render(request, 'pages/add_task.html', {'currID' : currID})

def delete_task(request, task_id):
    if request.session.get('status1', 'Guest') == 'admin':
        currID = request.session.get("currID")
        request.session["currID"] = currID-1
        task = Task.objects.get(task_id=task_id)
        Task.objects.filter(task_id__gt=task_id).update(task_id = F("task_id")-1)
        if request.method == 'POST':
            task.delete()
        return redirect('tasklist')
    else:
        return redirect('tasklist')

def complete_task(request, task_id):
    task = Task.objects.get(task_id=task_id)
    if request.method == 'POST':
        if task.completion == False:
            task.completion = True
            task.save()
        else:
            task.completion = False
            task.save()
    return redirect('tasklist')

def search(request):
    if request.method == 'POST':
        priority = request.POST.get('priority' , 'All')
        user_status = request.session.get('status1', 'Guest')
        username = request.session.get('new_user', 'Guest')
    
        if user_status == 'admin':
            myTasks = Task.objects.filter(creator=username)
        else:
            myTasks = Task.objects.filter(teacher_name=username)

        if priority != 'All':
            myTasks = myTasks.filter(priority = priority)
            
        context = {
            'myTasks': myTasks,
            'username': username, 
            'status': user_status,
            'priority': priority,
        }
        return render(request, 'pages/TaskList.html', context)
    else:
        return redirect('tasklist')

def completedTasks(request):
    user_status = request.session.get('status1', 'Guest')
    username = request.session.get('new_user', 'Guest')

    if user_status == 'admin':
        myTasks = Task.objects.filter(creator=username)
    else:
        myTasks = Task.objects.filter(teacher_name=username)
    myTasks = myTasks.filter(completion=True)

    context = {
        'myTasks': myTasks,
        'username': username, 
        'status': user_status,
        'Completed_Tasks' : "<- Task List",
    }
    return render(request, 'pages/TaskList.html', context)

def editTask(request, task_id):
    task = Task.objects.get(task_id=task_id)
    teacher_name = task.teacher_name
    task_title = task.task_title
    priority = task.priority
    description = task.description
    context = {
        'teacher_name' : teacher_name,
        'task_title' : task_title,
        'priority' : priority,
        'description' : description,
    }
    
    if request.method == 'POST':
        newTeacher_name = request.POST.get('teacherName')
        if newTeacher_name and newTeacher_name != teacher_name:
            task.teacher_name = newTeacher_name
        newTitle = request.POST.get('taskTitle')
        if newTitle and newTitle != task_title:
            task.task_title = newTitle
        newPriority = request.POST.get('priority')
        if newPriority != priority:
            task.priority = newPriority
        newDescription = request.POST.get('description')
        if newDescription != description:
            task.description = newDescription
        task.save()
        return redirect('tasklist')
    else:
        return render(request, 'pages/Edit_Task.html', context)