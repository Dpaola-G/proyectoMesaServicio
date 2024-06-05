from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from appMesaServicio.models import *
from random import randint
from django.db import Error, transaction
from django.views.decorators.csrf import csrf_exempt

def inicio(request):
    return render(request, "frmIniciarSesion.html")

def inicioAdministrador(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user, "rol": request.user.groups.get().name}
        return render(request, "administrador/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})

def inicioTecnico(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user, "rol": request.user.groups.get().name}
        return render(request, "tecnico/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})

def inicioEmpleado(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user, "rol": request.user.groups.get().name}
        return render(request, "empleado/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('txtUser')
        password = request.POST.get('txtPassword')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name="Administrador").exists():
                return redirect('inicioAdministrador')
            elif user.groups.filter(name='Tecnico').exists():
                return redirect('inicioTecnico')
            else:
                return redirect('inicioEmpleado')
        else:
            mensaje = "Usuario o contraseña incorrectos"
            return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})
    else:
        return redirect('inicio')

def vistaSolicitud(request):
    if request.user.is_authenticated:
        oficinaAmbientes = OficinaAmbiente.objects.all()
        datosSesion = {"user": request.user, "rol": request.user.groups.get().name, 'oficinaAmbientes': oficinaAmbientes}
        return render(request, "empleado/solicitud.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "frmIniciarSesion.html", {"mensaje": mensaje})

def registrarSolicitud(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user = request.user
                descripcion = request.POST.get('descripcion')
                idOfAmb = request.POST.get('idOfAmb')
                oficinaAmbiente = OficinaAmbiente.objects.get(pk=idOfAmb)
                solicitud = Solicitud(solUsuario=user, solDescripción=descripcion, solOficinaAmbiente=oficinaAmbiente)
                solicitud.save()
                consecutivoCaso = randint(1, 10000)
                codigoCaso = "REQ" + str(consecutivoCaso).rjust(5, '0')
                userCaso = User.objects.filter(groups__name__in=['Administrador']).first()
                estado = "Solicitada"
                caso = Caso(casSolicitud=solicitud, casCodigo=codigoCaso, casUsuario=userCaso, casEstado=estado)
                caso.save()
        except Error as error:
            mensaje = f"{error}"
    else:
        mensaje = "Método no permitido"
    return render(request, "empleado/solicitud.html", {"mensaje": mensaje})

def listarCasos(request):
    try:
        listaCasos = Caso.objects.all()
    except Error as error:
        mensaje = str(error)
    retorno = {"listaCasos": listaCasos, "mensaje": mensaje}
    return render(request, "administrador/listarCasos.html", retorno)

def listarEmpleadosTecnicos(request):
    try:
        tecnicos = User.objects.filter(groups__name__in=['Tecnico'])
    except Error as error:
        mensaje = str(error)
    retorno = {"tecnicos": tecnicos, "mensaje": mensaje}
    return render(request, "administrador/listarEmpleadosTecnicos.html", retorno)

def Salir(request):
    logout(request)
    return render(request, "frmIniciarSesion.html", {"mensaje": "Ha cerrado la sesión"})
