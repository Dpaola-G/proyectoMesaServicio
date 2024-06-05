from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here 

tipoOficinaAmbiente=[
    ('Administrativo','Administrativo'),
    ('Formacion','Formacion')
]

tipoUsuario = [
    ('Administrativo', 'Administrativo'),
    ('Instructor', 'Instructor')
]

estadoCaso =[
    ('solicitada', 'solicitada'),
    ('En Proceso', 'En Proceso'),
    ('Finalizada', 'Finalizada')
]

class OficinaAmbiente(models.Model):
    ofiTipo = models.CharField(max_length=15, choices=tipoOficinaAmbiente,
                    db_comment="tipo de oficina")
    ofiNombre = models.CharField(max_length=50, unique=True, db_comment="Nombre de la oficina o ambiente")
    
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True,
                                             db_comment="fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True,
                                                  db_comment="fecha y hora ultima creacion")

    def __str__(self) -> str:
        return self.ofiNombre

class User(AbstractUser):
    userTipo = models.CharField(max_length=15, choices=tipoUsuario)
    userFoto=models.ImageField(
        upload_to=f"fotos/", null=True, blank=True, db_comment="foto usuario")
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True,
                                             db_comment="fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True,
                                                  db_comment="fecha y hora ultima creacion")


    def __str__(self) -> str:
        return self.username
    
class Solicitud(models.Model):
    solUsuario=models.ForeignKey (User, on_delete=models.PROTECT, 
                                  db_comment="hace referencia al empleado que hace la solicitud")    
    
    solDescripcion = models.TextField(max_length=1000, 
                                      db_comment="Texto que describe la solicitud del empleado")
    
    solOficinaAmbiente = models.ForeignKey(OficinaAmbiente, on_delete=models.PROTECT,
                                           db_comment="hace referencia  a la oficina o ambiente donde se encuentra el equipo de la solicitud")
    
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True,
                                             db_comment="fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True,
                                                  db_comment="fecha y hora ultima creacion")

    def __str__(self) -> str:
        return self.solDescripcion
    
class Caso(models.Model):
    casoSolicitud = models.ForeignKey(Solicitud, on_delete=models.PROTECT,
                                      db_comment="hace referencia a la solicitud")
    casCodigo = models.CharField(max_length=10, unique=True,
                                  db_comment="codigo unico del caso")
    casUsuario= models. ForeignKey(User, on_delete=models.PROTECT,
                                   db_comment="empleado de soporte tecnico asignado")
    casEstado = models.CharField(max_length=15, choices=estadoCaso)
    
    # fechaHoraCreacion = models.DateTimeField(auto_now_add=True,
    #                                          db_comment="fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now_add=True,
                                                  db_comment="fecha y hora ultima creacion")
    
class TipoProcedimiento(models.Model):
    tipNombre = models.CharField(max_length=20, unique=True,
                                  db_comment="Nombre del tipo de procedimiento")
    tipDescripcion = models.TextField(max_length=1000,
                                      db_comment="Descripcion del tipo de procedimiento")
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True,
                                             db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now= True,
                                                      db_comment="Fecha y hora de la ultima actualzacion")
    
class SolucionCaso(models.Model):
    solCaso = models.ForeignKey(Caso, on_delete=models.PROTECT,
                                db_comment="hace referencia al caso que genera la solucion del problema")
    
    solProcedimiento = models.TextField(max_length=1000,                               
                                      db_comment="65")
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True,
                                             db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now= True,
                                                      db_comment="Fecha y hora de la ultima actualzacion")


    def __str__(self) -> str:
        return self.solTipoSolucion
    
class SolucionCasoTipoProcedimientos (models.Model):
    solSoluciones = models.ForeignKey(SolucionCaso, on_delete=models.PROTECT,
                                      db_comment="hace referencia a la solucion del caso")
    
    solTipoProcedimiento = models.ForeignKey(TipoProcedimiento, on_delete=models.PROTECT,
                                      db_comment="hace referencia a la solucion del caso")

