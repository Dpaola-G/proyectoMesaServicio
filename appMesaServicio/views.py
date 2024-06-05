from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render
from appMesaServicio.models import *
from random import *
from django.conf import settings
from django.db import Error, transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from smtplib import SMTPException

# Create your views here.
def inicio(request):
    return render (request, "frmIniciarSesion.html")


def inicioAdministrador (request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user, "rol":request.user.groups.get().name}
        return render (request, "administrador/inicio.html", datosSesion)
    else:
        mensaje ="debe iniciar sesión"
        return render (request, "frmIniciarSesion.html", {"mensaje": mensaje})
    

def inicioTecnico (request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user, "rol":request.user.groups.get().name}
        return render (request, "tecnico/inicio.html", datosSesion)
    else:
        mensaje ="debe iniciar sesión"
        return render (request, "frmIniciarSesion.html", {"mensaje": mensaje})


def inicioEmpleado (request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user, "rol":request.user.groups.get().name}
        return render (request, "empleado/inicio.html", datosSesion)
    else:
        mensaje ="debe iniciar sesión"
        return render (request, "frmIniciarSesion.html", {"mensaje": mensaje})
    

@csrf_exempt
def login(request):
    username=request.POST['txtUser']
    password=request.POST['txtPassword']
    user= authenticate(username=username, password=password)
    if user is not None:
        # registrar la variable de sesión
        auth.login(request, user)
        if user.groups.filter(name="Administrador").exists():
            return redirect('/inicioAdministrador')
        elif user.groups.filter(name='Tecnico').exists():
            return redirect('/inicioTecnico')
        else:
            return redirect('/inicioEmpleado')
        
    else:
        mensaje = "usuario o contraseña incorrecto"
        return render(request, "frmIniciarSesion.html", {"mensaje":mensaje})    


def vistaSolicitud (request):
    if request.user.is_authenticated:
        #consultar las oficinas y hambientes registrados
        oficinaAmbientes = OficinaAmbiente.objects.all()
        datosSesion = {"user": request.user,
                       "rol":request.user.groups.get().name,
                       'oficinaAmbientes':oficinaAmbientes}
        return render(request, 'empleado/solicitud.html',datosSesion)      
    else:
        mensaje = "debe iniciar sesion"
        return render(request, "frmIniciarSesion.html",{"mensaje":mensaje})


def registrarSolicitud(request):
    try:
        with transaction.atomic():
            user = request.user
            descripcion = request.POST ['descripcion']
            idOficina = request. POST ['cbOficina']
            oficinaAmbiente = OficinaAmbiente.objects.get(pk=idOficina)
            solicitud = Solicitud (solUsuario = user,
                                    solDescripción = descripcion,
                                    solOficinaAmbiente = oficinaAmbiente)
            solicitud.save()
            fecha = datetime.now()
            year = fecha.year
            consecutivoCaso = Solicitud.objects.filter(
                fechaHoraCreacion__year=year).count()
            consecutivoCaso = str(consecutivoCaso).rjust(5, '0')
            codigoCaso = f"REQ-{year}-{consecutivoCaso}"
            userCaso = User.objects.filter(
                groups__name__in=['Administrador']).first()
            estado = "Solicitada"
            caso = Caso(
                casoSolicitud=solicitud,
                casCodigo=codigoCaso,
                casUsuario=userCaso,
                casEstado=estado,
            )
            caso.save()
            asunto = 'Registro Solicitud - Mesa De Servicio'
            mensaje = (f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos '
                       f'informarle que su solicitud fue registrada en nuestro sistema con el número de caso '
                       f'<b>{
                           codigoCaso}</b>. <br><br> Su caso será gestionado en el menor tiempo posible, '
                       f'según los acuerdos de solución establecidos para la Mesa de Servicios del CTPI-CAUCA.'
                       f'<br><br>Lo invitamos a ingresar a nuestro sistema en la siguiente url: '
                       'http://mesadeservicioctpicauca.sena.edu.co.')
            thread = threading.Thread(
                target = enviarCorreo, args=(asunto, mensaje, [user.email]))
            thread.start()
            mensaje = "Se ha registrado su solicitud de manera exitosa"
    except Exception as e:
        transaction.rollback()
        mensaje = f"Error: {e}"
        return render(request, "error.html", {"message": mensaje})

def enviarCorreo(asunto=None, mensaje=None, destinatario=None, archivo=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('correo.html')
    contenido = template.render({
        'mensaje': mensaje
    })
    try:
        correo = EmailMultiAlternatives(
            asunto, mensaje, remitente, destinatario
        )
        correo.attach_alternative(contenido, 'text/html')
        if archivo != None:
            correo.attach_file(archivo)
        correo.send(fail_silently=True)
        print("enviado")
    except SMTPException as error:
        print(error)

        
        
        
def listarCasos(request):
    try:
        listaCasos=Caso.objects.all()
    
        
    except Error as error:
        mensaje = str (error)     
        
    retorno = {"listaCasos":listarCasos, "mensaje":mensaje}
    return render (request,("administrador/listarCasos.html" ))       
        
        
def listarEmpleadosTecnicos(request):
    try:
        #consulta para obtener todos los empleados con rol tecnico
        tecnicos = User.objects.filter(groups__name__in=['tecnico'])
    except Error as error:
        mensaje=str(error)  
    retorno = {"tecnicos":tecnicos, "mensaje":mensaje}     
                



def Salir(request):
    auth.logout(request)
    return render(request, "frmIniciarSesion.html", {"mensaje": "Ha cerrado la sesión"})