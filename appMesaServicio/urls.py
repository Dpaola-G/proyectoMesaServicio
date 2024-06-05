from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.inicio),
    path('login/', views.login),
    path('vistaSolicitud/', views.vistaSolicitud),
    path('inicioAdministrador/', views.inicioAdministrador),
    path('inicioTecnico/', views.inicioTecnico),
    path('inicioEmpleado/', views.inicioEmpleado),   
    path('listarCasosParaAsignar/', views.listarCasos),   
    path('salir/', views.Salir)
 
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
