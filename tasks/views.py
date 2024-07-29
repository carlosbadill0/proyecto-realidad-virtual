from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
# imports de prueba para la frecuencia cardiaca.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# views.py
from .models import FrecuenciaCardiaca
from .models import Evaluation
from .models import Evaluacion
import json
# codigo lucho
from .models import Usuario, Rol, Practicante
from .forms import UsuarioForm, PracticanteForm


if not Group.objects.filter(name='Evaluadores').exists():
    Group.objects.create(name='Evaluadores')
if not Group.objects.filter(name='Expositores').exists():
    Group.objects.create(name='Expositores')
    
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', '123')


def home(request):
    
    return render(request, 'home.html')
def signup (request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm 
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:   #registrar usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                evaluadores_group = Group.objects.get(name='Evaluadores')
                user.groups.add(evaluadores_group)
                login(request,user)
                return redirect('tasks')
            except:
                return render(request, 'signup.html',{
                'form': UserCreationForm,
                "error": 'el usuario ya existe'
        })
    return render(request, 'signup.html',{
        'form': UserCreationForm,
        "error": 'las contraseñas no coinciden'
        })
    
def tasks(request):
    return render(request, 'tasks.html')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html' ,{
            'form': AuthenticationForm
    })
    else: 
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None: 
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'credenciales incorrectas'          
            })
        else: 
            login(request,user)
            return redirect('tasks')
        
        

# @csrf_exempt
# def recibir_frecuencia(request):
#     if request.method == 'POST':
#         try:
#             frecuencia = float(request.POST.get('frecuencia', '0'))
            
#             # Guardar frecuencia en la base de datos (ejemplo usando un modelo)
#             nueva_frecuencia = FrecuenciaCardiaca(frecuencia=frecuencia)
#             nueva_frecuencia.save()
            
#             print(f'Frecuencia recibida y almacenada: {frecuencia} BPM')
            
#             return JsonResponse({'status': 'success', 'frecuencia': frecuencia})
#         except ValueError:
#             return JsonResponse({'status': 'error', 'message': 'Frecuencia no válida'})
    
#     return JsonResponse({'status': 'error', 'message': 'Método no soportado'})

# Variable global para mantener la última frecuencia



#de aqui para abajo esta comentado pa ver si funciona lo otro 
ultima_frecuencia = None

@csrf_exempt
def recibir_frecuencia(request):
    global ultima_frecuencia
    if request.method == 'POST':
        try:
            frecuencia = float(request.POST.get('frecuencia', '0'))
            if 30 <= frecuencia <= 220:  # Rango típico de frecuencia cardíaca
                ultima_frecuencia = frecuencia
                print(f'Frecuencia recibida y actualizada: {frecuencia} BPM')
                return JsonResponse({'status': 'success', 'frecuencia': frecuencia})
            else:
                return JsonResponse({'status': 'error', 'message': 'Frecuencia fuera de rango'})
        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'message': 'Frecuencia no válida'})
    return JsonResponse({'status': 'error', 'message': 'Método no soportado'})

def obtener_frecuencia(request):
    global ultima_frecuencia
    if request.method == 'GET':
        if ultima_frecuencia is not None:
            return JsonResponse({'status': 'success', 'frecuencia': ultima_frecuencia})
        else:
            return JsonResponse({'status': 'error', 'message': 'No hay datos disponibles'})
    return JsonResponse({'status': 'error', 'message': 'Método no soportado'})


def mostrar_frecuencia_cardiaca(request):
    # Renderiza el archivo HTML para mostrar la frecuencia cardíaca
    return render(request, 'frecuencia_cardiaca.html')



def evaluation_list(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'disenar_evaluacion.html', {'evaluations': evaluations})

def guardar_evaluacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        evaluacion = Evaluacion(
            tiempo_exposicion=data['tiempo_exposicion'],
            fecha_evaluacion=data['fecha_evaluacion'],
            nombre_evaluador=data['nombre_evaluador'],
            observaciones=data['observaciones']
            # Agrega más campos según tu modelo
        )
        evaluacion.save()
        return JsonResponse({'status': 'success', 'message': 'Datos guardados correctamente.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'})

# @csrf_exempt  # Para permitir peticiones POST sin CSRF token (solo para pruebas)
# def frecuencia_cardiaca(request):
#     if request.method == 'POST':
#         heart_rate = request.POST.get('heartRate')
#         # Aquí puedes procesar el valor de frecuencia cardíaca como lo necesites
#         print(f"Frecuencia cardíaca recibida: {heart_rate}")

#         # Puedes retornar una respuesta JSON si lo deseas
#         return JsonResponse({'message': 'Datos recibidos correctamente'})
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)


# vistas para el admin 
# Verifica que el usuario sea administrador


# codigo del lucho 

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Rol, Practicante
from .forms import UsuarioForm, PracticanteForm
# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    return render(request, "index.html")

def practicantes(request):
    return render(request, "practicantes.html")

def disenar(request):
    return render(request, "disenar.html")

def administrar(request):
    return render(request, "administrar.html")

#usuarios

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    for usuario in usuarios:
        print(usuario.id)  # Imprime para verificar los valores
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'formulario_usuario.html', {'form': form})

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'formulario_usuario.html', {'form': form})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'confirmar_eliminar.html', {'usuario': usuario})

#practicantes

def listar_practicantes(request):
    practicantes = Practicante.objects.all()
    return render(request, 'practicantes.html', {'practicantes': practicantes})

def agregar_practicante(request):
    if request.method == 'POST':
        form = PracticanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_practicantes')
    else:
        form = PracticanteForm()
    return render(request, 'practicantes/agregar_practicante.html', {'form': form})

def editar_practicante(request, id):
    practicante = get_object_or_404(Practicante, id=id)
    if request.method == 'POST':
        form = PracticanteForm(request.POST, instance=practicante)
        if form.is_valid():
            form.save()
            return redirect('listar_practicantes')
    else:
        form = PracticanteForm(instance=practicante)
    return render(request, 'practicantes/editar_practicante.html', {'form': form})

def borrar_practicante(request, id):
    practicante = get_object_or_404(Practicante, id=id)
    if request.method == 'POST':
        practicante.delete()
        return redirect('listar_practicantes')
    return render(request, 'practicantes/borrar_practicante.html', {'practicante': practicante})