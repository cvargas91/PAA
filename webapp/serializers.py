from pickle import TRUE
from django.contrib.auth.models import User, Group
from .models import Accion, Actor, Rol, Producto, Verificador,\
    RetroEntrega, MDV, Hito, Funcion, Indicador, Estrategia, Reporte,\
    ReporteAccion, ReporteFuncion, ReporteHito, Dimension
from .models_paa import *
from rest_framework import serializers,fields
from drf_writable_nested.serializers import WritableNestedModelSerializer
from pytz import timezone
from collections import OrderedDict, defaultdict

from spci.settings import TIME_ZONE

class HitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hito
        fields = '__all__'

class IndicadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = '__all__'

class FuncionSerializer(serializers.ModelSerializer):
    indicador_set = IndicadorSerializer(read_only=True, many=True)
    class Meta:
        model = Funcion
        fields = ['accion', 'nombre', 'dirGoogle', 'indicador_set']

### Elementos del sistema subidos por los usuarios
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'usuario', 'mdv', 'hitos', 'descripcion', 'estado', 'adjuntos', 'modificado', 'creado']
        
    def update(self, instance, validate_data):
        instance.mdv = validate_data.get('mdv', instance.mdv)        
        instance.hitos.set(validate_data.get('hitos', instance.hitos))
        instance.descripcion = validate_data.get('descripcion', instance.descripcion)
        instance.adjuntos = validate_data.get('adjuntos', instance.adjuntos)
        instance.modificado = validate_data.get('modificado', instance.modificado)
        instance.save()
        return instance

class ProductoDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'usuario', 'mdv', 'hitos', 'descripcion', 'estado', 'adjuntos', 'modificado', 'creado']
        depth = 3

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["fecha_creacion"] = instance.creado.strftime('%d/%m/%Y')
        return data

class VerificadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificador
        fields = ['id', 'usuario', 'indicador', 'valor', 'descripcion', 'adjuntos', 'estado', 'modificado', 'creado']
    
    def update(self, instance, validated_data):
        instance.indicador = validated_data.get('indicador', instance.indicador)
        instance.valor = validated_data.get('valor', instance.valor)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.adjuntos = validated_data.get('adjuntos', instance.adjuntos)
        instance.modificado = validated_data.get('modificado', instance.modificado)
        instance.save()
        return instance
    

class VerificadorDepthSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Verificador
        fields = ['id', 'usuario', 'indicador', 'valor', 'descripcion', 'adjuntos', 'estado', 'modificado', 'creado']
        depth = 3

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["fecha_creacion"] = instance.creado.strftime('%d/%m/%Y')        
        return data
### (FIN) Elementos del sistema subidos por los usuarios

class RetroEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroEntrega
        fields = ['id', 'usuario', 'producto', 'verificador', 'retroalimentacion']
    
    def to_representation (self, instance):
        data = super().to_representation(instance)
        new_format = "%d/%m/%Y - %H:%M:%S"
        new_date_modificado = instance.modificado.astimezone(timezone(TIME_ZONE))
        new_date_creado     = instance.creado.astimezone(timezone(TIME_ZONE))
        data["creado"] = new_date_creado.strftime(new_format)
        data["modificado"] = new_date_modificado.strftime(new_format)
        return data

class ReporteFuncionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteFuncion
        fields =['id','id_tactica','funcion','indicador','comentario_cumplimiento']

class ReporteHitoSerializer(serializers.ModelSerializer):
    #mdvs = MDVSerializer(many=True)
    #hitos = HitoSerializer(many=True)
    class Meta:
        model = ReporteHito
        fields = ['id','id_tactica','mdvs','hito','indicador','indicador_logro','justificacion_contingencia','reporte_justificacion_contingencia','comentario_cumplimiento']

class ReporteAccionSerializer(serializers.ModelSerializer):
    reporte_funciones = ReporteFuncionSerializer(many=True)
    reporte_hitos = ReporteHitoSerializer(many=True)
    
    class Meta:
        model = ReporteAccion
        fields = ['id','accion','estado_ejecucion','justificacion_contingencia','reporte_justificacion_contingencia','indicador','indicador_logro','reporte_funciones','reporte_hitos','recomendacion']


class ReporteSerializer(serializers.ModelSerializer):
    reporte_acciones = ReporteAccionSerializer(many=True)

    class Meta:
        model = Reporte
        fields = ['id', 'usuario', 'actor', 'estado', 'recomendacion','tipo','enviado','reporte_acciones','creado','modificado']    

    def create(self, validated_data):
        reporte_acciones = validated_data.pop('reporte_acciones')
        reporte_data = Reporte.objects.create(**validated_data)

        for reporte_accion in reporte_acciones:
            funciones_data = reporte_accion.pop('reporte_funciones')
            hitos_data = reporte_accion.pop('reporte_hitos')

            reporte_accion_data=ReporteAccion.objects.create(detalle_reporte=reporte_data,**reporte_accion)
            
            for funcion_data in funciones_data:
                ReporteFuncion.objects.create(dependencia=reporte_accion_data,**funcion_data)            
            for hito in hitos_data:
                #id_hitos = hito.pop('hitos')
                id_mdvs = hito.pop('mdvs')
                repo_hito = ReporteHito.objects.create(dependencia=reporte_accion_data, **hito)
                #for id_hito in id_hitos:
                #    repo_hito.hitos.add(id_hito)
                for id_mdv in id_mdvs:
                    repo_hito.mdvs.add(id_mdv)
                    
        return reporte_data
        
    def update(self, instance ,validated_data):
        
        reporte_acciones = validated_data.pop('reporte_acciones')
        instance.estado = validated_data.get('estado', instance.estado)
        instance.enviado = validated_data.get('enviado', instance.enviado)
        instance.recomendacion = validated_data.get('recomendacion', instance.recomendacion)
        instance.modificado = validated_data.get('modificado', instance.modificado)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        reporte_acciones_data = (instance.reporte_acciones).all()
        reporte_acciones_data = list(reporte_acciones_data)
        #instance.reporte_acciones = validated_data.get('reporte_acciones', instance.reporte_acciones)
        instance.save()
        
        reporte_accion_nuevos_id = []
        
        #se agregan o modifican nuevos reportes de acciones
        for reporte_accion in reporte_acciones:
            funciones_data = reporte_accion.pop('reporte_funciones')
            hitos_data = reporte_accion.pop('reporte_hitos')

            if "id" in reporte_accion.keys():
                if ReporteAccion.objects.filter(id=reporte_accion['id']).exists():
                    reporte_accion_instance = ReporteAccion.objects.get(id=reporte_accion['id'])
                    reporte_accion_instance.detalle_reporte = reporte_accion.get('detalle_reporte', reporte_accion_instance.detalle_reporte)
                    #reporte_accion_instance.mdvs.append(reporte_accion.get('mdvs', reporte_accion_instance.mdvs))
                    reporte_accion_instance.estado_ejecucion = reporte_accion.get('estado_ejecucion', reporte_accion_instance.estado_ejecucion)
                    reporte_accion_instance.justificacion_contingencia = reporte_accion.get('justificacion_contingencia', reporte_accion_instance.justificacion_contingencia)
                    reporte_accion_instance.reporte_justificacion_contingencia = reporte_accion.get('reporte_justificacion_contingencia', reporte_accion_instance.reporte_justificacion_contingencia)
                    reporte_accion_instance.recomendacion = reporte_accion.get('recomendacion', reporte_accion_instance.recomendacion)
                    for funcion_data in funciones_data:
                        ReporteFuncion.objects.create(dependencia=reporte_accion_instance,**funcion_data)            
                    for hito in hitos_data:
                        #id_hitos = hito.pop('hitos')
                        id_mdvs = hito.pop('mdvs')
                        repo_hito = ReporteHito.objects.create(dependencia=reporte_accion_instance, **hito)
                        #for id_hito in id_hitos:
                        #    repo_hito.hitos.add(id_hito)
                        for id_mdv in id_mdvs:
                            repo_hito.mdvs.add(id_mdv)

                    reporte_accion_instance.save()
                    reporte_accion_nuevos_id.append(reporte_accion_instance.id)
                else:
                    continue
            else:
                reporte_accion_instance = ReporteAccion.objects.create(detalle_reporte=instance, **reporte_accion)
                for funcion_data in funciones_data:
                    ReporteFuncion.objects.create(dependencia=reporte_accion_instance,**funcion_data)            
                for hito in hitos_data:
                #     id_hitos = hito.pop('hitos')
                    id_mdvs = hito.pop('mdvs')
                    repo_hito = ReporteHito.objects.create(dependencia=reporte_accion_instance, **hito)
                    #for id_hito in id_hitos:
                    #    repo_hito.hitos.add(id_hito)

                    for id_mdv in id_mdvs:
                        repo_hito.mdvs.add(id_mdv)
                    #ReporteHito.objects.create(dependencia=reporte_accion_instance, **hito)
                reporte_accion_nuevos_id.append(reporte_accion_instance.id)

        #se eliminan reportes de acciones que no esten en el request
        for reporte_accion_id in instance.reporte_acciones.values_list('id', flat=True):
            if reporte_accion_id not in reporte_accion_nuevos_id:
                ReporteAccion.objects.filter(pk=reporte_accion_id).delete()
        
        return instance

    
    def to_representation (self, instance):
        data = super().to_representation(instance)
        new_format = "%d/%m/%Y - %H:%M:%S"
        new_date_modificado = instance.modificado.astimezone(timezone(TIME_ZONE))
        new_date_creado     = instance.creado.astimezone(timezone(TIME_ZONE))
        data["creado"] = new_date_creado.strftime(new_format)
        data["modificado"] = new_date_modificado.strftime(new_format)
        return data

class ActualizaVerificadorSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.mdv = validated_data.get('mdv', instance.mdv)
        instance.hitos = validated_data.get('hitos', instance.hitos)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.adjuntos = validated_data.get('adjuntos', instance.adjuntos)
        instance.modificado = serializers.DateTimeField(auto_now=True)
        instance.save()
        return instance

    class Meta:
        model = Verificador
        fields = ['id', 'usuario', 'mdv', 'hitos', 'descripcion', 'estado', 'adjuntos', 'modificado', 'creado']

class ActualizaProductoSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.mdv = validated_data.get('mdv', instance.mdv)
        instance.hitos = validated_data.get('hitos', instance.hitos)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.adjuntos = validated_data.get('adjuntos', instance.adjuntos)
        instance.modificado = serializers.DateTimeField(auto_now=True)
        instance.save()
        return instance

    class Meta:
        model = Producto
        fields = ['id', 'usuario', 'mdv', 'hitos', 'descripcion', 'estado', 'adjuntos', 'modificado', 'creado']

class RolSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Rol
        fields = ['id', 'accion', 'actor', 'tipo']
        depth = 3

class RolSimpleSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Rol
        fields = ['id', 'actor', 'tipo']
        depth = 1

class EstrategiasSimpleSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Estrategia
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["value"] = instance.id
        data["label"] = instance.id_uaysen
        return data

class AccionSerializer(serializers.ModelSerializer):
    rol_set = RolSimpleSerializer(read_only=True, many=True)
    class Meta:
        model = Accion
        fields = ['id', 'titulo', 'id_uaysen', \
            'objetivo', 'tipo', 'anio', 'proyecto', \
            'estrategias','dimensiones' ,'rol_set', 'dirGoogle',
            'presupuesto','origen']
        depth = 1

class AccionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accion
        fields = ['id', 'titulo', 'id_uaysen', \
            'objetivo', 'tipo', 'anio', 'proyecto', \
            'estrategias', 'dimensiones','presupuesto','origen']
        depth = 1

class MDVSerializer(serializers.ModelSerializer):
    class Meta:
        model = MDV
        fields = ['id', 'accion', 'nombre', 'dirGoogle']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["value"] = instance.id
        data["label"] = instance.nombre
        return data

class ActorSerializer(serializers.ModelSerializer):
    #rol_set = RolSimpleSerializer(read_only=True, many=True)
    class Meta:
        model = Actor
        fields = ['id', 'nombre', 'id_uaysen', \
            'sigla', 'cai', 'es_area', 'categoria', \
            'dependencia', 'es_direccion']
        depth = 1

class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = ['id', 'nombre','texto_ley']
        depth = 1

#====================== Planificación Académica ======================

class PAA_AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAA_Asignatura
        fields = ['id', 'nombre','codigo','departamento','estado','id_ucampus','semestre','modalidad']
        depth = 1

class PAA_PlanificacionDocenciaSerializer(serializers.ModelSerializer):
    # asignatura = PAA_AsignaturaSerializer(many=True)

    class Meta:
        model = PAA_PlanificacionDocencia
        fields = ['id','planificacion','asignatura','rol','tipo','semestre','cantidad_horas','programa','descripcion','observacion']

class PAA_PlanificacionInvestigacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAA_PlanificacionInvestigacion
        fields = '__all__'

class PAA_PlanificacionGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAA_PlanificacionGestion
        fields = '__all__'

class PAA_PlanificacionVinculacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAA_PlanificacionVinculacion
        fields = '__all__'

class PAA_PlanificacionFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAA_PlanificacionFormacion
        fields = '__all__'

class PAA_PlanificacionSerializer(serializers.ModelSerializer):
    planificaciones_docencia      = PAA_PlanificacionDocenciaSerializer(many=True)
    planificaciones_investigacion = PAA_PlanificacionInvestigacionSerializer(many=True)
    planificaciones_gestion       = PAA_PlanificacionGestionSerializer(many=True)
    planificaciones_vinculacion   = PAA_PlanificacionVinculacionSerializer(many=True)
    planificaciones_formacion     = PAA_PlanificacionFormacionSerializer(many=True)

    class Meta:
        model = PAA_Planificacion
        fields = ['id','usuario', 'estado', 'categoria','rut_academicx','departamento','fecha_ingreso','jornada','modificado', 'creado','anio','total_horas','accion',\
                    'planificaciones_docencia','planificaciones_vinculacion','planificaciones_formacion','planificaciones_gestion','planificaciones_investigacion']

    def create(self, validated_data):
        planificaciones_docencia     = validated_data.pop('planificaciones_docencia',[]) 
        planificaciones_investigacion= validated_data.pop('planificaciones_investigacion',[])
        planificaciones_gestion      = validated_data.pop('planificaciones_gestion',[])
        planificaciones_vinculacion  = validated_data.pop('planificaciones_vinculacion',[])
        planificaciones_formacion    = validated_data.pop('planificaciones_formacion',[])

        planificacion = PAA_Planificacion.objects.create(**validated_data)

        PAA_PlanificacionDocencia.objects.bulk_create(
            [PAA_PlanificacionDocencia(planificacion=planificacion, **data) for data in planificaciones_docencia]
        )
        
        PAA_PlanificacionInvestigacion.objects.bulk_create(
            [PAA_PlanificacionInvestigacion(planificacion=planificacion, **data) for data in planificaciones_investigacion]
        )

        PAA_PlanificacionGestion.objects.bulk_create(
            [PAA_PlanificacionGestion(planificacion=planificacion, **data) for data in planificaciones_gestion]
        )

        PAA_PlanificacionVinculacion.objects.bulk_create(
            [PAA_PlanificacionVinculacion(planificacion=planificacion, **data) for data in planificaciones_vinculacion]
        )

        PAA_PlanificacionFormacion.objects.bulk_create(
            [PAA_PlanificacionFormacion(planificacion=planificacion, **data) for data in planificaciones_formacion]
        )

        return planificacion

    def update(self, instance, validated_data):
        instance.estado         = validated_data.get('estado', instance.estado)
        instance.modificado     = validated_data.get('modificado', instance.modificado)
        instance.total_horas    = validated_data.get('total_horas', instance.total_horas)
        instance.anio           = validated_data.get('anio', instance.anio)
        instance.accion         = validated_data.get('accion', instance.accion)
        instance.rut_academicx  = validated_data.get('rut_academicx', instance.rut_academicx)
        instance.categoria      = validated_data.get('categoria', instance.categoria)
        instance.departamento   = validated_data.get('departamento', instance.departamento)
        instance.jornada        = validated_data.get('jornada', instance.jornada)
        instance.save()

        # Diccionario que mapea los tipos de planificación a los modelos correspondientes
        planificacion_models = {
            'docencia': PAA_PlanificacionDocencia,
            'investigacion': PAA_PlanificacionInvestigacion,
            'gestion': PAA_PlanificacionGestion,
            'vinculacion': PAA_PlanificacionVinculacion,
            'formacion': PAA_PlanificacionFormacion,
        }
        # Crear un diccionario de IDs por tipo de planificación
        existing_ids_by_type = defaultdict(set)
        for planificacion_type, model in planificacion_models.items():
            existing_ids = model.objects.filter(planificacion=instance).values_list('id', flat=True)
            existing_ids_by_type[planificacion_type] = set(existing_ids)

        for planificacion_type, model in planificacion_models.items():
            planificacion_data = validated_data.get(f'planificaciones_{planificacion_type}', [])

            if planificacion_type == 'docencia':

                # Obtener las asignaturas incluidas en la planificación de docencia para actualizar su estado.
                asignaturas_incluidas = set(data.get('asignatura').id for data in planificacion_data if 'asignatura' in data)

                # Actualizar el estado de las asignaturas a "Asignada"
                PAA_Asignatura.objects.filter(id__in=asignaturas_incluidas).update(estado='Asignada')

            # Actualizar o crear planificaciones de este tipo
            for data in planificacion_data:
                planificacion_id = data.get('id')
                if planificacion_id:
                    # Si el ID está en la base de datos, actualiza la instancia
                    planificacion = model.objects.get(id=planificacion_id)
                else:
                    # Si no hay ID, crea una nueva instancia
                    planificacion = model(planificacion=instance)
                for field, value in data.items():
                    setattr(planificacion, field, value)
                planificacion.save()

            # Eliminar registros existentes que no están en la nueva planificación
            for existing_id in existing_ids_by_type[planificacion_type]:
                if existing_id not in {data.get('id') for data in planificacion_data}:
                    model.objects.filter(id=existing_id).delete()        

        return instance

    
    def to_representation (self, instance):
        data = super().to_representation(instance)
        new_format = "%d/%m/%Y - %H:%M:%S"
        new_date_modificado = instance.modificado.astimezone(timezone(TIME_ZONE))
        new_date_creado     = instance.creado.astimezone(timezone(TIME_ZONE))
        data["creado"] = new_date_creado.strftime(new_format)
        data["modificado"] = new_date_modificado.strftime(new_format)        

        return data
    
class PAA_PlanificacionDepthSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAA_Planificacion
        fields = ['id', \
                    'planificaciones_docencia','planificaciones_investigacion','planificaciones_gestion','planificaciones_vinculacion','planificaciones_formacion',\
                    'usuario', 'estado', 'modificado', 'creado','anio','total_horas','accion']
        depth = 3
        
    def to_representation (self, instance):
        data = super().to_representation(instance)
        new_format = "%d/%m/%Y - %H:%M:%S"
        new_date_modificado = instance.modificado.astimezone(timezone(TIME_ZONE))
        new_date_creado     = instance.creado.astimezone(timezone(TIME_ZONE))
        data["creado"] = new_date_creado.strftime(new_format)
        data["modificado"] = new_date_modificado.strftime(new_format)
        return data

# class PAA_RolSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PAA_Rol
#         fields = ['id', 'planificacion','tipo','rol']
#         depth = 1

class PAA_ObservacionPlanificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAA_ObservacionPlanificacion
        fields = ['id', 'usuario','planificacion','observacion','modificado','creado']        
#====================== Planificación Académica ======================