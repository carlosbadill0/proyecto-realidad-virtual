import json
import openpyxl # type: ignore
from collections import Counter
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.decorators import login_required, user_passes_test # type: ignore
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from django.contrib.auth.models import Group, User # type: ignore
from django.http import HttpResponse, JsonResponse # type: ignore
from django.shortcuts import get_object_or_404, redirect, render # type: ignore
from django.utils import timezone # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.views.decorators.http import require_http_methods # type: ignore

from .forms import (EvaluacionForm, EvaluacionRealizadaForm, ExpositorForm,
                    PracticanteForm, UserForm)
from .models import (ECGData, ECGData2, Evaluacion, EvaluacionRealizada,
                     EvaluacionScenario, Evaluation, Expositores, Practicante,
                     Scenario)


@login_required
def home(request):
    cantidad_usuarios = Expositores.objects.count()
    cantidad_evaluaciones_realizadas = EvaluacionRealizada.objects.count()
    
    expositores = Expositores.objects.all()
    edades = [expositor.edad for expositor in expositores]
    edad_counter = Counter(edades)
    expositores_labels = sorted(edad_counter.keys())
    expositores_data = [edad_counter[edad] for edad in expositores_labels]

    # Obtener todas las evaluaciones y sus conteos
    evaluaciones = EvaluacionRealizada.objects.values_list('evaluacion_aplicada__nombre', flat=True)
    evaluacion_counter = Counter(evaluaciones)
    evaluacion_labels = list(evaluacion_counter.keys())
    evaluacion_data = list(evaluacion_counter.values())

    return render(request, 'home.html', {
        'cantidad_usuarios': cantidad_usuarios,
        'cantidad_evaluaciones_realizadas': cantidad_evaluaciones_realizadas,
        'expositores_labels': expositores_labels,
        'expositores_data': expositores_data,
        'evaluacion_labels': evaluacion_labels,
        'evaluacion_data': evaluacion_data
    })


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserForm()
        })
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    # Crear usuario
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                        email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name']
                    )
                    user.save()

                    # Obtener el grupo seleccionado del formulario
                    selected_group = form.cleaned_data['group']
                    user.groups.add(selected_group)

                    login(request, user)
                    return redirect('home')
                except Exception as e:
                     return render(request, 'signup.html', {
                        'form': form,
                        'error': 'El usuario ya existe o hubo un problema al crearlo.'
                    })
            else:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Las contraseñas no coinciden.'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Formulario inválido.'
            })
    
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


ultima_frecuencia = None


@csrf_exempt
def obtener_id_evaluacionRealizada(request):
    if request.method == 'GET':
        id_evaluacionRealizada = EvaluacionRealizada.objects.latest('id').id
        return JsonResponse({'id_evaluacionRealizada': id_evaluacionRealizada})
    return JsonResponse({'status': 'error', 'message': 'Método no soportado'})
  
@csrf_exempt
@require_http_methods(["POST"])
def recibir_frecuencia(request):
    global ultima_frecuencia, guardar_datos  # Asegúrate de declarar las variables como globales
    try:
        data = json.loads(request.body)
        frecuencia = data.get('bpm')
        evaluation_id = data.get('evaluationId')
        print(f"Frecuencia recibida: {frecuencia}, Evaluation ID: {evaluation_id}")  # Agrega esta línea para depuración
        
        # Convertir frecuencia a entero si no lo es
        try:
            frecuencia = int(frecuencia)
            evaluation_id = int(evaluation_id)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': f'Frecuencia y evaluationId deben ser enteros: {str(e)}'})

        if frecuencia is not None:
            if 0 <= frecuencia <= 220:  # Rango típico de frecuencia cardíaca
                if guardar_datos:
                    # Guardar la frecuencia en el modelo
                    ecg_data = ECGData2(bpm=frecuencia, idEvaluacion_id=evaluation_id)
                    ecg_data.save()
                
                ultima_frecuencia = frecuencia  # Actualiza la variable global
                print(f"ultima_frecuencia actualizada: {ultima_frecuencia}")  # Agrega esta línea para depuración
                return JsonResponse({'status': 'success', 'frecuencia': frecuencia})
            else:
                return JsonResponse({'status': 'error', 'message': 'Frecuencia fuera de rango'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No se recibió frecuencia'})
    except json.JSONDecodeError as e:
        return JsonResponse({'status': 'error', 'message': f'Error al decodificar JSON: {str(e)}'})
    except Exception as e:
        # Agregar depuración para capturar el error exacto
        print(f"Error interno del servidor: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f'Error interno del servidor: {str(e)}'})

@require_http_methods(["GET"])
def obtener_frecuencia(request):
    global ultima_frecuencia
    print(f"Valor de ultima_frecuencia antes de GET: {ultima_frecuencia}")  # Agrega esta línea para depuración
    if request.method == 'GET':
        print(f"Valor de ultima_frecuencia en GET: {ultima_frecuencia}")  # Agrega esta línea para depuración
        if ultima_frecuencia is not None:
            return JsonResponse({'status': 'success', 'frecuencia': ultima_frecuencia})
        else:
            return JsonResponse({'status': 'error', 'message': 'No hay datos disponibles'})
    return JsonResponse({'status': 'error', 'message': 'Método no soportado'})

def mostrar_frecuencia_cardiaca(request):
    # Renderiza el archivo HTML para mostrar la frecuencia cardíaca
    return render(request, 'frecuencia_cardiaca.html')


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

                    login(request, user)  # Iniciar sesión con el nuevo usuario
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


#evaluaciones
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
    try:
        evaluacion = get_object_or_404(Evaluacion, pk=pk)
        selected_scenarios = evaluacion.scenarios.all()
        available_scenarios = Scenario.objects.exclude(id__in=selected_scenarios.values('id'))

        data = {
            'nombre': evaluacion.nombre,
            'descripcion': evaluacion.descripcion,
            'fecha': evaluacion.fecha,
            'scenarios': list(evaluacion.scenarios.values_list('function_name', flat=True)),
            'selected_scenarios': [{'id': scenario.id, 'nombre': scenario.function_name} for scenario in selected_scenarios],
            'available_scenarios': [{'id': scenario.id, 'nombre': scenario.function_name} for scenario in available_scenarios],
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})

def nueva_evaluacion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        scenarios_orden = request.POST.get('scenarios_orden').split(',')

        if not (nombre and descripcion and fecha and scenarios_orden):
            return JsonResponse({'success': False, 'error': 'Faltan datos'})

        try:
            evaluacion = Evaluacion.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                fecha=fecha
            )
            for orden, scenario_id in enumerate(scenarios_orden, start=1):
                scenario = Scenario.objects.get(id=scenario_id)
                EvaluacionScenario.objects.create(
                    evaluacion=evaluacion,
                    scenario=scenario,
                    orden=orden
                )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def editar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        scenarios_ids = request.POST.getlist('scenarios_ids[]')

        if not (nombre and descripcion and fecha and scenarios_ids):
            return JsonResponse({'success': False, 'error': 'Faltan datos'})

        try:
            evaluacion.nombre = nombre
            evaluacion.descripcion = descripcion
            evaluacion.fecha = fecha
            evaluacion.save()

            # Limpiar escenarios anteriores
            evaluacion.scenarios.clear()

            # Agregar nuevos escenarios
            for orden, scenario_id in enumerate(scenarios_ids, start=1):
                if scenario_id:  # Verificar que scenario_id no sea vacío o None
                    try:
                        scenario = Scenario.objects.get(id=scenario_id)
                        EvaluacionScenario.objects.create(
                            evaluacion=evaluacion,
                            scenario=scenario,
                            orden=orden
                        )
                    except Scenario.DoesNotExist:
                        return JsonResponse({'success': False, 'error': f'Scenario con ID {scenario_id} no existe'})

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        scenarios = Scenario.objects.all()
        selected_scenarios = evaluacion.scenarios.all()
        available_scenarios = scenarios.exclude(id__in=selected_scenarios.values('id'))
        
        data = {
            'nombre': evaluacion.nombre,
            'descripcion': evaluacion.descripcion,
            'fecha': evaluacion.fecha,
            'selected_scenarios': [{'id': es.id, 'nombre': es.function_name} for es in selected_scenarios],
            'available_scenarios': [{'id': s.id, 'nombre': s.function_name} for s in available_scenarios],
        }
        return JsonResponse(data)
     
def borrar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    if request.method == "POST":
        evaluacion.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})



def is_admin(user):
    return user.groups.filter(name='Administrador').exists()



def is_evaluator(user):
    return user.groups.filter(name='Evaluador').exists()



#expositores
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
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

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

#elegir evaluacion a realizar
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

    if request.GET.get('format') == 'json':
        
        def convert_to_seconds(time_str):
            h, m = map(int, time_str.split(':'))
            return h * 3600 + m * 60

        total_duration_seconds = sum(convert_to_seconds(escenario.duration) for escenario in escenarios)

        # Convertir total_duration_seconds a formato HH:MM
        total_duration_minutes = total_duration_seconds // 60
        total_duration_hours = total_duration_minutes // 60
        total_duration_minutes = total_duration_minutes % 60
        total_duration_str = f"{total_duration_hours:02}:{total_duration_minutes:02}"

        # Crear el JSON con los datos de la evaluación
        data = {
            "simulationID": f"sim-{evaluacion_realizada.id}",
            "date": evaluacion_realizada.fecha_evaluacion.strftime('%Y-%m-%d'),
            "duration": total_duration_str,
            "details": {
                "scene": evaluacion_realizada.evaluacion_aplicada.nombre,
                "description": evaluacion_realizada.evaluacion_aplicada.descripcion
            },
            "scenarios": [
                {
                    "id": f"scene-{escenario.id}",
                    "functionName": escenario.function_name,
                    "tagName": escenario.tag_name,
                    "duration": escenario.duration
                }
                for escenario in escenarios
            ]
        }
        return JsonResponse(data)

    return render(request, 'frecuencia_cardiaca.html', {
        'expositores': Expositores.objects.all(),
        'expositor_seleccionado': expositor_seleccionado,
        'evaluacion': evaluacion_realizada,
        'escenarios': escenarios,
        'evaluaciones': evaluaciones,
        'ultima_evaluacion': ultima_evaluacion,
    })
    
#evaluaciones realizadas
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

#etapas de evaluacion
#guardar datos de la conexion csg_data
guardar_datos = False

@csrf_exempt
def iniciar_guardado(request):
    global guardar_datos
    if request.method == 'POST':
        guardar_datos = True
        print("Guardado iniciado")  # Depuración
        return JsonResponse({"status": "success", "message": "Guardado iniciado"})
    return JsonResponse({"status": "error", "message": "Método no soportado"})

@csrf_exempt
def recibir_datos(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                bpm = data.get('bpm')
                evaluation_id = data.get('evaluationId')
                
                # Convertir bpm y evaluation_id a enteros si no lo son
                try:
                    bpm = int(bpm)
                    evaluation_id = int(evaluation_id)
                except ValueError as e:
                    return JsonResponse({'status': 'error', 'message': f'bpm y evaluationId deben ser enteros: {str(e)}'})
 
                # Agregar depuración para verificar los valores antes de guardar
                print(f"Datos recibidos - BPM: {bpm}, Evaluation ID: {evaluation_id}")

                ecg_data = ECGData2(bpm=bpm, idEvaluacion_id=evaluation_id)
                ecg_data.save()
                return JsonResponse({'status': 'success'})
            except json.JSONDecodeError as e:
                return JsonResponse({'status': 'error', 'message': f'JSON inválido: {str(e)}'})
            except Exception as e:
                import traceback
                print(f"Error interno del servidor: {str(e)}")
                print(traceback.format_exc())  # Esto te da un traceback más detallado
                return JsonResponse({'status': 'error', 'message': f'Error interno del servidor: {str(e)}'})
        return JsonResponse({'status': 'error', 'message': 'Método de solicitud inválido'})

@csrf_exempt
def verificar_guardado(request):
    if request.method == 'GET':
        try:
            registros = ECGData2.objects.all().values()
            return JsonResponse({'status': 'success', 'data': list(registros)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def detener_guardado(request):
    global guardar_datos
    if request.method == 'POST':
        guardar_datos = False
        print("Guardado detenido")  # Depuración
        return JsonResponse({"status": "success", "message": "Guardado detenido"})
    return JsonResponse({"status": "error", "message": "Método no soportado"})

@csrf_exempt
def estado_guardado(request):
    global guardar_datos
    if request.method == 'GET':
        return JsonResponse({"guardar_datos": guardar_datos})
    return JsonResponse({"status": "error", "message": "Método no soportado"})


def obtener_datos(request):
    # Obtener los últimos 10 datos de BPM
    data = ECGData2.objects.filter(timestamp__gte=timezone.now()-timedelta(minutes=10)).order_by('timestamp')
    
    bpm_values = [entry.bpm for entry in data]
    timestamps = [entry.timestamp.strftime("%Y-%m-%d %H:%M:%S") for entry in data]
    
    return JsonResponse({'bpm_values': bpm_values, 'timestamps': timestamps})

def mostrar_grafico(request):
    return render(request, 'grafico.html')

def get_latest_ecg2(request):
    try:
        latest_data = ECGData2.objects.latest('timestamp')
        return JsonResponse({
            'timestamp': latest_data.timestamp,
            'value': latest_data.bpm,
            'status': 'success'
        })
    except ECGData2.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'No data available'
        })

def listar_datos(request):
    datos = ECGData2.objects.all()
    return render(request, 'listardatosecgdata2.html', {'datos': datos})

def exportar_evaluacion_excel(request, pk):
    evaluacion = get_object_or_404(EvaluacionRealizada, pk=pk)
    pulsos = ECGData2.objects.filter(idEvaluacion_id=pk)

    # Depuración: Imprimir datos obtenidos
    print(f"Evaluación: {evaluacion}")
    print(f"ECG Data Count: {pulsos.count()}")
    for pulso in pulsos:
        print(f"Pulso: {pulso}")

    # Crear un libro de trabajo y una hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Evaluación"

    # Escribir encabezados
    headers = [
        "Nombre del Evaluador", "Nombre de la Evaluación", "Nombre del Expositor",
        "Casos de Estrés", "Fecha de Evaluación", "Hora de Evaluación", "Pulsaciones", "Timestamp"
    ]
    ws.append(headers)

    # Escribir datos de la evaluación
    for pulso in pulsos:
        row = [
            evaluacion.nombre_evaluador,
            evaluacion.evaluacion_aplicada.nombre,
            evaluacion.expositor.nombre,
            ", ".join([scenario.function_name for scenario in evaluacion.evaluacion_aplicada.scenarios.all()]),
            evaluacion.fecha_evaluacion,
            evaluacion.fecha_evaluacion.strftime("%H:%M:%S"),
            pulso.bpm,
            pulso.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ]
        ws.append(row)

    # Preparar la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=evaluacion_{pk}.xlsx'
    wb.save(response)
    return response