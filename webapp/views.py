import mimetypes
from django.views.generic import ListView, View
import sys
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from spci.settings import STATIC_ROOT, STATIC_URL, \
    UCAMPUS_API,UCAMPUS_USER,UCAMPUS_PASS, TIME_ZONE
from .models import Accion, Actor, PerfilUsuario, Meta, Estrategia, \
    nombresRol as opcionesRoles, \
    tiposAccion as opcionesTipos, \
    tiposTactica as opcionesTacticas, \
    meses as opcionesMeses, \
    Plazo
## Para reportes ##
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
##
## Para Planificación Académica ##
from .models_paa import *
from urllib.parse import quote
import pytz
## Para Planificación Académica ##
##
from .serializers import *
from django.db.models import Q, Sum,FloatField
from django.db.models.functions import Cast
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import os
from collections import defaultdict
from datetime import datetime
import requests, logging
import locale
from .utils import *

# def. de constantes
CALLBACK_URI = '/gCallback'
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"]
SUBDOMAIN_URL = os.getenv('API_GOOGLE_SUBDOMAIN_URL')
LOCAL = eval(os.getenv('API_GOOGLE_LOCAL'))
# fin def. de constantes

def getPerfilUsuario(request) :    
    perfilUsuario = request.user.perfilusuario_set.first()    
    if 'perfil' in request.session and request.session['perfil'] != perfilUsuario.actor.nombre :        
        return request.user.perfilusuario_set.get(actor__nombre=request.session['perfil'])
    return perfilUsuario
        
def index(request):
    if request.user and request.user.is_authenticated :
        perfiles = User.objects.filter(email=request.user.email).first().perfilusuario_set.all()
        cantidadPerfiles = len(perfiles)
        if cantidadPerfiles == 0 :
            return render(request, 'webapp/sinPerfil.html', {})
        elif cantidadPerfiles > 1 :
            detallePerfiles = []
            for perfil in perfiles :
                detallePerfiles.append(
                    {'perfil' : perfil.actor.nombre,
                    'es_encargado' : perfil.es_encargado})            
            detallePerfiles = sorted(detallePerfiles, key=lambda x: x['perfil'])

            return render(request, 'webapp/escogePerfil.html',
                {'nombreUsuario' : '{} {}'.format(request.user.first_name, request.user.last_name),
                'perfiles' : detallePerfiles})
        return redirect('/app')
    else :
        return redirect('/gRedirect')

@require_http_methods(["POST"])
def seteaPerfil(request):
    request.session['perfil'] = request.POST['perfil']
    return redirect('/app')

def datosIniciales(request) :
    perfilUsuario = getPerfilUsuario(request)

    return JsonResponse({
        'usuario': {
            'id' : request.user.id,
            'username' : request.user.username,
            'nombre' : request.user.first_name,
            'apellido' : request.user.last_name,
            'perfil' : {
                'actor_id' : perfilUsuario.actor.id,
                'actor_nombre' : perfilUsuario.actor.nombre,
                'area_sigla' : perfilUsuario.actor.dependencia.sigla if perfilUsuario.actor.dependencia else perfilUsuario.actor.sigla,
                'esAreaAcademico' : perfilUsuario.actor.categoria == "académicas",
                'esEncargado' : perfilUsuario.es_encargado,
                'esAnalistaUPCI' : perfilUsuario.es_analistaUPCI,
                'esMultiPerfil' : len(request.user.perfilusuario_set.all()) > 1,
                'foto' : perfilUsuario.foto,
                'planificacionAcademica' : perfilUsuario.perfil_planificacion,
            }
        },
        'opciones' : {
            'actores' : list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Actor.objects.values_list('id', 'nombre')))),
            'roles' : ["Todos"] + list(map(lambda x : x[0], opcionesRoles)),
            'tipos' : ["Todos"] + list(map(lambda x : x[0], opcionesTipos)),
            'tacticas' : ["Todas"] + list(map(lambda x : x[0], opcionesTacticas)),
            'meses' : ["Todos"] + list(map(lambda x : x[0], opcionesMeses))
        }
    })
    
def gRedirect(request) :
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=SCOPES)
    flow.redirect_uri = "https://{}{}".format(SUBDOMAIN_URL, CALLBACK_URI)
    authorization_url, state = flow.authorization_url(access_type='offline')
    return redirect(authorization_url)

def gCallback(request) :
    state = request.GET['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=SCOPES,
        state=state)

    authorization_response = None
    flow.redirect_uri = "https://{}{}".format(SUBDOMAIN_URL, CALLBACK_URI)
    uri_https = str(request.build_absolute_uri()).replace("http://", "https://")
    #authorization_response = request.build_absolute_uri()
    authorization_response = uri_https
    try :
        flow.fetch_token(authorization_response=authorization_response)
    except :
        return render(request, 'webapp/error.html', {'error' : str(sys.exc_info())})
    credentials = flow.credentials
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
    if user_info['verified_email'] and user_info['hd'] =='uaysen.cl' :
        current_user = User.objects.filter(username=user_info['email']).first()
        if not current_user :
            return render(request, 'webapp/sinUsuario.html', {})
        for perfil in current_user.perfilusuario_set.all() :
            perfil.sesion = {
                'token' : credentials.token,
                'refresh_token' : credentials.refresh_token,
                'token_uri' : credentials.token_uri,
                'client_id' : credentials.client_id,
                'client_secret' : credentials.client_secret,
                'scopes' : credentials.scopes
            }
            perfil.save()
        login(request, current_user)
    else :
        raise PermissionDenied()
    return redirect('/')

def getCredentials(request) :
    perfilUsuario = getPerfilUsuario(request)    
    return JsonResponse({'g_access_token': perfilUsuario.sesion["token"]})

def app(request):
    context = {'state': 'ok'}
    return render(request, 'webapp/app.html', context)

#Conexión API UCAMPUS // Planificación Anual Académica
def consultar_api_ucampus(api: str, params={}):
    
    result = requests.get(
        f'{UCAMPUS_API}/{api}', params=params,
        auth=(UCAMPUS_USER, UCAMPUS_PASS)
    )
    
    if result.status_code != 200:
        raise Exception(
            f'ha habido un error al intentar consultar {UCAMPUS_API}/{api}\n'
            f'\tparams: {params}\n\n'
            f'error {result.status_code}: {result.text}'
        )

    return result.json()

@api_view(['GET'])
def obtener_cursos(request):    
    periodos = ["2023.1", "2023.2"]
    cursos_api = []
    for periodo in periodos:
        cursos_periodo = consultar_api_ucampus(api='cursos', params={'periodo': periodo})
        cursos_api.extend(cursos_periodo)

    nuevos_cursos = []

    for curso in cursos_api:        
        id_curso = int(curso['id_curso'])
        cursos_existentes = PAA_Asignatura.objects.filter(id_ucampus=id_curso)
        if not cursos_existentes:

            nuevo_curso = PAA_Asignatura(
                id_ucampus=id_curso,
                nombre=curso['nombre'],
                codigo=curso['codigo'],
                departamento=curso['departamento'],
                modalidad=curso['modalidad'],
                semestre=curso['periodo_texto']
            )
            nuevos_cursos.append(nuevo_curso)

    PAA_Asignatura.objects.bulk_create(nuevos_cursos)

    return Response(cursos_api)

@api_view(['GET'])
def obtener_cursos_dictados(periodo):
    return consultar_api_ucampus(api='cursos_dictados.json', params={'periodo[]': periodo})

@api_view(['GET'])
def obtener_profesores(request):
    periodo = "2023.1";
    # return consultar_api_ucampus(api='cursos.json', params={'periodo[]': periodo})
    cursos_api = consultar_api_ucampus(api='profesores', params={'periodo': periodo}) 

@api_view(['GET'])
def usuarios_departamento(request):
    perfil_usuario = getPerfilUsuario(request)
    
    if "Departamento" in perfil_usuario.actor.nombre:
        departamento_usuario = perfil_usuario.actor.nombre
    else:
        departamento_usuario = perfil_usuario.actor.dependencia.nombre
    usuarios_departamento = usuarios_mismo_departamento(departamento_usuario)
    return JsonResponse(usuarios_departamento, safe=False)

def obtener_rut_ucampus(consulta):
    persona = consultar_api_ucampus(api='personas', params={'q': consulta})
    return persona[0]["rut"]

@api_view(['GET'])
def mis_cursos(request):
    nombre = request.user.first_name
    apellido = request.user.last_name
    consulta = (nombre + " " + apellido).lower()    
    
    
    ## Uso exclusivo del plan de pruebas del módulo de planificación anual académica
    testing_planificacion = ['sebastian saez', 'christian vasquez','cesar vargas','cristian valdes']
    if consulta in testing_planificacion:
        consulta = "romina aranda"    
    ## Uso exclusivo del plan de pruebas del módulo de planificación anual académica


    #Se realiza consulta API ucampus para obtener RUT de la persona
    rut_persona = obtener_rut_ucampus(consulta)

    mis_cursos_api = []
    periodos = ["2023.1", "2023.2"]
    for periodo in periodos:
        cursos_periodo = consultar_api_ucampus(api='cursos_dictados', params={'rut': rut_persona, 'periodo': periodo})
        mis_cursos_api.extend(cursos_periodo)
    
    
    codigos_mis_cursos = [curso['codigo'] for curso in mis_cursos_api]
    mis_cursos = PAA_Asignatura.objects.filter(codigo__in=codigos_mis_cursos)    
    serializer = PAA_AsignaturaSerializer(mis_cursos, many=True)

    return Response(serializer.data)

class HitoViewSet(viewsets.ModelViewSet):
    queryset = Hito.objects.all()
    serializer_class = HitoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accion']

    #querySet tratamiento incidencia duplicidades POA2023
    def get_queryset(self):
        queryset = Hito.objects.all()
        accion_id = self.request.query_params.get('accion')
        if accion_id:
            accion = Accion.objects.get(id=accion_id)
            if accion.anio == 2022:
                queryset = queryset.filter(accion=accion)
            else:
                queryset = queryset.filter(Q(accion=accion) & Q(dirGoogle__isnull=False))
        return queryset

class FuncionViewSet(viewsets.ModelViewSet):
    queryset = Funcion.objects.all()
    serializer_class = FuncionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accion']

    #querySet tratamiento incidencia duplicidades POA2023
    def get_queryset(self):
        queryset = Funcion.objects.all()
        accion_id = self.request.query_params.get('accion')
        if accion_id:
            accion = Accion.objects.get(id=accion_id)
            if accion.anio == 2022:
                queryset = queryset.filter(accion=accion)
            else:
                queryset = queryset.filter(Q(accion=accion) & Q(dirGoogle__isnull=False))
        return queryset
        
class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['funcion']

    #querySet tratamiento incidencia duplicidades POA2023
    def get_queryset(self):
        queryset = Indicador.objects.all()
        funcion_id = self.request.query_params.get('funcion')
        if funcion_id:
            funcion = Funcion.objects.get(id=funcion_id)
            queryset = queryset.filter(Q(funcion=funcion) & Q(dirGoogle__isnull=False))
        return queryset
    
    @action(detail=False, methods=['get'])
    def metaPorFuncion(self, request):
        id_funcion = request.query_params['funcion']
        #total_metas = Indicador.objects.filter(funcion=id_funcion).annotate(as_float=Cast('meta', FloatField())).aggregate(valor=Sum('as_float'))        
        total_metas = Indicador.objects.filter(funcion__dirGoogle__isnull=False, dirGoogle__isnull=False, funcion=id_funcion).annotate(as_float=Cast('meta', FloatField())).aggregate(valor=Sum('as_float'))

        return JsonResponse({"datos" : 
            {
                "total_meta_funcion" : total_metas
            }})

class MDVViewSet(viewsets.ModelViewSet):
    queryset = MDV.objects.all()
    serializer_class = MDVSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['accion']

    @action(detail=False, methods=['get'])
    def mdvsProductosReporte (self, request):
        id_accion = request.query_params['accion']
        mdvs = MDV.objects.filter(accion__hito=id_accion, estado="Finalizado")
        
        verificadorSerializados = self.get_serializer(mdvs, many=True)
        return JsonResponse({"datos" : 
        {"reporte-hito" : verificadorSerializados.data,
            
        }})


class AccionViewSet(viewsets.ModelViewSet):
    queryset = Accion.objects.all()
    serializer_class = AccionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['objetivo', 'tipo', 'anio']

    @action(detail=False, methods=['get'])
    def estrategias(self, request):
        return JsonResponse({'series': Meta.objects.all().first().matrizAccionEstrategia})
    
    @action(detail=False, methods=['get'], url_path=r'anios_unicos/(?P<accion>[^/.]+)')
    def anios_unicos(self, request,accion, *args, **kwargs):
        anios = Accion.objects.order_by('anio').values_list('anio', flat=True).distinct()
        return JsonResponse({'periodo': list(anios)})
    
    @action(detail=False, methods=['get'], url_path=r'origen_unicos/(?P<accion>[^/.]+)')
    def origen_unicos(self, request,accion, *args, **kwargs):
        # origenes = Accion.objects.order_by('origen').values_list('origen', flat=True).distinct()
        # return JsonResponse({'origenes': list(origenes)})
        acciones = Accion.objects.order_by('origen').values_list('origen', 'proyecto','anio', 'id_uaysen')
        origenes = []
        for accion in acciones:
            if(accion[2] == 2022):
                if(accion[1]!= None):
                    origenes.append('URY')
                else:
                    origenes.append('TRANSVERSAL')
            else:
                origenes.append(accion[0])

        return JsonResponse({'origenes': list(set(origenes))})  

    @action(detail=False, methods=['get'], url_path=r'hitosyfunciones/(?P<accion>[^/.]+)')
    def hitosyfunciones(self, request, accion, *args, **kwargs) :
        accion = Accion.objects.get(id=accion)

        if accion.anio == 2022:
            #funciones = list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Funcion.objects.filter(accion__id=accion).values_list('id', 'nombre'))))
            funciones = list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Funcion.objects.filter(accion=accion).values_list('id', 'nombre'))))
            #hitos = list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion).values_list('id', 'nombre', 'descripcion', 'plazo'))))
            hitos = list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion=accion).values_list('id', 'nombre', 'descripcion', 'plazo'))))
        else:
            #funciones = list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Funcion.objects.filter(accion__id=accion,dirGoogle__isnull=False).values_list('id', 'nombre'))))
            funciones = list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Funcion.objects.filter(accion=accion,dirGoogle__isnull=False).values_list('id', 'nombre'))))
            #hitos = list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion,dirGoogle__isnull=False).values_list('id', 'nombre', 'descripcion', 'plazo'))))
            hitos = list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion=accion,dirGoogle__isnull=False).values_list('id', 'nombre', 'descripcion', 'plazo'))))

        #Manejo del plazo en los hitos para informarlos en Acciones Institucionales
        for hito in hitos:
            plazo = list(map(lambda x: {'anio':x[0], 'mes':x[1]}, list(Plazo.objects.filter(id=hito['plazo']).values_list('plazo_anio','plazo_mes'))))
            hito['plazo'] = plazo
        
        #return JsonResponse({ 'funciones' : list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Funcion.objects.filter(accion__id=accion).values_list('id', 'nombre')))) , 'hitos' : list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion).values_list('id', 'nombre', 'descripcion', 'plazo')))) })
        return JsonResponse({
            'funciones' : funciones,
            'hitos' : hitos
        })
    
    @action(detail=False, methods=['get'], url_path=r'mdvsFuncionesEhitos/(?P<accion>[^/.]+)')
    def mdvsFuncionesEhitos(self, request, accion, *args, **kwargs) :
        mdvs = list(map(lambda x: {'value':x[0], 'label':x[1]}, list(MDV.objects.filter(accion__id=accion).values_list('id','nombre'))))        

        accion_obj = Accion.objects.get(id=accion)
    
        if accion_obj.anio == 2022:
            hitos = list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion).values_list('id', 'nombre', 'descripcion', 'plazo'))))
            for hito in hitos:
                plazo = list(map(lambda x: {'anio':x[0], 'mes':x[1]}, list(Plazo.objects.filter(id=hito['plazo']).values_list('plazo_anio','plazo_mes'))))
                hito['plazo'] = plazo
        else:
            hitos = list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion,dirGoogle__isnull=False).values_list('id', 'nombre', 'descripcion', 'plazo'))))
            mdvs = list(map(lambda x: {'value':x[0], 'label':x[1]}, list(Hito.objects.filter(accion__id=accion,dirGoogle__isnull=False).values_list('id','descripcion'))))
            
            for hito in hitos:
                plazo = list(map(lambda x: {'anio':x[0], 'mes':x[1]}, list(Plazo.objects.filter(id=hito['plazo']).values_list('plazo_anio','plazo_mes'))))
                hito['plazo'] = plazo

        return JsonResponse({
            'mdvs' : mdvs,
            'hitos' : hitos
        })
        #return JsonResponse({'hitos' : list(map(lambda x: {'value':x[0], 'label':x[1], 'descripcion':x[2], 'plazo':x[3]}, list(Hito.objects.filter(accion__id=accion).values_list('id', 'nombre', 'descripcion', 'plazo')))) ,'mdvs' : list(map(lambda x: {'value':x[0], 'label':x[1]}, list(MDV.objects.filter(accion__id=accion).values_list('id','nombre'))))})

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all().order_by('-nombre')
    serializer_class = ActorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=['get'])
    def getActores(self, request):  
        actores = Actor.objects.all().order_by('nombre')
        actoresSerializados = self.get_serializer(actores, many=True)
        return JsonResponse({'datos': actoresSerializados.data})

    def getActoresPanel (self, request):
        actores = Actor.objects.filter(id__in=request)
        actoresSerializados = self.get_serializer(actores, many=True)
        return JsonResponse({"datos" : 
            {
                "detalleActores" : actoresSerializados.data,
            }
        })
    
    @action(detail=False, methods=['get'])
    def getDependencias(self, request):  
        actores = Actor.objects.filter(dependencia__dependencia__isnull=True).exclude(categoria='todos').order_by('-nombre')
        #actores = Actor.objects.filter(dependencia__isnull=True).order_by('-nombre')
        actoresSerializados = self.get_serializer(actores, many=True)
        return JsonResponse({'datos': ["Todos"] + actoresSerializados.data})
    
    @action(detail=False, methods=['get'])
    def getDireccion(self, request):
        dependencia = request.query_params['dependencia']
        actores = Actor.objects.filter(dependencia=dependencia).order_by('-nombre').exclude(es_direccion=True)
        actoresSerializados = self.get_serializer(actores, many=True)
        return JsonResponse({'datos': ["Todos"] + actoresSerializados.data})

    @action(detail=False, methods=['get'])
    def getDirecciones(self, request):
        actores = Actor.objects.filter(es_direccion=True)
        actoresSerializados = self.get_serializer(actores, many=True)
        
        return JsonResponse({'datos': ["Todos"] + actoresSerializados.data})
    
    @action(detail=False, methods=['get'])
    def getUnidades(self, request):
        actores = Actor.objects.filter(es_direccion=False)
        actoresSerializados = self.get_serializer(actores, many=True)
        
        return JsonResponse({'datos': ["Todos"] + actoresSerializados.data})

class VerificadorViewSet(viewsets.ModelViewSet):
    queryset = Verificador.objects.all().order_by('-id')
    serializer_class = VerificadorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario']

class VerificadorDepthViewSet(viewsets.ModelViewSet):
    queryset = Verificador.objects.all().order_by('-id')
    serializer_class = VerificadorDepthSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'estado', 'indicador','valor']

    def getVerificadoresUnidad(self, sinMi, request) :
        perfilUsuario = getPerfilUsuario(request)    
        verificadores = Verificador.objects.distinct().exclude(usuario=request.user).\
            filter(indicador__funcion__accion__rol__actor=perfilUsuario.actor) \
            if sinMi else \
            Verificador.objects.distinct().filter(indicador__funcion__accion__rol__actor=perfilUsuario.actor, usuario=request.user)
        
        verificadores_borrador = verificadores.filter(estado="Borrador")
        verificadores_enviado_Lider = verificadores.filter(estado="Enviado al líder")
        verificadores_enviado_UPCI = verificadores.filter(estado="Enviado a UPCI")
        verificadores_finalizado = verificadores.filter(estado="Finalizado")
        verificadores_rechazado_lider = verificadores.filter(estado="Rechazado por líder")
        verificadores_rechazado_UPCI = verificadores.filter(estado="Rechazado por UPCI")
        serializer_borrador = self.get_serializer(verificadores_borrador, many=True)
        serializer_enviado_Lider = self.get_serializer(verificadores_enviado_Lider, many=True)
        serializer_enviado_UPCI = self.get_serializer(verificadores_enviado_UPCI, many=True)
        serializer_finalizado = self.get_serializer(verificadores_finalizado, many=True)
        serializer_rechazo_lider = self.get_serializer(verificadores_rechazado_lider, many=True)
        serializer_rechazo_UPCI = self.get_serializer(verificadores_rechazado_UPCI, many=True)
        data = {
                "borradores" : serializer_borrador.data,
                "enviados_Lider" : serializer_enviado_Lider.data,
                "enviados_UPCI" : serializer_enviado_UPCI.data,
                "rechazados_Lider" : serializer_rechazo_lider.data,
                "rechazados_UPCI" : serializer_rechazo_UPCI.data,
                "finalizados" : serializer_finalizado.data
                }
        # Crear el diccionario personalizado con la información requerida
        # data = {
        #     "borradores": VerificadorDepthSerializer(verificadores_borrador, many=True).data,
        #     "enviados_Lider": VerificadorDepthSerializer(verificadores_enviado_Lider, many=True).data,
        #     "enviados_UPCI": VerificadorDepthSerializer(verificadores_enviado_UPCI, many=True).data,
        #     "rechazados_Lider": VerificadorDepthSerializer(verificadores_rechazado_lider, many=True).data,
        #     "rechazados_UPCI": VerificadorDepthSerializer(verificadores_rechazado_UPCI, many=True).data,
        #     "finalizados": VerificadorDepthSerializer(verificadores_finalizado, many=True).data,
        # }

        for key in data.keys():
            verificadores = data[key]
            for verificador in verificadores:
                perfiles = User.objects.filter(email=verificador['usuario']['email']).first().perfilusuario_set.all()
                accion = verificador['indicador']['funcion']['accion']['id']                                
                rol = self.getRolUsuario(accion, perfiles[0].actor)
                verificador['rol'] = rol
        
        return {"datos": data}
        # for verificador in verificadores:
        #     print("Accion? ", verificador.indicador.funcion.accion)
        #     perfiles = User.objects.filter(email=verificador.usuario.email).first().perfilusuario_set.all()
        #     print("PERFIL ? ", perfiles[0].actor)
        #     rol = Rol.objects.filter(accion=verificador.indicador.funcion.accion, actor=perfiles[0].actor)
        #     print("rol ", rol);            
        #     print("cantidad roles ", len(rol))
        #     print("Usuario ? ", verificador.usuario)

        #     data["roles"] = [{            
        #         "tipo": rol[0].tipo,
        #         "actor": perfiles[0].actor.nombre,  # Ajusta el nombre del campo de acuerdo a tu modelo Actor
        #     }]
        # Agregar información del rol al diccionario
        # data["roles"] = [
        #     {
        #         "tipo": verificador.indicador.funcion.accion__rol.tipo,
        #         "actor": verificador.indicador.funcion.accion__rol.actor.nombre,  # Ajusta el nombre del campo de acuerdo a tu modelo Actor
        #     }
        #     for verificador in verificadores
        # ]        
    
    @action(detail=False, methods=['get'])
    def verificadoresUnidadSinMi(self, request):
        return JsonResponse(self.getVerificadoresUnidad(True, request))

    @action(detail=False, methods=['get'])
    def misVerificadores(self, request):
        return JsonResponse(self.getVerificadoresUnidad(False, request))

    @action(detail=False, methods=['get'])
    def verificadorPorIndicador(self, request):
        id_indicador = request.query_params['indicador']
        verificadoresPorIndicador = Verificador.objects.filter(indicador=id_indicador, estado="Finalizado")
        total_avances= Verificador.objects.filter(indicador=id_indicador, estado="Finalizado").annotate(as_float=Cast('valor', FloatField())).aggregate(valor=Sum('as_float'))
        verificadorSerializados = self.get_serializer(verificadoresPorIndicador, many=True)
        return JsonResponse({"datos" : 
            {"verificadores" : verificadorSerializados.data,
            "total_avances" : total_avances
            }})
    
    def getRolUsuario(self, accion, actor):
        rol_viewset = RolViewSet()
        # Llamar a la función getRolUsuario en RolViewSet
        resultado = rol_viewset.getRolUsuario(accion, actor)  
        return resultado

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('-id')
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'mdv', 'estado']

class ProductoDepthViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('-id')
    serializer_class = ProductoDepthSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'mdv', 'estado']

    def getProductosUnidad(self, sinMi, request) :
        perfilUsuario = getPerfilUsuario(request)
        #filter(mdv__accion__rol__actor=perfilUsuario.actor) \
        productos = Producto.objects.distinct().exclude(usuario=request.user).\
            filter(Q(mdv__isnull = False, mdv__accion__rol__actor=perfilUsuario.actor) | \
            Q(mdv__isnull = True, hitos__accion__rol__actor=perfilUsuario.actor)) \
            if sinMi else \
            Producto.objects.distinct().filter(Q(mdv__isnull = False, mdv__accion__rol__actor=perfilUsuario.actor) | Q(mdv__isnull = True, hitos__accion__rol__actor=perfilUsuario.actor), usuario=request.user)
            #Producto.objects.distinct().filter(mdv__accion__rol__actor=perfilUsuario.actor, usuario=request.user)


        
        productos_borrador = productos.filter(estado="Borrador")
        productos_enviado_Lider = productos.filter(estado="Enviado al líder")
        productos_enviado_UPCI = productos.filter(estado="Enviado a UPCI")
        productos_rechazado_lider = productos.filter(estado="Rechazado por líder")
        productos_rechazado_UPCI = productos.filter(estado="Rechazado por UPCI")
        productos_finalizado = productos.filter(estado="Finalizado")
        serializer_borrador = self.get_serializer(productos_borrador, many=True)
        serializer_enviado_Lider = self.get_serializer(productos_enviado_Lider, many=True)
        serializer_enviado_UPCI = self.get_serializer(productos_enviado_UPCI, many=True)
        serializer_rechazo_lider = self.get_serializer(productos_rechazado_lider, many=True)
        serializer_rechazo_UPCI = self.get_serializer(productos_rechazado_UPCI, many=True)
        serializer_finalizado = self.get_serializer(productos_finalizado, many=True)
        datos = {
                "borradores" : serializer_borrador.data,
                "enviados_Lider" : serializer_enviado_Lider.data,
                "enviados_UPCI" : serializer_enviado_UPCI.data,
                "rechazados_Lider" : serializer_rechazo_lider.data,
                "rechazados_UPCI" : serializer_rechazo_UPCI.data,
                "finalizados" : serializer_finalizado.data}
        
        for key in datos.keys():
            productos = datos[key]
            for producto in productos:
                perfiles = User.objects.filter(email=producto['usuario']['email']).first().perfilusuario_set.all()

                if producto['mdv'] is None:
                    accion = producto['hitos'][0]['accion']['id']
                else:
                    accion = producto['mdv']['accion']['id']                    
                rol = self.getRolUsuario(accion, perfiles[0].actor)
                producto['rol'] = rol
                # accion = producto['indicador']['funcion']['accion']['id']
                # rol = self.getRolUsuario(accion, perfiles[0].actor)
                # producto['rol'] = rol
        # return {"datos" : {"borradores" : serializer_borrador.data,
        #                     "enviados_Lider" : serializer_enviado_Lider.data,
        #                     "enviados_UPCI" : serializer_enviado_UPCI.data,
        #                     "rechazados_Lider" : serializer_rechazo_lider.data,
        #                     "rechazados_UPCI" : serializer_rechazo_UPCI.data,
        #                     "finalizados" : serializer_finalizado.data}}
        return {"datos": datos}
    def getTodosProductosUnidad(self, request) :
        productos = Producto.objects.filter(actor=request.actor)
        productos_unidad_serializados = self.get_serializer(productos, many=True)
        return JsonResponse({"datos" : 
            {"productos" : productos_unidad_serializados.data }})
    
    def getRolUsuario(self, accion, actor):
        rol_viewset = RolViewSet()
        # Llamar a la función getRolUsuario en RolViewSet
        resultado = rol_viewset.getRolUsuario(accion, actor)  
        return resultado

    @action(detail=False, methods=['get'])
    def productosUnidadSinMi(self, request):
        return JsonResponse(self.getProductosUnidad(True, request))

    @action(detail=False, methods=['get'])
    def misProductos(self, request):
        return JsonResponse(self.getProductosUnidad(False, request))

    @action(detail=False, methods=['get'])
    def productosUnidad(self, request):
        return JsonResponse(self.getTodosProductosUnidad(False, request))

    @action(detail=False, methods=['get'])
    def hitosReporte (self, request):
        id_accion = request.query_params['accion']
        anio_accion = Accion.objects.get(id=id_accion).anio

        if anio_accion == 2022:
            query = Q(mdv__accion=id_accion, estado="Finalizado")
            mdv_list = list(map(lambda x: {'value': x[0], 'hitos': x[1]},list(Producto.objects.filter(query).values_list('mdv', 'hitos'))))
        elif anio_accion == 2023:
            query = Q(hitos__accion=id_accion, estado="Finalizado")
            mdv_list = list(map(lambda x: {'value': x[0], 'hitos': x[1]},list(Producto.objects.filter(query).values_list('hitos', 'hitos'))))
        else:
            mdv_list = []

        return JsonResponse({'mdv': mdv_list})

        #return JsonResponse({'mdv': mdv_list})
        # id_accion = request.query_params['accion']
        # return JsonResponse({
        #     'mdv' : list(map(lambda x: {'value':x[0], 'hitos':x[1]}, list(Producto.objects.filter(mdv__accion=id_accion,estado="Finalizado").values_list('mdv','hitos'))))
        #     })

class RetroEntregaViewSet(viewsets.ModelViewSet):
    queryset = RetroEntrega.objects.all().order_by('-modificado')
    serializer_class = RetroEntregaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'producto', 'verificador']

    @action(detail=False, methods=['get'])
    def misRetroalimentaciones(self, request):
        misRetrosProductos = RetroEntrega.objects.filter(producto__usuario=request.user)    
        misRetrosVerificadores = RetroEntrega.objects.filter(verificador__usuario=request.user)
        retroProductosSerializados = self.get_serializer(misRetrosProductos, many=True)
        retroVerificadoresSerializados = self.get_serializer(misRetrosVerificadores, many=True)
        
        for retroVerificador, retroVerificadorSerializado in zip(misRetrosVerificadores,retroVerificadoresSerializados.data):
            retroVerificadorSerializado['accion'] = retroVerificador.verificador.indicador.funcion.accion.id_uaysen

        for retroProducto, retroProductoSerializado in zip(misRetrosProductos, retroProductosSerializados.data):
            retroProductoSerializado['accion'] = retroProducto.producto.mdv.accion.id_uaysen if (retroProducto.producto.mdv and retroProducto.producto.mdv.accion) else retroProducto.producto.hitos.first().accion.id_uaysen
            #retroProductoSerializado['accion'] = retroProducto.producto.mdv.accion.id_uaysen

        return JsonResponse({'datos' : 
            {
            'productos' :  retroProductosSerializados.data,
            'verificadores' :  retroVerificadoresSerializados.data
            }
        })

class ReportesViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor','id']
    http_method_names = ['patch','post','get']

    @action(detail=False, methods=['get','post'])
    def misReportes (self, request):
        reportes_por_tipo = defaultdict(list)

        misReportes = Reporte.objects.filter(estado="Borrador", usuario=request.user).exclude(tipo="PMI")
        misReportesPMI = Reporte.objects.filter(estado="Borrador", usuario=request.user, tipo="PMI")
        
        for reporte in misReportes:
            reportes_por_tipo[reporte.tipo].append(reporte)
        
        reportes_serializados = {}
        for tipo, reportes in reportes_por_tipo.items():
            reportes_serializados[tipo] = self.get_serializer(reportes, many=True).data
        
        #reportesSerializados = self.get_serializer(misReportes, many=True)
        reportesSerializadosPMI = self.get_serializer(misReportesPMI, many=True)

        return JsonResponse({'datos' : 
            {
            'borradores' :  reportes_serializados,
            'borradoresPMI' :  reportesSerializadosPMI.data,
            }
        })

    @action(detail=False, methods=['get'])
    def reportesUpci (self, request):
        reportes_por_tipo = defaultdict(list)

        reportesUpci = Reporte.objects.filter(estado="Finalizado").exclude(tipo="PMI")
        reportesUpciPMI = Reporte.objects.filter(estado="Finalizado", tipo="PMI")

        for reporte in reportesUpci:
            reportes_por_tipo[reporte.tipo].append(reporte)
        
        reportes_serializados = {}
        for tipo, reportes in reportes_por_tipo.items():
            reportes_serializados[tipo] = self.get_serializer(reportes, many=True).data

        #reportesSerializados = self.get_serializer(reportesUpci, many=True)
        reportesSerializadosPMI = self.get_serializer(reportesUpciPMI, many=True)

        return JsonResponse({'datos' : 
            {
            'finalizados' :  reportes_serializados,
            'finalizadosPMI' :  reportesSerializadosPMI.data
            }
        })
    
    def delete(self, request,id_reporte):
        reporte = Reporte.objects.filter(id="id_reporte")
        reporte.delete()
        return Response({"eliminado_id" : id_reporte})

    def reportePdf(self, request, *args, **kwargs):
        model = Reporte
        template_name = "webapp/reporte_UPCI.html"
        context_object_name = 'reportes'
#Pruebas para el envio de reporte pdf generado via email
class ReporteUpciPDFViewSet4 (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request):        
        lista_id = [137,138,141]
        reportes = Reporte.objects.filter(id=138)#49
        reportesUnificar = Reporte.objects.filter(id__in=lista_id)
        format_time = "%d-%m-%Y"

        # Establecer la configuración local en español
        locale.setlocale(locale.LC_TIME, 'es_ES')

        # Obtener la fecha actual con el formato deseado
        fecha_actual = datetime.now().strftime('%B %Y').capitalize()

        actor = Reporte.objects.get(id=116)
        data = {
            'reportes': reportes,
            'reportesUnificar': reportesUnificar,
            'fecha_actual' : fecha_actual,
        }        
        template_name = "webapp/reporte_UPCI_Unificado.html"
        #template_name = "webapp/reporte_UPCI_PMI.html"
        pdf = render_to_pdf (template_name, data)
        file_name = 'Reporte_%s_%s.pdf' %(actor.actor.sigla, actor.modificado.strftime(format_time))
        #return render(request, template_name, data)
        
        # modificado
        # return  HttpResponse(pdf, content_type='application/pdf')        

        #response['Content-Disposition'] = 'inline; filename=' + file_name
        #return response
        contexto = {
            "nombre_usuario" : "Seba",
            "tipo_entrega" : "verificador",
        }
        # envío de correo al colaborador que subió la entrega
        #html_content = loader.render_to_string("webapp/correo_Finalizado_colaborador.html", contexto)
        
        subject = "Prueba envio adjunto Reporte"
        body = "Entrega reporte enviado"
        from_email = "colabora@uaysen.cl"
        recipient_list = ['sebastiansaezmansilla@gmail.com']

        #Open PDF file in binary mode
        #with open(pdf, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        #    part = MIMEBase("application", "octet-stream")
        #    part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        #encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        #part.add_header("Content-Disposition", f"attachment; filename= {file_name}",)
        part = (file_name, pdf, 'application/pdf')
        #async_send_mail(subject=subject, body=body, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html=html_content, adjunto=pdf)
        return  HttpResponse(pdf, content_type='application/pdf')
        

class ReporteUpciPDFViewSet (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request, id_reporte):        
        reportes = Reporte.objects.filter(id=id_reporte)#49
        actor = Reporte.objects.get(id=id_reporte)
        format_time = "%d-%m-%Y"
        fecha = actor.modificado.strftime(format_time)
        data = {
            'reportes': reportes,
        }
        template_name = "webapp/reporte_UPCI.html"
        pdf = render_to_pdf (template_name, data)
        file_name = 'Reporte_%s_%s.pdf' %(actor.actor.sigla, fecha)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + file_name
        return response
    
#clase que recibe una lista de ID correspondiente a una lista de reportes a Unificar.
class ReporteUpciPDFUnificadoViewSet (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    def get(self, request):        
        id_reportes = [value for key, value in self.request.GET.items() if key.startswith('id_reporte[')]
    
        reportesUnificar = Reporte.objects.filter(id__in=id_reportes)
        # Establecer la configuración local en español
        locale.setlocale(locale.LC_TIME, 'es_ES')

        # Obtener la fecha actual con el formato deseado
        fecha_actual = datetime.now().strftime('%B %Y').capitalize()
        analistaUpci = '{} {}'.format(request.user.first_name, request.user.last_name)
        data = {            
            'reportesUnificar': reportesUnificar,
            'fecha_actual' : fecha_actual,
            'analistaUpci' : analistaUpci,
        }
        template_name = "webapp/reporte_UPCI_Unificado.html"
        pdf = render_to_pdf (template_name, data)
        file_name = 'Reporte_%s_%s.pdf'
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + file_name
        return response
    
class ReporteUpciPDFUnificadoUnidadViewSet (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request, id_reporte):                       
        reportes = Reporte.objects.filter(id=id_reporte)#49
        actor = Reporte.objects.get(id=id_reporte)
        analistaUpci = '{} {}'.format(request.user.first_name, request.user.last_name)
        format_time = "%d-%m-%Y"
        fecha = actor.modificado.strftime(format_time)
        data = {
            'reportes': reportes,
            'analistaUpci' : analistaUpci
        }
        template_name = "webapp/reporte_UPCI_UnidadUnificado.html"
        pdf = render_to_pdf (template_name, data)
        file_name = 'Reporte_%s_%s.pdf' %(actor.actor.sigla, fecha)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + file_name
        return response

class ReporteUpciPmiPDFViewSet (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request, id_reporte):        
        reportes = Reporte.objects.filter(id=id_reporte)#49
        actor = Reporte.objects.get(id=id_reporte)
        format_time = "%d-%m-%Y"
        fecha = actor.modificado.strftime(format_time)
        data = {
            'reportes': reportes,
        }
        template_name = "webapp/reporte_UPCI_PMI.html"
        pdf = render_to_pdf (template_name, data)
        file_name = 'Reporte_PMI_%s_%s.pdf' %(actor.actor.sigla, fecha)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + file_name
        return response

class ReporteUpciPmiPDFViewSet4 (ListView):
    queryset = Reporte.objects.all().order_by('-modificado')
    serializer_class = ReporteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'actor']
    
    @staticmethod
    def get(request):        
        reportes = Reporte.objects.filter(id=116)#49
        data = {
            'reportes': reportes,
        }        
        template_name = "webapp/reporte_UPCI_PMI.html"
        pdf = render_to_pdf (template_name, data)
        #file_name = 'Reporte_%s_%s.pdf' %(actor.actor.sigla, fecha)
        #return render(request, template_name, data)
        return  HttpResponse(pdf, content_type='application/pdf')
        #response['Content-Disposition'] = 'inline; filename=' + file_name
        #return response

class EditaVerificadorViewSet(viewsets.ModelViewSet):
    #queryset = Verificador.objects.all().filter(estado='Borrador')
    queryset = Verificador.objects.all().order_by('-modificado')
    serializer_class = VerificadorSerializer
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['patch', 'get']

    @action(detail=False, methods=['patch','get'])
    def verificadoresRechazados(self, request):
        datosRequest = request.data     
        verificador = Verificador.objects.filter(usuario=request.user)
        verificador = Verificador.objects 
        serializer = self.serializer_class(instance=verificador, data=datosRequest, partial = True)

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse({'verificadores_borradores' :
                {
                'verificadores' : serializer.data
                }
            })
        else:            
            return Response(serializer.errors)            

class EditaProductoViewSet (viewsets.ModelViewSet):
    #queryset = Producto.objects.all().filter(estado='Borrador')
    queryset = Producto.objects.all().order_by('-modificado')
    serializer_class = ProductoSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['patch', 'get']

    @action(detail=False, methods=['patch','get'])
    def ProductosRechazados(self, request):
        datosRequest = request.data     
        producto = Producto.objects 
        serializer = self.serializer_class(instance=producto, data=datosRequest, partial = True)

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse({'productos_borradores' :
                {
                'productos' : serializer.data
                }
            })
        else:
            return Response(serializer.errors) 

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all().order_by('-id')
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo','actor','accion']

    @action(detail=False, methods=['get'], url_path=r'rolPorRol/(?P<tipo>[^/.]+)/(?P<origen>[^/.]+)')
    def rolPorRol(self, request, tipo, origen='POA', *args, **kwargs):
        perfilUsuario = getPerfilUsuario(request)
        accionesPorRol = {}                        
        
        roles = Rol.objects.filter(actor__in=validaDependencia(perfilUsuario.actor), tipo=tipo).order_by('accion__origen','accion__id_uaysen', 'accion__anio')
        serializer = self.get_serializer(roles, many=True)        
        accionesPorRol = getAccionesPorRol(serializer)    
        return Response(accionesPorRol)
    
    @action(detail=False, methods=['get'], url_path=r'rolResponsable/(?P<id_actor>[^/.]+)')
    def rolResponsable(self, request, id_actor, *args, **kwargs):              
        if id_actor != "0":
            roles = Rol.objects.filter(actor=id_actor, tipo ="Responsable", accion__origen="POA").order_by('accion__id')
        else:
            roles = Rol.objects.filter(tipo ="Responsable", accion__origen="POA")
            
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)
    
    
    # @action(detail=False, methods=['get'], url_path=r'rolResponsableUnificado/id_actor=(?P<id_actor>[^/.]+)&anio=(?P<anio>[^/.]+)')
    # def rolResponsableUnificado(self, request, id_actor,anio,*args, **kwargs):              
    #     if id_actor != "0":
    #         roles = Rol.objects.filter(actor=id_actor, tipo="Responsable", accion__anio=anio).order_by('accion__id')        
            
    #     serializer = self.get_serializer(roles, many=True)
    #     return Response(serializer.data)
    @action(detail=False, methods=['get'], url_path=r'rolResponsableUnificado/id_actor=(?P<id_actor>[^/.]+)&anio=(?P<anio>[^/.]+)')
    def rolResponsableUnificado(self, request, id_actor, anio, *args, **kwargs):              
        if id_actor != "0":
            roles = Rol.objects.filter(actor=id_actor, tipo="Responsable")
            if anio != "0":
                roles = roles.filter(accion__anio=anio)
            roles = roles.order_by('accion__id')
    
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path=r'rolResponsablePMI/(?P<id_actor>[^/.]+)')
    def rolResponsablePMI(self, request, id_actor, *args, **kwargs):
        if id_actor != "0":
            roles = Rol.objects.filter(actor=id_actor, tipo ="Responsable", accion__origen="PMI")
        else:
            roles = Rol.objects.filter(tipo ="Responsable", accion__origen="PMI")
            
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data)
        
    def getRolUsuario(self,accion, actor):        
        rol = Rol.objects.filter(actor=actor, accion__id=accion).first();
        rolSerializado = self.serializer_class(rol)                
        return rolSerializado.data
        # reportes = Reporte.objects.filter(id=id_reporte)#49
        # actor = Reporte.objects.get(id=id_reporte)
        # analistaUpci = '{} {}'.format(request.user.first_name, request.user.last_name)
        # format_time = "%d-%m-%Y"
        # fecha = actor.modificado.strftime(format_time)
        # data = {
        #     'reportes': reportes,
        #     'analistaUpci' : analistaUpci
        # }
        # template_name = "webapp/reporte_UPCI_UnidadUnificado.html"
        # pdf = render_to_pdf (template_name, data)
        # file_name = 'Reporte_%s_%s.pdf' %(actor.actor.sigla, fecha)
        # response = HttpResponse(pdf, content_type='application/pdf')
        # response['Content-Disposition'] = 'inline; filename=' + file_name
        #return response

class EstrategiaViewSet(viewsets.ModelViewSet):
    queryset = Estrategia.objects.all()
    serializer_class = EstrategiasSimpleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['periodo']
    http_method_names = ['get']
    
class DimensionViewSet(viewsets.ModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']
    http_method_names = ['get']

#########################################################
# Sección BACKEND workflow de las entregas (entregables)
#########################################################
@api_view(['POST'])
def entregableEnviaALider(request):
    '''
    evento del workflow donde un colaborador envía una entrega
    a su encargado de unidad (líder). Consideraciones (a validar):
     - la entrega debiese estar en estado "borrador"
     - la entrega es de tipo verificador o producto
     - solo el colaborador puede enviar al líder sus propias entregas
    probablemente, sea una tarea previamente rechazada
    '''
    datosRequest = request.data

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        if verificador.usuario.id != request.user.id :
            raise PermissionDenied()
        verificador.envia_a_lider()
        verificador.save()
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        if producto.usuario.id != request.user.id :
            raise PermissionDenied()
        producto.envia_a_lider()
        producto.save()
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableLiderDaVistoBueno(request) :
    '''
    evento del workflow donde un(a) líder de unidad da el visto
    bueno para que la entrega sea revisada por UPCI.
    Consideraciones (a validar):
     - la entrega debiese estar en estado "enviado al lider"
     - la entrega es de tipo verificador o producto
     - solo el **encargado de la unidad responsable** de la entrega
     tiene permitido dar este visto bueno
    '''
    datosRequest = request.data
    perfilUsuario = getPerfilUsuario(request)

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        # TODO: condicion incompleta, debe ser encargado de la
        # unidad responsable de la accion de la entrega
        if not perfilUsuario.es_encargado :
            raise PermissionDenied()
        verificador.envia_a_UPCI()
        verificador.save()
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        # TODO: condicion incompleta, debe ser encargado de la
        # unidad responsable de la accion de la entrega
        if not perfilUsuario.es_encargado :
            raise PermissionDenied()
        producto.envia_a_UPCI()
        producto.save()
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableUPCIDaVistoBueno(request) :
    '''
    evento del workflow donde un(a) líder de unidad da el visto
    bueno para que la entrega sea revisada por UPCI.
    Consideraciones (a validar):
     - la entrega debiese estar en estado "enviado al lider"
     - la entrega es de tipo verificador o producto
     - solo el **encargado de la unidad responsable** de la entrega
     tiene permitido dar este visto bueno
    '''
    datosRequest = request.data
    perfilUsuario = getPerfilUsuario(request)

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        if not perfilUsuario.es_analistaUPCI :
            raise PermissionDenied()
        verificador.acepta_UPCI()
        verificador.save()
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        if not perfilUsuario.es_analistaUPCI :
            raise PermissionDenied()
        producto.acepta_UPCI()
        producto.save()
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableLiderRechaza(request) :
    '''
    evento del workflow donde un(a) líder de unidad rechaza
    y da feedback de la entrega
    '''
    datosRequest = request.data
    perfilUsuario = getPerfilUsuario(request)

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        # TODO: condicion incompleta, debe ser encargado de la
        # unidad responsable de la accion de la entrega
        if not perfilUsuario.es_encargado :
            raise PermissionDenied()
        verificador.rechaza_lider(datosRequest['retroalimentacion'])
        verificador.save()
        RetroEntrega.objects.create(
            usuario=request.user,
            verificador=verificador,
            retroalimentacion=datosRequest['retroalimentacion']
        )
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        # TODO: condicion incompleta, debe ser encargado de la
        # unidad responsable de la accion de la entrega
        if not perfilUsuario.es_encargado :
            raise PermissionDenied()
        producto.rechaza_lider(datosRequest['retroalimentacion'])
        producto.save()
        RetroEntrega.objects.create(
            usuario=request.user,
            producto=producto,
            retroalimentacion=datosRequest['retroalimentacion']
        )
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableUPCIRechaza(request) :
    '''
    evento del workflow donde UPCI rechaza y da retroalimentación
    de la entrega
    '''
    datosRequest = request.data
    perfilUsuario = getPerfilUsuario(request)

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        if not perfilUsuario.es_analistaUPCI :
            raise PermissionDenied()
        verificador.rechazado_UPCI(datosRequest['retroalimentacion'])
        verificador.save()
        RetroEntrega.objects.create(
            usuario=request.user,
            verificador=verificador,
            retroalimentacion=datosRequest['retroalimentacion']
        )
        serializer = VerificadorDepthSerializer(verificador)
        return Response(serializer.data)

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        if not perfilUsuario.es_analistaUPCI :
            raise PermissionDenied()
        producto.rechazado_UPCI(datosRequest['retroalimentacion'])
        producto.save()
        RetroEntrega.objects.create(
            usuario=request.user,
            producto=producto,
            retroalimentacion=datosRequest['retroalimentacion']
        )
        serializer = ProductoDepthSerializer(producto)
        return Response(serializer.data)
        
    else :
        raise PermissionDenied()

@api_view(['POST'])
def entregableDescarta(request) :
    '''
    evento del workflow donde un(a) líder de unidad da el visto
    bueno para que la entrega sea revisada por UPCI.
    Consideraciones (a validar):
     - la entrega debiese estar en estado "enviado al lider"
     - la entrega es de tipo verificador o producto
     - solo el **encargado de la unidad responsable** de la entrega
     tiene permitido dar este visto bueno
    '''
    datosRequest = request.data

    if datosRequest['entrega_tipo'] == 'verificador' :
        verificador = get_object_or_404(Verificador, pk=datosRequest['entrega_id'])
        if verificador.usuario.id != request.user.id :
            raise PermissionDenied()
        verificador.delete()
        return Response({"eliminado_id" : datosRequest['entrega_id'], "eliminado_tipo" : datosRequest['entrega_tipo']})

    elif datosRequest['entrega_tipo'] == 'producto' :
        producto = get_object_or_404(Producto, pk=datosRequest['entrega_id'])
        if producto.usuario.id != request.user.id :
            raise PermissionDenied()
        producto.delete()
        return Response({"eliminado_id" : datosRequest['entrega_id'], "eliminado_tipo" : datosRequest['entrega_tipo']})
    else :
        raise PermissionDenied()
#########################################################
# FIN Sección BACKEND workflow de las entregas
#########################################################


#====================== Planificación Académica ======================
class PAA_AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = PAA_Asignatura.objects.all().order_by('-nombre')
    serializer_class = PAA_AsignaturaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'codigo','estado','departamento','modalidad']
    http_method_names = ['patch','post','get']

    @action(detail=False, methods=['get'], url_path=r'cursos_academicxs/(?P<nombre>[^/.]+)/(?P<apellido>[^/.]+)/(?P<anio>[^/.]+)')
    def cursos_academicxs(self, request, nombre, apellido, anio,*args, **kwargs):

        consulta = (nombre + " " + apellido).lower()    
        ## Uso exclusivo del plan de pruebas del módulo de planificación anual académica
        testing_planificacion = ['sebastian saez', 'christian vasquez','cesar vargas','cristian valdes']
        if consulta in testing_planificacion:
            consulta = "romina aranda"    
        ## Uso exclusivo del plan de pruebas del módulo de planificación anual académica

        rut_persona = obtener_rut_ucampus(consulta)

        mis_cursos_api = []
        periodos = [anio + ".1", anio + ".2"]
        for periodo in periodos:
            cursos_periodo = consultar_api_ucampus(api='cursos_dictados', params={'rut': rut_persona, 'periodo': periodo})
            mis_cursos_api.extend(cursos_periodo)
    
    
        codigos_mis_cursos = [curso['codigo'] for curso in mis_cursos_api]
        mis_cursos = self.queryset.filter(codigo__in=codigos_mis_cursos)

        serializer = PAA_AsignaturaSerializer(mis_cursos, many=True)

        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def asignaturas(self, request, *args, **kwargs):
        # Filtra las asignaturas por estado "Asignada" y "No asignada"
        asignaturas_asignadas = self.queryset.filter(estado="Asignada")
        asignaturas_no_asignadas = self.queryset.filter(estado="No asignado")

        response_data = {
            'datos': {
                'Asignada': PAA_AsignaturaSerializer(asignaturas_asignadas, many=True).data,
                'No asignado': PAA_AsignaturaSerializer(asignaturas_no_asignadas, many=True).data,
            }
        }
        return JsonResponse(response_data)
    
    @action(detail=False, methods=['get'], url_path=r'asignaturasDepartamento')
    def asignaturasDepartamento(self, request,*args, **kwargs):
        perfilUsuario = getPerfilUsuario(request)

        if "Departamento" in perfilUsuario.actor.nombre:
            departamento_usuario = perfilUsuario.actor.nombre
        else:
            departamento_usuario = perfilUsuario.actor.dependencia.nombre

        asignaturas = PAA_Asignatura.objects.all()
        data = {
            'asignaturas_dpto_usuario': {
                departamento_usuario: [],
            },
            'asignaturas_otro_dpto': {},
            'asignaturas_direccion': {},
        }

        # Mapeo de nombres de departamento de Ucampos a claves según actores en Colabora
        mapeo_departamentos = {
            "Ciencias de la Ingeniería y Ciencias Naturales": "Departamento de Ciencias Naturales y Tecnología",
            "Ciencias Sociales": "Departamento de Ciencias Sociales y Humanidades",
            "Área de Inglés": "Departamento de Ciencias Sociales y Humanidades",
            "Ciencias de la Salud": "Departamento de Ciencias de la Salud",
            "Dirección de Pregrado": "Dirección de Pregrado",
            "Dirección de Postgrado y Educación Continua": "Dirección de Postgrado y Educación Continua",
        }

        for asignatura in asignaturas:
            departamento = asignatura.departamento

            # Usar el mapeo para obtener la clave deseada
            clave_departamento = mapeo_departamentos.get(departamento, departamento)
            serializer = PAA_AsignaturaSerializer(asignatura)

            # Verificamos si el departamento es "Dirección" y agregamos las asignaturas a 'asignaturas_direccion'
            if "Dirección" in clave_departamento:
                data['asignaturas_direccion'].setdefault(clave_departamento, []).append(serializer.data)
            else:
                # Agregar la asignatura al departamento correspondiente
                if clave_departamento == departamento_usuario:
                    data['asignaturas_dpto_usuario'][departamento_usuario].append(serializer.data)
                elif clave_departamento not in data['asignaturas_otro_dpto']:
                    data['asignaturas_otro_dpto'][clave_departamento] = [serializer.data]
                else:
                    data['asignaturas_otro_dpto'][clave_departamento].append(serializer.data)

        # Serializar el diccionario en formato JSON
        return JsonResponse({'data': data})
    

class PAA_PlanificacionViewSet(viewsets.ModelViewSet):
    queryset = PAA_Planificacion.objects.all().order_by('-modificado')
    serializer_class = PAA_PlanificacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'estado','anio','accion']
    http_method_names = ['patch','post','get']

    def obtener_planificacion(self, planificacion):
        for data in planificacion:
            planificacion_docencia = data.get('planificaciones_docencia')
            if planificacion_docencia:
                for docencia in planificacion_docencia:
                    tipo = docencia.get('tipo')
                    if tipo != "OtraActividad":
                        asignatura = PAA_Asignatura.objects.get(id=docencia.get('asignatura'))
                        if asignatura:                                                
                            docencia['asignatura'] = PAA_AsignaturaSerializer(asignatura).data
        return planificacion
    
    def obtener_resumen(self, planificacion):
        total_horas_docencia = sumaHorasPlanificacion(planificacion.planificaciones_docencia.all(), 'cantidad_horas')
        total_horas_investigacion = sumaHorasPlanificacion(planificacion.planificaciones_investigacion.all(), 'cantidad_horas')
        total_horas_gestion = sumaHorasPlanificacion(planificacion.planificaciones_gestion.all(), 'cantidad_horas')
        total_horas_formacion = sumaHorasPlanificacion(planificacion.planificaciones_formacion.all(), 'cantidad_horas')
        total_horas_vinculacion = sumaHorasPlanificacion(planificacion.planificaciones_vinculacion.all(), 'cantidad_horas')

        suma_total = (
            total_horas_docencia +
            total_horas_investigacion +
            total_horas_gestion +
            total_horas_formacion +
            total_horas_vinculacion
        )

        return [
            {
                'actividad'     : "docencia",
                'total_horas'   : total_horas_docencia,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_docencia, suma_total) if total_horas_docencia > 0 else 0
            },
            {
                'actividad'     : "investigacion",
                'total_horas'   : total_horas_investigacion,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_investigacion,suma_total) if total_horas_investigacion > 0 else 0
            },
            {
                'actividad'     : "gestion",
                'total_horas'   : total_horas_gestion,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_gestion,suma_total) if total_horas_gestion > 0 else 0
            },
            {
                'actividad'     : "vinculacion",
                'total_horas'   : total_horas_vinculacion,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_vinculacion,suma_total) if total_horas_vinculacion > 0 else 0
            },
            {
                'actividad'     : "formacion",
                'total_horas'   : total_horas_formacion,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_formacion,suma_total) if total_horas_formacion > 0 else 0
            },            
            {
                'actividad'     : "total",
                'total_horas'   : suma_total,
                'porcentaje'    : 100
            },
        ]

    @action(detail=False, methods=['get'])
    def planificaciones(self, request, *args, **kwargs):
        estados_requeridos = [
            "Pendiente",
            "Aprobado_Jefe_Departamento",
            "Rechazado_Jefe_Departamento",
            "Aprobado_Direccion_Academica",
            "Rechazado_Direccion_Academica",
        ]
        
        planificaciones_filtradas = self.queryset.filter(estado__in=estados_requeridos).order_by('usuario', 'anio')

        response_data = {
            'datos': {
                estado: PAA_PlanificacionSerializer(
                    planificaciones_filtradas.filter(estado=estado), many=True
                ).data
                for estado in estados_requeridos
            }
        }
        return JsonResponse(response_data)
    
    @action(detail=False, methods=['get'], url_path=r'resumenActividadesAcademico/(?P<idPlanificacion>[^/.]+)')
    def resumenActividadesAcademico(self, request, idPlanificacion, *args, **kwargs):
        planificacion = get_object_or_404(PAA_Planificacion, pk=idPlanificacion)
        resumen = self.obtener_resumen(planificacion)
    
        return Response(resumen)


    @action(detail=False, methods=['get'], url_path=r'planificacionAcademicx/(?P<idPlanificacion>[^/.]+)')
    def planificacionAcademicx(self, request, idPlanificacion, *args, **kwargs):     
        planificaciones_filtradas = self.queryset.filter(id=idPlanificacion).order_by("anio")
        serialized_data = PAA_PlanificacionSerializer(planificaciones_filtradas, many=True).data

        for data in serialized_data:
            usuario = PAA_Planificacion.objects.get(id=idPlanificacion).usuario            
            data['usuario'] = {
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'nombre': usuario.first_name,
                'apellido': usuario.last_name,
            }
            planificacion_docencia = data.get('planificaciones_docencia')
            if planificacion_docencia:
                for docencia in planificacion_docencia:
                    tipo = docencia.get('tipo')
                    if tipo != "OtraActividad":
                        asignatura = PAA_Asignatura.objects.get(id=docencia.get('asignatura'))
                        if asignatura:                                                
                            docencia['asignatura'] = PAA_AsignaturaSerializer(asignatura).data

        response_data = {
                'planificacion' : serialized_data            
        }

        return JsonResponse(response_data)
    
    @action(detail=False, methods=['get'], url_path=r'misPlanificaciones/(?P<periodo>[^/.]+)')
    def misPlanificaciones(self, request, periodo, *args, **kwargs):        
        planificaciones_filtradas = self.queryset.filter(usuario=request.user, anio=periodo).order_by("anio")
        
        serialized_data = PAA_PlanificacionSerializer(planificaciones_filtradas, many=True).data        
        # Itera sobre el resultado y agrega la información de la asignatura
        for data in serialized_data:
            planificacion_docencia = data.get('planificaciones_docencia')
            if planificacion_docencia:
                for docencia in planificacion_docencia:
                    tipo = docencia.get('tipo')
                    if tipo != "OtraActividad":
                        asignatura = PAA_Asignatura.objects.get(id=docencia.get('asignatura'))
                        if asignatura:                                                
                            docencia['asignatura'] = PAA_AsignaturaSerializer(asignatura).data

        response_data = {
                'planificacion' : serialized_data            
        }

        return JsonResponse(response_data)        

    #@action(detail=False, methods=['get'], url_path=r'planificacionesDepartamento/(?P<periodo>[^/.]+)')
    @action(detail=False, methods=['get'], url_path=r'planificacionesDepartamento/(?P<periodo>[^/.]+)/(?P<opcion>[^/.]+)')
    def planificacionesDepartamento(self, request, periodo, opcion, *args, **kwargs):
        perfilUsuario = getPerfilUsuario(request)

        #Se obtiene Actor del usuario.
        if "Departamento" in perfilUsuario.actor.nombre:
            departamento_jefe = perfilUsuario.actor.nombre
        else:
            departamento_jefe = perfilUsuario.actor.dependencia.nombre
        
        # Se obtienen las planificaciones filtrando por el estado proporcionado en la URL como "opcion".
        ids_unicos = PAA_Planificacion.objects.filter(
            Q(usuario__perfilusuario__actor__nombre=departamento_jefe) | Q(usuario__perfilusuario__actor__dependencia__nombre=departamento_jefe),
            estado=opcion,
            anio=periodo
        ).values('id').distinct()

        #corrección en el uso de usuario multiperfil
        planificaciones = PAA_Planificacion.objects.filter(id__in=ids_unicos)

        # planificaciones = PAA_Planificacion.objects.filter(
        #     Q(usuario__perfilusuario__actor__nombre=departamento_jefe) | Q(usuario__perfilusuario__actor__dependencia__nombre=departamento_jefe),
        #     estado=opcion,
        #     anio=periodo
        # )

        planificaciones_con_usuario = []
        new_format = "%d/%m/%Y - %H:%M:%S"        
        
        for planificacion in planificaciones:            
            planificacion_con_usuario = {
                'id': planificacion.id,
                'usuario': {
                    'id': planificacion.usuario.id,
                    'username': planificacion.usuario.username,
                    'email': planificacion.usuario.email,
                    'fullname': planificacion.usuario.first_name + " " +planificacion.usuario.last_name,
                },
                'estado': planificacion.estado,
                'categoria': planificacion.categoria,
                'rut_academicx': planificacion.rut_academicx,
                'departamento': planificacion.departamento,
                #'fecha_ingreso': planificacion.fecha_ingreso.astimezone(timezone(TIME_ZONE)).strftime(new_format),
                'fecha_ingreso': planificacion.fecha_ingreso,
                'jornada': planificacion.jornada,
                'total_horas': planificacion.total_horas,
                'modificado': planificacion.modificado.astimezone(pytz.timezone(TIME_ZONE)).strftime(new_format),
                'creado': planificacion.creado.astimezone(pytz.timezone(TIME_ZONE)).strftime(new_format),
                'anio': planificacion.anio,
                # 'planificaciones_docencia'      : planificacion.planificaciones_docencia,
                # 'planificaciones_vinculacion'   : planificacion.planificaciones_vinculacion,
                # 'planificaciones_formacion'     : planificacion.planificaciones_formacion,
                # 'planificaciones_gestion'       : planificacion.planificaciones_gestion,
                # 'planificaciones_investigacion' : planificacion.planificaciones_investigacion,
                'accion': {
                    'id' : planificacion.accion.id if planificacion.accion else "no relacionada",
                    'id_uaysen': planificacion.accion.id_uaysen if planificacion.accion else "no relacionada",
                }
                
            }
            planificaciones_con_usuario.append(planificacion_con_usuario)

        response_data = {
            'datos': planificaciones_con_usuario,            
        }
        return JsonResponse(response_data)

    @action(detail=False, methods=['get'], url_path=r'resumenActividades/(?P<periodo>[^/.]+)')
    def resumenActividades(self, request, periodo, *args, **kwargs):        
        usuario = request.user        
        try:
            planificacion = PAA_Planificacion.objects.get(usuario=usuario, anio=periodo)
        except PAA_Planificacion.DoesNotExist:
            # Si no se encuentra la planificación, crear una nueva con usuario y año
            planificacion = PAA_Planificacion(usuario=usuario, anio=periodo, estado='Pendiente')
            planificacion.save()

        total_horas_docencia = sumaHorasPlanificacion(planificacion.planificaciones_docencia.all(), 'cantidad_horas')
        total_horas_investigacion = sumaHorasPlanificacion(planificacion.planificaciones_investigacion.all(), 'cantidad_horas')
        total_horas_gestion = sumaHorasPlanificacion(planificacion.planificaciones_gestion.all(), 'cantidad_horas')
        total_horas_formacion = sumaHorasPlanificacion(planificacion.planificaciones_formacion.all(), 'cantidad_horas')
        total_horas_vinculacion = sumaHorasPlanificacion(planificacion.planificaciones_vinculacion.all(), 'cantidad_horas')

        # Calcular la suma total de horas para el cálculo de porcentajes
        suma_total = (
            total_horas_docencia +
            total_horas_investigacion +
            total_horas_gestion +
            total_horas_formacion +
            total_horas_vinculacion
        )

        if suma_total > 0:
            planificacion.total_horas = suma_total
            planificacion.save()

        resumen = [
            {
                'actividad'     : "docencia",
                'total_horas'   : total_horas_docencia,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_docencia, suma_total) if total_horas_docencia > 0 else 0
            },
            {
                'actividad'     : "investigacion",
                'total_horas'   : total_horas_investigacion,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_investigacion,suma_total) if total_horas_investigacion > 0 else 0
            },
            {
                'actividad'     : "gestion",
                'total_horas'   : total_horas_gestion,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_gestion,suma_total) if total_horas_gestion > 0 else 0
            },
            {
                'actividad'     : "vinculacion",
                'total_horas'   : total_horas_vinculacion,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_vinculacion,suma_total) if total_horas_vinculacion > 0 else 0
            },
            {
                'actividad'     : "formacion",
                'total_horas'   : total_horas_formacion,
                'porcentaje'    : porcentajeHorasPlanificacion(total_horas_formacion,suma_total) if total_horas_formacion > 0 else 0
            },            
            {
                'actividad'     : "total",
                'total_horas'   : suma_total,
                'porcentaje'    : 100
            },
        ]

        return Response(resumen)

class PAA_ObservacionPlanificacionViewSet(viewsets.ModelViewSet):
    queryset = PAA_ObservacionPlanificacion.objects.all().order_by('-modificado')
    serializer_class = PAA_ObservacionPlanificacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['usuario', 'modificado']
    http_method_names = ['patch','post','get']

    @action(detail=False, methods=['get'], url_path=r'observacionesASubsanar/(?P<periodo>[^/.]+)')
    def observacionesASubsanar(self, request, periodo, *args, **kwargs): 
        # Filtra las observaciones enviadas a la planificación de un académico
        observaciones = self.queryset.filter(planificacion__usuario=request.user)

        observaciones_con_usuario = []  # Lista para almacenar observaciones con información del usuario

        for observacion in observaciones:
            observacion_con_usuario = {
                'id': observacion.id,
                'usuario': {
                    'id': observacion.usuario.id,
                    'username': observacion.usuario.username,
                    'email': observacion.usuario.email,
                },
                'planificacion': observacion.planificacion.id,
                'observacion': observacion.observacion,
                'modificado': observacion.modificado,
                'creado': observacion.creado
            }
            observaciones_con_usuario.append(observacion_con_usuario)

        response_data = {
            'datos': observaciones_con_usuario,            
        }
        return JsonResponse(response_data)
    
    @action(detail=False, methods=['get'])
    def misObservaciones(self, request, *args, **kwargs):
        # Filtra las observaciones creadas por un usuario (Jefe Departamento o Dirección Académica)
        observaciones = self.queryset.filter(usuario=request.user)        

        observaciones_con_usuario = []

        for observacion in observaciones:
            observacion_con_usuario = {
                'id': observacion.id,
                'usuario': {
                    'id': observacion.usuario.id,
                    'username': observacion.usuario.username,
                    'email': observacion.usuario.email,
                },
                'planificacion': observacion.planificacion.id if observacion.planificacion else None,
                'observacion': observacion.observacion,
                'modificado': observacion.modificado,
                'creado': observacion.creado
            }
            observaciones_con_usuario.append(observacion_con_usuario)

        response_data = {
            'datos': observaciones_con_usuario,            
        }
        return JsonResponse(response_data)
# class PAA_RolViewSet(viewsets.ModelViewSet):
#     queryset = PAA_Rol.objects.all().order_by('-id')
#     serializer_class = PAA_RolSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['planificacion','tipo', 'rol']

#====================== Planificación Académica ======================

@api_view(['GET'])
def accionesFiltradas(request) :
    actor = request.query_params['actor']
    rol = request.query_params['rol']
    tipo = request.query_params['tipo']
    anio = request.query_params['anio']
    origen = request.query_params['origen']

    filtro = Q()
    dict_filtros = {}
    
    if actor != "Todos" :
        dict_filtros['rol__actor__id'] = actor
    
    if rol != "Todos" :
        dict_filtros['rol__tipo'] = rol

    if tipo != "Todos" :
        dict_filtros['tipo'] = tipo

    if anio != "Todos" :
        dict_filtros['anio'] = anio
    
    if origen != "Todos" :
        dict_filtros['origen'] = origen
    
    if anio == "2022":
        if origen == "URY":
            #dict_filtros['proyecto__isnull'] = False
            filtro |= Q( proyecto__isnull=False, origen ="POA")
            dict_filtros.pop('origen', None)
            
        if origen == "TRANSVERSAL":
            filtro |= Q( proyecto__isnull=True, origen ="POA")
            dict_filtros.pop('origen', None)
            #dict_filtros['proyecto__isnull'] = True

    if anio == "Todos":
        if origen == "URY":
            filtro |= Q(origen="URY", anio__gte=2022) | Q(proyecto__isnull=False, anio=2022)
            dict_filtros.pop('origen', None)
        if origen == "TRANSVERSAL":
            filtro |= Q(origen="TRANSVERSAL", anio__gte=2022) | Q( proyecto__isnull=True, anio=2022)
            dict_filtros.pop('origen', None)


    for item in dict_filtros:
        filtro &= Q(**{item:dict_filtros[item]})    
    qs = Accion.objects.filter(filtro)
    serializer = AccionSimpleSerializer(qs, many=True)

    return Response(serializer.data)

# solo para razones de testing:
def permission_denied_view(request):
    raise PermissionDenied()

# requests de uso interno
# 404
def cuatrocientoscuatro(request, exception=None):
    context = {'state': 'ok'}
    return render(request, 'webapp/404.html', context)

def render_to_pdf(template_reporte, context_dict={}):    
    response = HttpResponse(content_type='application/pdf')    
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

    template = get_template(template_reporte)
    html = template.render(context_dict)
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback
    )

    if pisa_status.err:
        return HttpResponse("some problem with pdf")
    return response

def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = STATIC_URL        # Typically /static/
                    sRoot = STATIC_ROOT      # Typically /home/userX/project_static/

                    if uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl)
                    )
            return path
