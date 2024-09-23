from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib.auth.models import User, Group, Permission # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib.auth import login, logout, authenticate # type: ignore
# imports de prueba para la frecuencia cardiaca.
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import json
from datetime import timedelta
# views.py

from .models import EvaluacionScenario, Evaluation
from .models import Evaluacion, CasoDeEstres, Scenario, EvaluacionRealizada
import json
# codigo lucho
from .models import Usuario, Rol, Practicante, DisenarEvaluacion, User, Group
from .forms import UsuarioForm, PracticanteForm, EvaluacionRealizadaForm ,EvaluacionForm, CasoDeEstresForm, ScenarioForm
from .models import ECGData
from django.contrib.auth.decorators import login_required # type: ignore
from django.shortcuts import render, get_object_or_404 # type: ignore

@login_required
def home(request):   
    return render(request, 'home.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'credenciales incorrectas'
            })
        else:
            login(request, user)
            return redirect('home')

def signout(request):
    logout(request)
    return redirect('signin')

def tasks(request):
    return render(request, 'tasks.html')

  
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
    try:
        evaluations = Evaluation.objects.all()
        return render(request, 'disenar_evaluacion.html', {'evaluations': evaluations})
    except Exception as e:
        return render(request, 'disenar_evaluacion.html', {'error': str(e)})

def guardar_evaluacion(request):
    if request.method == 'POST':
        try:
            # Cargar los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            
            # Validar que los campos esperados están en el JSON recibido
            required_fields = ['tiempo_exposicion', 'fecha_evaluacion', 'nombre_evaluador', 'observaciones']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'status': 'error', 'message': f'Falta el campo {field}.'}, status=400)

            # Crear nueva instancia de Evaluacion con los datos recibidos
            evaluacion = Evaluacion(
                tiempo_exposicion=data['tiempo_exposicion'],
                fecha_evaluacion=data['fecha_evaluacion'],
                nombre_evaluador=data['nombre_evaluador'],
                observaciones=data['observaciones']
            )
            evaluacion.save()
            
            return JsonResponse({'status': 'success', 'message': 'Datos guardados correctamente.'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error al parsear JSON.'}, status=400)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error interno del servidor: {str(e)}'}, status=500)
    
    # Si no es POST, retornamos error de método no permitido
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


# codigo del lucho 

from django.http import HttpResponse # type: ignore
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
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
    usuarios = User.objects.all()
    grupos = Group.objects.all()
    contexto = {
        'usuarios': usuarios,
        'grupos': grupos
    }
    return render(request, 'listar_usuarios.html', contexto)

def crear_usuario(request):
    if request.method == 'GET':
        return render(request, 'formulario_usuario.html', {'form': UserForm()})
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            # Validar que las contraseñas coinciden
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 == password2:
                try:
                    # Crear usuario
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'], 
                        password=password1,
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name']
                    )
                    user.save()

                    # Obtener el grupo seleccionado del formulario
                    selected_group_name = form.cleaned_data.get('group')
                    group = Group.objects.get(name=selected_group_name)
                    user.groups.add(group)

                    return redirect('listar_usuarios')
                except Exception as e:
                    return render(request, 'formulario_usuario.html', {
                        'form': form,
                        'error': 'El usuario ya existe o hubo un problema al crearlo.'
                    })
            else:
                return render(request, 'formulario_usuario.html', {
                    'form': form,
                    'error': 'Las contraseñas no coinciden.'
                })
    return render(request, 'formulario_usuario.html', {'form': form})

def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    grupo_id = request.POST.get('grupo')
    grupo = Group.objects.get(id=grupo_id)
    usuario.groups.clear()
    usuario.groups.add(grupo)
    usuario.save()
    return redirect('listar_usuarios') 

def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    return redirect('listar_usuarios')

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
    return render(request, 'practicantes.html', {'form': form})

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

#Diseñar evaluación

from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.http import JsonResponse # type: ignore
from .models import Evaluacion
from .forms import EvaluacionForm

def lista_evaluaciones(request):
    evaluaciones = Evaluacion.objects.all()
    scenarios = Scenario.objects.all()
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.save()
            form.save_m2m()
            return redirect('lista_evaluaciones')
    else:
        form = EvaluacionForm()

    return render(request, 'disenar.html', {
        'evaluaciones': evaluaciones,
        'form': form,
        'scenarios': scenarios,
    })

def detalle_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    return JsonResponse({
        'nombre': evaluacion.nombre,
        'descripcion': evaluacion.descripcion,
        'fecha': evaluacion.fecha,
        'scenarios': list(evaluacion.scenarios.values_list('id', flat=True))
    })

def nueva_evaluacion(request):
    if request.method == "POST":
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.save()
            form.save_m2m()
            # Limpiar la relación ManyToMany antes de agregar los nuevos escenarios
            evaluacion.scenarios.clear()
            # Guardar el orden de los escenarios
            orden = request.POST.get('scenarios_orden', '').split(',')
            for index, scenario_id in enumerate(orden):
                scenario = Scenario.objects.get(id=scenario_id)
                EvaluacionScenario.objects.create(evaluacion=evaluacion, scenario=scenario, orden=index + 1)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def editar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    if request.method == "POST":
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.save()
            form.save_m2m()
            # Limpiar la relación ManyToMany antes de agregar los nuevos escenarios
            evaluacion.scenarios.clear()
            # Guardar el orden de los escenarios
            orden = request.POST.get('scenarios_orden', '').split(',')
            for index, scenario_id in enumerate(orden):
                scenario = Scenario.objects.get(id=scenario_id)
                EvaluacionScenario.objects.create(evaluacion=evaluacion, scenario=scenario, orden=index + 1)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def borrar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    if request.method == "POST":
        evaluacion.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

#roles de los usuarios
from django.contrib.auth.decorators import login_required, user_passes_test # type: ignore
from .forms import UserForm
from django.contrib.auth.models import User # type: ignore

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.groups.add(form.cleaned_data['group'])
            return redirect('manage_users')
    else:
        form = UserForm()
    users = User.objects.all()
    return render(request, 'manage_users.html', {'form': form, 'users': users})

#proteger vistas segun roles 
from django.contrib.auth.decorators import login_required, user_passes_test # type: ignore

def is_evaluator(user):
    return user.groups.filter(name='Evaluador').exists()

@login_required
@user_passes_test(is_evaluator)
def disenar(request):
    # Lógica para diseñar evaluación
    return render(request, 'disenar.html')



# CRUD Expositor
from django.http import JsonResponse # type: ignore # type: ignore
from .models import Expositores
from .forms import ExpositorForm

def lista_expositores(request):
    expositores = Expositores.objects.all()
    evaluations = Evaluacion.objects.all()
    return render(request, 'lista_expositores.html', {'expositores': expositores, 'evaluations': evaluations})

def detalle_expositor(request, pk):
    expositor = get_object_or_404(Expositores, pk=pk)
    return JsonResponse({'nombre': expositor.nombre, 'fecha_ingreso': expositor.fecha_ingreso, 'fecha_nacimiento' : expositor.fecha_nacimiento,
                         'edad': expositor.edad, 'genero':expositor.genero, 'semestre_academico': expositor.semestre_academico,
                         'carrera': expositor.carrera, 'observacion_inicial': expositor.observacion_inicial, 'observacion_final': expositor.observacion_final                         
                         })

def crear_expositor(request):
    if request.method == 'POST':
        form = ExpositorForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def editar_expositor(request, pk):
    expositor = get_object_or_404(Expositores, pk=pk)
    if request.method == 'POST':
        form = ExpositorForm(request.POST, instance=expositor)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def borrar_expositor(request, pk):
    expositor = get_object_or_404(Expositores, pk=pk)
    if request.method == 'POST':
        expositor.delete()
        return JsonResponse({'success': True})

def elegir_evaluacion(request, pk):
    expositor_seleccionado = get_object_or_404(Expositores, pk=pk)
    expositores = Expositores.objects.all()
    evaluations = Evaluacion.objects.all()
    scenarios_by_evaluation = {  ##linea para mostrar los escenarios de cada evaluacion al elegir una evaluacion
        evaluation.id: list(evaluation.scenarios.values('function_name', 'duration', 'tag_name'))
        for evaluation in evaluations
    }
    if request.method == 'POST':
        evaluacion_id = request.POST.get('evaluacion_id')
        nombre_evaluador = request.POST.get('nombre_evaluador')
        fecha_evaluacion = request.POST.get('fecha_evaluacion')
        observacion_inicial = expositor_seleccionado.observacion_inicial

        evaluacion_realizada = EvaluacionRealizada.objects.create(
            expositor=expositor_seleccionado,
            nombre_evaluador=nombre_evaluador,
            fecha_evaluacion=fecha_evaluacion,
            observacion_inicial=observacion_inicial,
            evaluacion_aplicada_id=evaluacion_id
        )
        

        return redirect('evaluar_expositor', id=expositor_seleccionado.id, id_evaluacion=evaluacion_realizada.id)

    return render(request, 'elegirEvaluacion.html', {
        'expositor_seleccionado': expositor_seleccionado,
        'expositores': expositores,
        'scenarios_by_evaluation' : scenarios_by_evaluation,
        'evaluations': evaluations
    })

# conexion sensor ecg

@csrf_exempt
def receive_ecg_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        value = data.get('value')
        if value is not None:
            ECGData.objects.create(value=value)
            return JsonResponse({'status': 'success'}, status=201)
        return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def ecg_chart(request):
    return render(request, 'ecg_chart.html')

from django.http import JsonResponse # type: ignore
from .models import ECGData

def get_ecg_data(request):
    data = list(ECGData.objects.all().values('timestamp', 'value'))
    return JsonResponse(data, safe=False)

def get_latest_ecg(request):
    latest_data = ECGData.objects.latest('timestamp')
    return JsonResponse({
        'timestamp': latest_data.timestamp,
        'value': latest_data.value,
        'status': 'success'
    })

# evaluar a un expositor 
def evaluar_expositor(request, id, id_evaluacion):
    expositor_seleccionado = get_object_or_404(Expositores, id=id)
    evaluacion_realizada = get_object_or_404(EvaluacionRealizada, id=id_evaluacion)
    escenarios = evaluacion_realizada.evaluacion_aplicada.scenarios.all()
    evaluaciones = EvaluacionRealizada.objects.filter(expositor=expositor_seleccionado)
    ultima_evaluacion = evaluaciones.last() if evaluaciones.exists() else None
    
    if request.method == 'POST':
        tiempo_total = request.POST.get('tiempo_total')
        observacion_final = request.POST.get('observacion_final')

        # Convertir tiempo_total a timedelta
        tiempo_total_seconds = int(tiempo_total)
        tiempo_total_timedelta = timedelta(seconds=tiempo_total_seconds)
        tiempo_total_str = str(tiempo_total_timedelta)

        evaluacion_realizada.tiempo_exposicion = tiempo_total_str
        evaluacion_realizada.observacion_final = observacion_final
        evaluacion_realizada.save()

        return render(request, 'mensaje_realizado.html')  # Redirigir a la plantilla intermedia

    return render(request, 'frecuencia_cardiaca.html', {
        'expositores': Expositores.objects.all(),
        'expositor_seleccionado': expositor_seleccionado,
        'evaluacion': evaluacion_realizada,
        'escenarios': escenarios,
        'evaluaciones': evaluaciones,
        'ultima_evaluacion': ultima_evaluacion,
    })
    

def listar_evaluaciones_realizadas(request):
    evaluaciones_realizadas = EvaluacionRealizada.objects.all()
    return render(request, 'listar_evaluaciones_realizadas.html', {
        'evaluaciones_realizadas': evaluaciones_realizadas
    })
 
def detalle_evaluacionRealizada(request, pk):
    evaluacion = get_object_or_404(EvaluacionRealizada, pk=pk)
    data = {
        'expositor': evaluacion.expositor.nombre,
        'nombre_evaluador': evaluacion.nombre_evaluador,
        'fecha_evaluacion': evaluacion.fecha_evaluacion,
        'observacion_inicial': evaluacion.observacion_inicial,
        'observacion_final': evaluacion.observacion_final,
        'tiempo_exposicion': evaluacion.tiempo_exposicion,
        'video_evaluacion': evaluacion.video_evaluacion.url if evaluacion.video_evaluacion else None,
    }
    return JsonResponse(data)

def editar_evaluacionRealizada(request, pk):
    evaluacion = get_object_or_404(EvaluacionRealizada, pk=pk)
    if request.method == 'POST':
        form = EvaluacionRealizadaForm(request.POST, instance=evaluacion)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EvaluacionRealizadaForm(instance=evaluacion)
    return render(request, 'editar_evaluacion.html', {'form': form})   

def borrar_evaluacionRealizada(request, pk):
    evaluacion = get_object_or_404(EvaluacionRealizada, pk=pk)
    if request.method == "POST":
        evaluacion.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})