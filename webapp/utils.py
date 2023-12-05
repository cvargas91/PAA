from django.db.models import Sum
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models_paa import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q


def getAccionesPorRol (serializer):    
    accionesPorRol = {}

    if len(serializer.data) > 0:
        origen = serializer.data[0]['accion']['origen']        
    else:
        return accionesPorRol    
        
    for rol in serializer.data:        
        if(rol['accion']['origen'] == "POA"):            
            if(rol['accion']['proyecto'] is None):
                origen = "TRANSVERSAL"
            else:
                origen = "URY"
        else:
            origen = rol['accion']['origen']

        accionesPorRol.setdefault(origen, []).extend([rol])

    return accionesPorRol


def validaDependencia(actor):    
    dependencia = actor.dependencia    
    actores = [actor]
    while dependencia is not None:        
        if dependencia.dependencia is None:                      
            actores.append(dependencia)            
            return actores            
        
        dependencia = dependencia.dependencia
    return None

def sumaHorasPlanificacion(queryset, campo):
    suma = queryset.aggregate(Sum(campo))
    return suma[campo + "__sum"] or 0

def porcentajeHorasPlanificacion(total_actividad, total_horas):
    return round((total_actividad / total_horas) * 100, 2)

def usuarios_mismo_departamento(departamento):
    # usuarios_departamento = PerfilUsuario.objects.filter(
    # Q(actor__nombre=departamento) | Q(actor__dependencia__nombre=departamento)
    # ).select_related('usuario')
    usuarios_departamento = PerfilUsuario.objects.filter(
        Q(actor__nombre=departamento) | Q(actor__dependencia__nombre=departamento),
        Q(perfil_planificacion='Académico') | Q(perfil_planificacion__isnull=True)
    ).select_related('usuario')

    usuarios_json = []
    for perfil in usuarios_departamento:
        usuario = perfil.usuario
        usuario_info = {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'nombre': usuario.first_name,
            'apellido': usuario.last_name,
            'perfil' : {
                'actor_id' : perfil.actor.id,
                'actor_nombre' : perfil.actor.nombre,
                'area_sigla' : perfil.actor.dependencia.sigla if perfil.actor.dependencia else perfil.actor.sigla,
                'esAreaAcademico' : perfil.actor.categoria,
                'esEncargado' : perfil.es_encargado,
                'planificacionAcademica' : perfil.perfil_planificacion,
            }
        }
        usuarios_json.append(usuario_info)
    
    return usuarios_json
##################################################################
#   Sección Workflow cambios de estado Planificación Académica   #
##################################################################
@api_view(['POST'])
def planificacionEnvioAJefeDpto(request):
    '''
        Evento del workflow donde perfil académico envía
        una planificación académica a Jefe Departamento
    '''
    
    try:
        datosRequest = request.data
        planificacion = get_object_or_404(PAA_Planificacion, pk=datosRequest['planificacion'])
        planificacion.enviado_a_jefeDpto()
        planificacion.save()
        return JsonResponse({'message': 'Planificación actualizada exitosamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)})     

@api_view(['POST'])
def planificacionJefeDptoRechaza(request):
    '''
        Evento del workflow donde perfil Jefe Departamento rechaza/observa
        una planificación académica
    '''
    try:
        datosRequest = request.data
        planificacion = get_object_or_404(PAA_Planificacion, pk=datosRequest['planificacion'])
        planificacion.rechazo_jefeDpto()
        planificacion.save()

        PAA_ObservacionPlanificacion.objects.create(
            usuario = request.user,
            planificacion = planificacion,
            observacion = datosRequest['observacion']
        )
        return JsonResponse({'message': 'Planificación actualizada exitosamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)})

    

@api_view(['POST'])
def planificacionJefeDptoAcepta(request):
    '''
        Evento del workflow donde perfil Jefe Departamento
        acepta una planificación académica y se envia a dirección académica
    '''
    try:
        datosRequest = request.data

        planificacion = get_object_or_404(PAA_Planificacion, pk=datosRequest['planificacion'])
        planificacion.enviado_a_direccion()
        planificacion.save()

        return JsonResponse({'message': 'Planificación actualizada exitosamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)})    

def planificacionDireccionRechaza(request):
    '''
        Evento del workflow donde perfil Dirección Académica rechaza/observa
        una planificación académica
    '''
    try:
        datosRequest = request.data

        planificacion = get_object_or_404(PAA_Planificacion, pk=datosRequest['planificacion'])
        planificacion.rechazo_direccion()
        planificacion.save()

        PAA_ObservacionPlanificacion.objects.create(
            usuario = request.user,
            planificacion = planificacion,
            observacion = datosRequest['observacion']
        )

        return JsonResponse({'message': 'Planificación actualizada exitosamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)})    

@api_view(['POST'])
def planificacionDireccionAcepta(request):
    '''
        Evento del workflow donde perfil Dirección Académica finalmente
        acepta una planificación académica
    '''
    try:
        datosRequest = request.data

        planificacion = get_object_or_404(PAA_Planificacion, pk=datosRequest['planificacion'])
        planificacion.aceptado_direccion()
        planificacion.save()
        return JsonResponse({'message': 'Planificación actualizada exitosamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
@api_view(['POST'])
def planificacionVinculacionCompromisos(request):
    '''
        Vincula planificación de un academicx con los compromisos del departamento
    '''
    try:
        datosRequest = request.data
        accion_id = datosRequest['accion']
        accion = get_object_or_404(Accion, id=accion_id)

        planificacion = get_object_or_404(PAA_Planificacion, pk=datosRequest['planificacion'])
        planificacion.accion = accion
        planificacion.save()
        
        return JsonResponse({'message': 'Planificación actualizada exitosamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)})    
    
##################################################################
#   Sección Workflow cambios de estado Planificación Académica   #
##################################################################
