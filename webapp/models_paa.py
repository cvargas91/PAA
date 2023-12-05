from django.db import models
from django.conf import settings
from django_fsm import FSMField, transition
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils import timezone
#from .models import anios
import threading



MAX_LENGTH = 250
SHORT_LENGTH = 10
BYTES_LIMITE_CORREO_ELECTRICO = 25000000
PREFIJO_ASUNTO_MAIL = "[testing] "

anios = [
    (2023, 2023),
    (2024, 2024),
    (2025, 2025),
    (2026, 2026),
]

TIPOS_ROLES = (
        ('docencia', 'Docencia'),
        ('investigacion', 'Investigación'),
        ('vinculacion', 'Vinculación'),
)

# Define los tipos de roles específicos para cada tipo de planificación
ROLES_CHOICES = [
    ('docencia', (
        ('responsable_curso', 'Responsable del curso'),
        ('co_responsable', 'Co-responsable'),
        ('equipo', 'Parte del equipo'),
        ('coordinador', 'Coordinador de equipo docente'),
    )),
    ('investigacion', (
        ('investigador_principal', 'Investigador Principal'),
        ('co_investigador', 'Co-Investigador/a'),
        ('responsable_productos', 'Responsable de Productos'),
    )),
    ('vinculacion', (
        ('principal', 'Principal'),
        ('colaborador', 'Colaborador/a'),
        ('responsable_productos', 'Responsable de Productos'),
    )),
]

nombresRolDocencia = [
    ('Responsable del curso', 'Responsable del curso'),
    ('Co-responsable', 'Co-responsable'),
    ('Parte del equipo', 'Parte del equipo'),
    ('Coordinador/a equipo docente', 'Coordinador/a equipo docente'),
]

nombresRolInvestigacion = [
    ('Investigador/a principal', 'Investigador/a principal'),
    ('Co-investigador/a', 'Co-investigador/a'),
    ('Responsable de Productos', 'Responsable de Productos'),
]

nombresRolVinculacion = [
    ('Principal', 'Principal'),
    ('Colaborador/a', 'Colaborador/a'),
    ('Responsable productos', 'Responsable productos'),
]


class PAA_Asignatura (models.Model) :
    nombre = models.CharField(max_length=MAX_LENGTH, verbose_name='Nombre Asignatura')
    codigo = models.CharField(max_length=MAX_LENGTH, verbose_name='Código Asignatura')
    #descripcion = models.TextField(verbose_name='Descripción de Asignatura')
    departamento = models.TextField(verbose_name='Departamento de Asignatura', default='sinDepto')
    modalidad = models.TextField(verbose_name='Modalidad en que se imparte Asignatura', default='sinModalidad')
    estado = models.CharField(max_length=MAX_LENGTH, verbose_name='Estado Asignatura', default='No asignado')
    id_ucampus = models.PositiveSmallIntegerField(verbose_name='Id del curso de ucampus.uaysen.cl', null=True, blank=True)
    semestre = models.CharField('Semestre',max_length=MAX_LENGTH, null=True, blank=True)

    class Meta:
        verbose_name = "PAA - Asignatura"
        verbose_name_plural = "PAA - Asignaturas"

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.codigo)

class PAA_Planificacion (models.Model) :
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    #estado = models.CharField(max_length=50, verbose_name='Estado de la Planificación')
    estado = FSMField(verbose_name='Estado de la Planificación', default='Pendiente')
    rut_academicx = models.CharField(max_length=50, verbose_name='RUT del académicx', default='', null=True, blank=True)
    categoria = models.CharField(max_length=50, verbose_name='Categoría del académicx',default='',null=True, blank=True)
    departamento = models.CharField(max_length=50, verbose_name='Departamento del académicx',default='',null=True, blank=True)
    fecha_ingreso = models.DateField(verbose_name='Fecha ingreso a la Universidad',null=True,blank=True)
    jornada = models.CharField(max_length=50, verbose_name='Jornada académicx en horas',default='',null=True, blank=True)
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)    
    anio = models.PositiveIntegerField(choices=anios, verbose_name='Año')
    total_horas = models.PositiveIntegerField('Total Horas', null=True, blank=True)
    accion = models.ForeignKey('Accion',on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Acción')

    class Meta:
        verbose_name = "PAA - Planificación de Académico"
        verbose_name_plural = "PAA - Planificaciones de Académico"

    def __str__(self):
        txt = "Planificación"
        txt+= " de {}:".format(self.usuario.username)
        return txt
    
    @transition(field=estado, source='Pendiente', target='Enviado_jefe_dpto')
    def enviado_a_jefeDpto(self):
        pass

    @transition(field=estado, source='Enviado_jefe_dpto', target='Pendiente')
    def rechazo_jefeDpto(self):
        pass

    @transition(field=estado, source='Enviado_jefe_dpto', target='Enviado_direccion')
    def enviado_a_direccion(self):
        pass

    @transition(field=estado, source='Enviado_direccion', target='Enviado_jefe_dpto')
    def rechazo_direccion(self):
        pass

    @transition(field=estado, source='Enviado_direccion', target='Aceptado_direccion')
    def aceptado_direccion(self):
        pass    
    
class PAA_PlanificacionDocencia (models.Model):    
    #clave "asignatura" se setea en nulo en caso de eliminación de una asignatura, así; no perder información de la planificación
    planificacion = models.ForeignKey(PAA_Planificacion, related_name='planificaciones_docencia', blank=True, null=True,on_delete=models.CASCADE)
    asignatura = models.ForeignKey(PAA_Asignatura, related_name='asignatura',null=True, blank=True,on_delete=models.SET_NULL)
    tipo = models.CharField('Tipo Planificacion',max_length=MAX_LENGTH, null=True, blank=True)
    rol = models.CharField('Rol Docencia',max_length=MAX_LENGTH, null=True, blank=True,choices=nombresRolDocencia, default="")
    semestre = models.CharField('Semestre',max_length=MAX_LENGTH, null=True, blank=True)
    cantidad_horas = models.PositiveIntegerField('Cantidad Horas', null=True)
    programa = models.TextField(verbose_name='Programa', null=True, blank=True)
    descripcion = models.TextField(verbose_name='Descripción de Actividad/Programacion', null=True, blank=True)
    observacion = models.TextField(verbose_name='Observaciones Programa', null=True, blank=True)

    class Meta:
        verbose_name = "PAA - Planificación Docencia de Académico"
        verbose_name_plural = "PAA - Planificaciones Docencia de Académico"

    def __str__(self):
        txt = "Planificación Docencia"
        txt+= " de {}:".format(self.planificacion.usuario.username)
        return txt
    
class PAA_PlanificacionInvestigacion (models.Model):
    planificacion = models.ForeignKey(PAA_Planificacion, related_name='planificaciones_investigacion', blank=True, null=True,on_delete=models.CASCADE)
    nombre_proyecto = models.TextField(verbose_name='Nombre del Proyecto', null=True, blank=True)
    descripcion = models.TextField(verbose_name='Descripción de Actividad', null=True, blank=True)    
    tipo = models.CharField('Tipo Planificación',max_length=MAX_LENGTH, null=True, blank=True)    
    rol = models.CharField('Rol Investigación',max_length=MAX_LENGTH, null=True, blank=True,choices=nombresRolInvestigacion, default="")
    cantidad_horas = models.PositiveIntegerField('Cantidad Horas', null=True)
    estado_proyecto = models.CharField('Estado del Proyecto',max_length=MAX_LENGTH, null=True, blank=True)
    autoria = models.CharField('Calidad Autoria',max_length=MAX_LENGTH, null=True, blank=True)
    fuente_financiamiento = models.CharField('Fuente Financiamiento',max_length=MAX_LENGTH, null=True, blank=True)

    class Meta:
        verbose_name = "PAA - Planificación Investigación de Académico"
        verbose_name_plural = "PAA - Planificaciones Investigación de Académico"

    def __str__(self):
        txt = "Planificación Docencia"
        txt+= " de {}:".format(self.planificacion.usuario.username)
        return txt
    
class PAA_PlanificacionGestion (models.Model):
    planificacion = models.ForeignKey(PAA_Planificacion, related_name='planificaciones_gestion', blank=True, null=True,on_delete=models.CASCADE)
    nombre_actividad = models.TextField(verbose_name='Nombre de la Actividad', null=True, blank=True)
    cantidad_horas = models.PositiveIntegerField('Cantidad Horas', null=True)
    cargo = models.CharField('Cargo Actividad',max_length=MAX_LENGTH, null=True, blank=True)

    class Meta:
        verbose_name = "PAA - Planificación Gestión Institucional de Académico"
        verbose_name_plural = "PAA - Planificaciones Gestión Institucional de Académico"

    def __str__(self):
        txt = "Planificación Gestión Institucional"
        txt+= " de {}:".format(self.planificacion.usuario.username)
        return txt

class PAA_PlanificacionVinculacion (models.Model):
    planificacion = models.ForeignKey(PAA_Planificacion, related_name='planificaciones_vinculacion', blank=True, null=True,on_delete=models.CASCADE)
    nombre_actividad = models.TextField(verbose_name='Nombre de la Actividad', null=True, blank=True)
    cantidad_horas = models.PositiveIntegerField('Cantidad Horas', null=True)
    unidad = models.CharField('Unidad Encargada',max_length=MAX_LENGTH, null=True, blank=True)
    rol = models.CharField('Rol Vinculación con el medio',max_length=MAX_LENGTH, null=True, blank=True,choices=nombresRolVinculacion, default="")
    linea_accion = models.CharField('Línea de acción de la Actividad',max_length=MAX_LENGTH, null=True, blank=True)
    frecuencia = models.CharField('Frecuencia de la Actividad',max_length=MAX_LENGTH, null=True, blank=True)
    fecha_inicio = models.DateField('Fecha inicio Actividad', blank=True, null=True)
    fecha_fin = models.DateField('Fecha termino Actividad', blank=True, null=True)

    class Meta:
        verbose_name = "PAA - Planificación Vinculación con el Medio de Académico"
        verbose_name_plural = "PAA - Planificaciones Vinculación con el Medio de Académico"

    def __str__(self):
        txt = "Planificación Vinculación con el Medio"
        txt+= " de {}:".format(self.planificacion.usuario.username)
        return txt

class PAA_PlanificacionFormacion (models.Model):
    planificacion = models.ForeignKey(PAA_Planificacion, related_name='planificaciones_formacion', blank=True, null=True,on_delete=models.CASCADE)
    nombre_actividad = models.TextField(verbose_name='Nombre de la Actividad', null=True, blank=True)
    cantidad_horas = models.PositiveIntegerField('Cantidad Horas', null=True)
    institucion = models.TextField(verbose_name='Institución que realiza la Actividad', null=True, blank=True)
    fecha_inicio = models.DateField('Fecha inicio Actividad')
    fecha_fin = models.DateField('Fecha termino Actividad')

    class Meta:
        verbose_name = "PAA - Planificación Actividades Formativas de Académico"
        verbose_name_plural = "PAA - Planificaciones Actividades Formativa de Académico"

    def __str__(self):
        txt = "Planificación Actividades Formativas"
        txt+= " de {}:".format(self.planificacion.usuario.username)
        return txt


# class PAA_Rol(models.Model):
#     planificacion = models.ForeignKey(PAA_Planificacion, on_delete=models.CASCADE, null=True)
#     tipo = models.CharField(max_length=20, choices=TIPOS_ROLES)
#     rol = models.CharField(
#         max_length=30,
#         choices=ROLES_CHOICES,  # Establece las opciones iniciales como 'docencia'
#         blank=True,
#     )

#     class Meta:
#         verbose_name = "PAA - Rol de la Planificación Académica"
#         verbose_name_plural = "PAA - Roles de la Planificación Académica"

#     def __str__(self):
#         return f"Rol de {self.tipo} en Planificación Académica"        

class PAA_ObservacionPlanificacion(models.Model) :
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    planificacion = models.ForeignKey('PAA_Planificacion', on_delete=models.SET_NULL, null=True)    
    observacion = models.TextField(verbose_name='Observación de la Planificación')
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "PAA - Observación de la Planificación Académica"
        verbose_name_plural = "PAA - Observaciones de la Planificación Académica"

    def __str__(self):
        txt = "Observación"        
        txt += " de Planificación de académico/a: {}".format(self.planificacion.usuario.username)        
        return txt