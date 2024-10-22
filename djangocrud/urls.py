"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from tasks import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    # path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.signout, name='logout'),
    path('', views.signin, name='signin'),
    path('api/frecuencia/', views.recibir_frecuencia, name='recibir_frecuencia'),
#     path('api/ultima_frecuencia/', views.obtener_frecuencia, name='obtener_frecuencia'),
##  path('frecuencia-cardiaca/', views.mostrar_frecuencia_cardiaca, name='frecuencia_cardiaca'),
     path('a/', views.evaluation_list, name='disenar_evaluacion'),
     path('api/guardar_evaluacion/', views.guardar_evaluacion, name='guardar_evaluacion'),
#    path('frecuencia-cardiaca/', views.frecuencia_cardiaca, name='frecuencia_cardiaca'),
#codigo lucho 
    #path('', views.index, name='index'),
#    path('practicantes/', views.listar_practicantes, name='listar_practicantes'),
    # path('practicantes-agregar/', views.agregar_practicante, name='agregar_practicante'),
    path('administrar/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='borrar_usuario'),
    # urls para practicante
    # path('practicantes/', views.listar_practicantes, name='listar_practicantes'),
    # path('practicantes-agregar/', views.agregar_practicante, name='agregar_practicante'),
    # path('practicantes-editar/<int:id>/', views.editar_practicante, name='editar_practicante'),
    # path('practicantes-borrar/<int:id>/', views.borrar_practicante, name='borrar_practicante'),
    #urls para evaluacion
#     path('crear_evaluacion/', views.crear_evaluacion, name='crear_evaluacion'),
    path('diseñar/', views.lista_evaluaciones, name='lista_evaluaciones'),
    path('evaluaciones_realizadas/', views.listar_evaluaciones_realizadas, name='listar_evaluaciones_realizadas'),
    path('evaluaciones_realizadas/<int:pk>/', views.detalle_evaluacionRealizada, name='detalle_evaluacionRealizada'),
    path('evaluaciones_realizadas/<int:pk>/editar/', views.editar_evaluacionRealizada, name='editar_evaluacionRealizada'),
    path('evaluaciones_realizadas/<int:pk>/borrar/', views.borrar_evaluacionRealizada, name='borrar_evaluacionRealizada'),
    
    path('evaluacion/<int:pk>/', views.detalle_evaluacion, name='detalle_evaluacion'),
    path('evaluacion/nueva/', views.nueva_evaluacion, name='nueva_evaluacion'),
    
    path('evaluacion/<int:pk>/editar/', views.editar_evaluacion, name='editar_evaluacion'),
    path('evaluacion/<int:pk>/borrar/', views.borrar_evaluacion, name='borrar_evaluacion'),
    
    path('elegir-evaluacion/<int:pk>/', views.elegir_evaluacion, name='elegir_evaluacion'),
    
    # path('elegir-evaluacion/', views.elegir_evaluacion, name='elegir_evaluacion'),

    # urls expositor
    path('expositores/', views.lista_expositores, name='lista_expositores'),
    path('expositor/<int:pk>/', views.detalle_expositor, name='detalle_expositor'),
    path('expositor/nueva/', views.crear_expositor, name='crear_expositor'),
    path('expositor/<int:pk>/editar/', views.editar_expositor, name='editar_expositor'),
    path('expositor/<int:pk>/borrar/', views.borrar_expositor, name='borrar_expositor'),
    
    #pruebas 
    # path('frecuencia-cardiaca/', views.frecuencia_cardiaca_view, name='frecuencia_cardiaca_view'),
    # path('api/frecuencia-cardiaca/', views.frecuencia_cardiaca, name='frecuencia_cardiaca'),
    # path('api/ultima_frecuencia/', views.ultima_frecuencia, name='ultima_frecuencia'),
    path('frecuencia-cardiaca/', views.receive_ecg_data, name='receive_ecg_data'),
    path('ecg-chart/', views.ecg_chart, name='ecg_chart'),
    path('ecg-data/', views.get_ecg_data, name='get_ecg_data'),
    path('ultima_frecuencia/', views.get_latest_ecg, name='get_latest_ecg'),
    
    path('iniciar_guardado/', views.iniciar_guardado, name='iniciar_guardado'),
    path('detener_guardado/', views.detener_guardado, name='detener_guardado'),
    path('recibir_datos/<int:evaluacion_id>/', views.recibir_datos, name='recibir_datos'),
    path('obtener_datos/', views.obtener_datos, name='obtener_datos'),
    path('ultima_frecuencia2/', views.get_latest_ecg2, name='get_latest_ecg2'),
    #url para evaluar a un expositor
    path('evaluar/<int:id>/<int:id_evaluacion>/', views.evaluar_expositor, name='evaluar_expositor'),
    ## para mandar el json
    path('evaluar_expositor/<int:id>/<int:id_evaluacion>/', views.evaluar_expositor, name='evaluar_expositor'),
    
    path('api/frecuencia/', views.recibir_frecuencia, name='recibir_frecuencia'),
    path('api/ultima_frecuencia/', views.obtener_frecuencia, name='obtener_frecuencia'),
    path('api/iniciar_guardado/', views.iniciar_guardado, name='iniciar_guardado'),
    path('api/detener_guardado/', views.detener_guardado, name='detener_guardado'),
    path('api/estado_guardado/', views.estado_guardado, name='estado_guardado'),
    path('api/obtener_id_evaluacion/', views.obtener_id_evaluacionRealizada, name='obtener_id_evaluacion'),
     
    path('listar_datos/', views.listar_datos, name='listar_datos'),
    path('api/verificar/', views.verificar_guardado, name='verificar_guardado'),
    path('exportar_evaluacion/<int:pk>/', views.exportar_evaluacion_excel, name='exportar_evaluacion_excel'),
 ]

