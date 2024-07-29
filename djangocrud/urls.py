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
from django.contrib import admin
from django.urls import path
from tasks import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
     path('api/frecuencia/', views.recibir_frecuencia, name='recibir_frecuencia'),
     path('api/ultima_frecuencia/', views.obtener_frecuencia, name='obtener_frecuencia'),
  path('frecuencia-cardiaca/', views.mostrar_frecuencia_cardiaca, name='frecuencia_cardiaca'),
     path('a/', views.evaluation_list, name='disenar_evaluacion'),
     path('api/guardar_evaluacion/', views.guardar_evaluacion, name='guardar_evaluacion'),
#    path('frecuencia-cardiaca/', views.frecuencia_cardiaca, name='frecuencia_cardiaca'),
#codigo lucho 
    path('', views.index, name='index'),
    #path('practicantes/', views.listar_practicantes, name='listar_practicantes'),
    path('practicantes-agregar/', views.agregar_practicante, name='agregar_practicante'),
    path('diseñar/', views.disenar,),
    path('administrar/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    # urls para practicante
    path('practicantes/', views.listar_practicantes, name='listar_practicantes'),
    path('practicantes-agregar/', views.agregar_practicante, name='agregar_practicante'),
    path('practicantes-editar/<int:id>/', views.editar_practicante, name='editar_practicante'),
    path('practicantes-borrar/<int:id>/', views.borrar_practicante, name='borrar_practicante'),
]

