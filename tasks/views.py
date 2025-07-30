from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate 
from .forms import TaskForm 
from .models import task
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import MyUserCreationForm



def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': MyUserCreationForm() })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect ('tasks')
            except:
                return render(request, 'signup.html', {
                    'form': MyUserCreationForm(),
                    "error": 'el usuario ya existe'
                })
        return render(request, 'signup.html', {
                'form': MyUserCreationForm(),
                 "error": 'clave no coincide'})
@login_required
def tasks(request):
    tareas = task.objects.filter(usuario=request.user, fechacompletada__isnull=True)
    return render(request, 'tasks.html', {'tareas': tareas, 'completadas': False})
@login_required
def tasks_completed(request):
    tareas = task.objects.filter(usuario=request.user, fechacompletada__isnull=False).order_by('-fechacompletada')
    return render(request, 'tasks.html', {'tareas': tareas, 'completadas': True})

@login_required
def create_task(request):

    if request.method == 'GET':
        return render (request, 'create_task.html', {
            'form': TaskForm()
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.usuario = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
             return render (request, 'create_task.html', {
                'form': TaskForm(),
                'error':'proporsionar datos valido'
            })
@login_required
def task_detail(request, task_id):

    if request.method == 'GET':
      tarea = get_object_or_404(task, pk=task_id, usuario=request.user)
      form = TaskForm(instance=tarea)
      return render(request, 'task_detail.html', {'task': tarea, 'form': form})
    else:
        try:
            tarea = get_object_or_404(task, pk=task_id, usuario=request.user)
            form = TaskForm(request.POST, instance=tarea)
            form.save()
            return redirect('tasks')
        except ValueError:
           return render(request, 'task_detail.html', {'task': tarea, 'form': form, 'error': ' errorDatos invalidos'})
@login_required
def complete_task(request, task_id):
    tarea = get_object_or_404(task, pk=task_id, usuario=request.user)
    if request.method == 'POST':
     tarea.fechacompletada = timezone.now()
     tarea.save()
    return redirect('tasks')
@login_required
def delete_task(request, task_id):
    tarea = get_object_or_404(task, pk=task_id, usuario=request.user)
    if request.method == 'POST':
     tarea.delete()
    return redirect('tasks')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form' : AuthenticationForm()
        })
    else:
       user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
       if user is None: 
           
           return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'usuario o password incorrecto'
            })
       else:
           login(request, user) 
           return redirect('tasks')
       
       
        
