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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from tasks.views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('logout/', views.signout, name='logout'),
    path('', views.inicio, name='inicio'),
    path('login/', views.signin, name='signin'),

    # urls usuario
    path('administrar/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='borrar_usuario'),

    # urls evaluacion
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

    # urls expositor
    path('expositores/', views.lista_expositores, name='lista_expositores'),
    path('expositor/<int:pk>/', views.detalle_expositor, name='detalle_expositor'),
    path('expositor/nueva/', views.crear_expositor, name='crear_expositor'),
    path('expositor/<int:pk>/editar/', views.editar_expositor, name='editar_expositor'),
    path('expositor/<int:pk>/borrar/', views.borrar_expositor, name='borrar_expositor'),
    
    #pruebas datos sensor
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
    ## para mandar el json de la evaluacion a oculus
    path('evaluar_expositor/<int:id>/<int:id_evaluacion>/', views.evaluar_expositor, name='evaluar_expositor'),
    
    #urls para la api arduino-web
    path('api/frecuencia/', views.recibir_frecuencia, name='recibir_frecuencia'),
    path('api/ultima_frecuencia/', views.obtener_frecuencia, name='obtener_frecuencia'),
    path('api/iniciar_guardado/', views.iniciar_guardado, name='iniciar_guardado'),
    path('api/detener_guardado/', views.detener_guardado, name='detener_guardado'),
    path('api/estado_guardado/', views.estado_guardado, name='estado_guardado'),
    path('api/obtener_id_evaluacion/', views.obtener_id_evaluacionRealizada, name='obtener_id_evaluacion'),
     
    path('listar_datos/', views.listar_datos, name='listar_datos'),
    path('api/verificar/', views.verificar_guardado, name='verificar_guardado'),
    path('exportar_evaluacion/<int:pk>/', views.exportar_evaluacion_excel, name='exportar_evaluacion_excel'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    
    ## recuperar contraseña o cambiar contraseña
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    ##no borrar, es para probar el envio de datos con la api de sendgrid
    path('send-test-email/', views.send_test_email, name='send_test_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)