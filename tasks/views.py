from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Clase para generar un formulario de registro y login
from django.contrib.auth.models import User #Clase para regis   trar usuarios
from django.contrib.auth import login,logout,authenticate #login: Crear una cookie para el usuario, logout: cierra la sesión del usuario
from django.http import HttpResponse
from . forms import TaskForm #Importar el formulario de create_task
from . models import Task #Importando el modelo de las tareas 
from django.db import IntegrityError #Error de integridad en la base de datos, para manejar la excepción
from django.utils import timezone
from django.contrib.auth.decorators import login_required #Función decoradora para verificar que haya un usuario logeado (Protejer URL's)

# Create your views here.

def home(request):
    return render(request, 'home.html')
def signin(request):
    if request.method == 'GET':
         return render(request,'signin.html',{
            'form': AuthenticationForm
        }) 
    else:
        print(request.POST)
        #autenticar que el usuario y contraseña se enecuentren en la base de datos
        user = authenticate(request, username=request.POST['username'], password=request.POST['password']) 

        if user is None: #Si no se encuentra el usuario y contraseña
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos',
            })
        else:
            login(request,user) #guardar su sesión
            return redirect('tasks')
def signup(request):
    
    if request.method == 'GET': #GET -> muestra el formulario
        
        return render(request,'signup.html',{
            'form': UserCreationForm
        })
        
    else: #POST -> obtiene datos del formulario
        
        if request.POST['password1'] == request.POST['password2']: #válidar que sean las mismas contraseñas en el formulario
            # registrando usuario
            #Try except para evitar que se caiga el servidor si la consulta a la base de datos falla
            try:
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
                print(f"REGISTRO: {user}")
                user.save()
                login(request,user) #se crea una cookie 
                return redirect('signin')
            
            except IntegrityError:
                
                return render(request,'signup.html',{
                        'form': UserCreationForm,
                        'error': 'El usuario ya existe'
                    })
        else:
            return render(request,'signup.html',{
                        'form': UserCreationForm,
                        'error': 'Las contraseñas no coinciden'
                    })
@login_required #Verifica que haya un usuario logeado 
def tasks(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull = True)
    print(tasks)
    return render(request, 'tasks.html',{
        'tasks': tasks,
        'page_title': "Tareas pendientes"
    })
@login_required
def tasks_completed(request):
    
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull = False).order_by('-datecompleted')
    print(tasks)
    return render(request, 'tasks.html',{
        'tasks': tasks,
        'page_title': 'Tareas completadas'
        
    })
@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TaskForm
        })
    else:
        try:
            #Obteniendo los datos del formulario y guardandolos en la BD
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user #asignando el usuario que está logeado
            new_task.save() #Guardando los datos en la base de datos
            return redirect('tasks')
            
        except ValueError: 
            return render(request, 'create_task.html',{
                'form': TaskForm,
                'error': 'Error al guardar los datos'
            })
@login_required           
def task_detail(request, task_id):
    
    if request.method == 'GET':
        task = get_object_or_404(Task,pk = task_id, user = request.user) #Tareas que pertenezcan al id especificado y al usuario logeado
        form = TaskForm(instance=task) #Obtener formulario
        return render(request, 'task_detail.html',{
            'task': task,
            'form': form
            
        })
    else:
        try:
            #Guardar los datos modificados
            task  = get_object_or_404(Task, pk = task_id, user=request.user)
            form = TaskForm(request.POST, instance=task) # generando nuevo formulario
            form.save()
            return redirect('tasks')
            
        except ValueError:
            return render(request, 'task_detail.html',{
                'task': task,
                'form': form,
                'error': "Error al actualizar tarea"
            })
@login_required           
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required  
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
@login_required
def signout(request):
    logout(request)
    return redirect('home')




            
            
        
        
        
   