from django.contrib import admin
from django.contrib.admin import AdminSite
from django import forms
from django.contrib.admin import SimpleListFilter
from .models import *
from .models_paa import *
from .models import ReporteAccion as ReportesAcciones
from .models import Indicador as Indicadores

class ConDirGoogleFilter(admin.SimpleListFilter):
    title = 'Tiene dirGoogle'
    parameter_name = 'con_dir_google'

    def lookups(self, request, model_admin):
        return (
            ('con', 'Con Directorio Drive'),
            ('sin', 'Sin Directorio Drive'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'con':
            return queryset.filter(dirGoogle__isnull=False, accion__anio=2023)
        if self.value() == 'sin':
            return queryset.filter(dirGoogle__isnull=True, accion__anio=2023)
        
class ConDirGoogleFilterIndicador(admin.SimpleListFilter):
    title = 'Tiene dirGoogle'
    parameter_name = 'con_dir_google'

    def lookups(self, request, model_admin):
        return (
            ('con', 'Con dirGoogle'),
            ('sin', 'Sin dirGoogle'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'con':
            return queryset.filter(dirGoogle__isnull=False)
        if self.value() == 'sin':
            return queryset.filter(dirGoogle__isnull=True)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    actions = None
    #list_display = ('id_accion','usuario', 'descripcion', 'estado')
    list_filter = ['estado','mdv__accion__id_uaysen']
    search_fields = ['mdv__accion__id_uaysen','usuario__first_name','usuario__last_name','estado','descripcion']
    
    @admin.display(ordering='mdv__accion__id_uaysen')
    def id_accion(self, obj):
        return obj.mdv.accion.id_uaysen

@admin.register(Verificador)
class VerificadorAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion','usuario', 'descripcion', 'estado')
    list_filter = ['estado','indicador__funcion__accion__id_uaysen']
    search_fields = ['indicador__funcion__accion__id_uaysen','usuario__first_name','usuario__last_name','estado','descripcion']

    @admin.display(ordering='indicador__funcion__accion')
    def id_accion(self, obj):
        return obj.indicador.funcion.accion.id_uaysen

@admin.register(Plazo)
class PlazoAdmin(admin.ModelAdmin):
    actions = None

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('nombre_usuario', 'email_usuario','actor','es_encargado', 'es_analistaUPCI')
    list_filter = ['es_encargado','es_analistaUPCI','actor']
    search_fields = ['usuario__first_name','usuario__last_name', 'actor__nombre', 'actor__sigla']
        
    @admin.display(ordering='accion__id_uaysen')
    def nombre_usuario(self, obj):
        nombre = obj.usuario.first_name +" " + obj.usuario.last_name
        return nombre

    @admin.display(ordering='accion__id_uaysen')
    def email_usuario(self, obj):
        return obj.usuario.email

    class FiltroEntrega(SimpleListFilter):
        title = 'Tipo de Entrega'
        parameter_name = 'producto'

        def lookups(self, request, model_admin):
            return (
                ('Productos', ('Productos')),
                ('Verificadores', ('Verificadores'))
            )

        def queryset(self, request, queryset):
            if self.value() == 'Productos':
                return queryset.exclude(producto__isnull=True)
            if self.value() == 'Verificadores':
                return queryset.exclude(producto__isnull=False)

@admin.register(RetroEntrega)
class RetroEntregaAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('accion','entrega','usuario', 'retroalimentacion')
    search_fields = ['producto__mdv__accion__id_uaysen','verificador__indicador__funcion__accion__id_uaysen','usuario__first_name','usuario__last_name','retroalimentacion']
    #list_filter = [FiltroEntrega]

    @admin.display(ordering='accion__id_uaysen')
    def entrega(self, obj):
        if obj.producto:
            return "Producto: " + obj.producto.descripcion
        else:
            return "Verificador: " + obj.verificador.descripcion

    @admin.display(ordering='accion__id_uaysen')
    def accion(self, obj):
        if obj.producto:
            return obj.producto.mdv.accion.id_uaysen
        else:
            return obj.verificador.indicador.funcion.accion.id_uaysen

@admin.register(Reporte)
class Reporte(admin.ModelAdmin):
    actions = None
    list_display = ('acciones','actor','estado', 'tipo')
    #search_fields = ['actor__nombre', 'actor__sigla', 'estado', 'tipo']
    search_fields = ['tipo']
    list_filter = ['estado', 'tipo']
        #@admin.display(ordering='accion__id_uaysen')
    def acciones(self,obj):    
        acciones = list(ReportesAcciones.objects.filter(detalle_reporte=obj).values_list('accion__id_uaysen', flat=True))
        return acciones

@admin.register(ReporteAccion)
class ReporteAccion(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion','id_reporte','detalle','estado_ejecucion')

    @admin.display(ordering='accion__id_uaysen')
    def id_reporte(self, obj):
        return obj.detalle_reporte.id

    @admin.display(ordering='accion__id_uaysen')
    def id_accion(self, obj):
        return obj.accion.id_uaysen
        
    @admin.display(ordering='accion__id_uaysen')
    def detalle(self, obj):
        return "Reporte Unidad: " + obj.detalle_reporte.actor.nombre + " ("+obj.detalle_reporte.actor.sigla + ")"

@admin.register(ReporteFuncion)
class ReporteFuncion(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion','nombre_funcion','indicador')

    @admin.display(ordering='accion__id_uaysen')
    def nombre_funcion(self, obj):
        return obj.funcion.nombre

    @admin.display(ordering='accion__id_uaysen')
    def id_accion(self, obj):
        return obj.dependencia.accion.id_uaysen

@admin.register(ReporteHito)
class ReporteHito(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion','nombre_hito','indicador','indicador_logro')

    @admin.display(ordering='accion__id_uaysen')
    def nombre_hito(self, obj):
        return obj.hito.nombre

    @admin.display(ordering='accion__id_uaysen')
    def id_accion(self, obj):
        return obj.dependencia.accion.id_uaysen

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion','actor', 'tipo')
    list_filter = ['tipo', 'actor','accion__id_uaysen']
    search_fields = ['accion__id_uaysen', 'actor__nombre', 'actor__sigla']

    @admin.display(ordering='accion__id_uaysen')
    def id_accion(self, obj):
        return obj.accion.id_uaysen

@admin.register(Hito)
class HitoAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion', 'nombre', 'plazo_hito')
    list_filter = (ConDirGoogleFilter,)
    search_fields = ['accion__id_uaysen','nombre','plazo__plazo_anio']

    @admin.display(ordering='accion__id_uaysen')
    def id_accion(self, obj):
        return obj.accion.id_uaysen
        
    #@admin.display(ordering='accion__id_uaysen')
    def plazo_hito(self, obj):
        
        if(obj.plazo is None):
            plazo_hito = "No definido"            
        else:
            if(obj.plazo.plazo_anio < 2000):
                plazo_hito = obj.plazo.plazo_mes + "-" + "20" + str(obj.plazo.plazo_anio)
            else:
                plazo_hito = obj.plazo.plazo_mes + "-" + str(obj.plazo.plazo_anio)
        return plazo_hito
        

@admin.register(Funcion)
class FuncionAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion', 'nombre', 'indicador', 'meta')
    search_fields = ['accion__id_uaysen','nombre']
    list_filter = (ConDirGoogleFilter,)

    @admin.display(ordering='accion__id_uaysen')
    def id_accion(self, obj):
        return obj.accion.id_uaysen
        
    def indicador(self,obj):    
        indicador = list(Indicadores.objects.filter(funcion=obj).values_list('nombreVerificador', flat=True))
        return indicador
            
    def meta(self,obj):    
        meta = list(Indicadores.objects.filter(funcion=obj).values_list('meta', flat=True))
        return meta

@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion', 'nombre', 'nombreVerificador','formula')
    search_fields = ['funcion__accion__id_uaysen','nombre','nombreVerificador']
    list_filter = (ConDirGoogleFilterIndicador,)

    @admin.display(ordering='funcion__accion__id_uaysen')
    def id_accion(self, obj):
        return obj.funcion.accion.id_uaysen

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('nombre', 'sigla', 'es_area', 'dependencia')
    list_filter = ['es_area','es_direccion','categoria']
    search_fields = ['nombre' ,'sigla','dependencia__nombre']
    ordering = ['nombre']

@admin.register(Accion)
class AccionAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id_uaysen', 'tipo', 'objetivo','origen')
    list_filter = ['tipo','proyecto','origen',]
    search_fields = ['id_uaysen__icontains' ,'tipo', 'origen','objetivo']
    ordering = ['id_uaysen']

@admin.register(MDV)
class MDVAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('id_accion', 'nombre')
    #list_filter = ['accion']
    search_fields = ['accion__id_uaysen','nombre']

    @admin.display(ordering='accion__id_uaysen')
    def id_accion(self, obj):
        return obj.accion.id_uaysen

#====================== Planificación Académica ======================
class PlanificacionesAdminSite(AdminSite):
    site_header = 'Panel de Planificación Anual Académica'

planificaciones_admin_site = PlanificacionesAdminSite(name='planificaciones')
planificaciones_admin_site.register(PAA_Asignatura)
planificaciones_admin_site.register(PAA_Planificacion)

@admin.register(PAA_Asignatura)
class PAA_AsignaturaAdmin(admin.ModelAdmin):
    actions = None    
    search_fields = ['nombre','codigo']
    list_filter = ['departamento', 'estado','semestre','modalidad']
    ordering = ['nombre']
    list_display = ('nombre','codigo', 'departamento', 'estado','id_ucampus','semestre','modalidad')

@admin.register(PAA_Planificacion)
class PAA_PlanificacionAdmin(admin.ModelAdmin):
    actions = None    
    list_filter = ['usuario__first_name','usuario__last_name','rut_academicx','estado', 'modificado', 'creado','anio','accion__id_uaysen']
    list_display = ('usuario','estado', 'rut_academicx','categoria','departamento','fecha_ingreso','jornada','modificado', 'creado','anio','total_horas','accion')

@admin.register(PAA_PlanificacionDocencia)
class PAA_PlanificacionDocenciaAdmin(admin.ModelAdmin):
    actions = None    
    list_filter = ['asignatura__codigo','planificacion__usuario__first_name','planificacion__usuario__last_name','tipo','semestre','programa','descripcion','observacion']
    list_display = ('planificacion','asignatura','rol','tipo','semestre','programa','descripcion','observacion')

@admin.register(PAA_PlanificacionInvestigacion)
class PAA_PlanificacionInvestigacionAdmin(admin.ModelAdmin):
    actions = None    
    list_filter = ['planificacion__usuario__first_name','planificacion__usuario__last_name','nombre_proyecto','descripcion','tipo','estado_proyecto','autoria']
    list_display = ('nombre_proyecto','descripcion','rol','tipo','estado_proyecto','autoria')

@admin.register(PAA_PlanificacionGestion)
class PAA_PlanificacionGestionAdmin(admin.ModelAdmin):
    actions = None    
    list_filter = ['planificacion__usuario__first_name','planificacion__usuario__last_name','nombre_actividad','cargo']
    list_display = ('planificacion','nombre_actividad','cantidad_horas','cargo')

@admin.register(PAA_PlanificacionVinculacion)
class PAA_PlanificacionVinculacionAdmin(admin.ModelAdmin):
    actions = None    
    list_filter = ['planificacion__usuario__first_name','planificacion__usuario__last_name','nombre_actividad','unidad','linea_accion','frecuencia','fecha_inicio','fecha_fin']
    list_display = ('planificacion','nombre_actividad','rol','unidad','linea_accion','frecuencia','fecha_inicio','fecha_fin')

@admin.register(PAA_PlanificacionFormacion)
class PAA_PlanificacionFormacionAdmin(admin.ModelAdmin):
    actions = None    
    list_filter = ['planificacion__usuario__first_name','planificacion__usuario__last_name','nombre_actividad','institucion','fecha_inicio','fecha_fin']
    list_display = ('planificacion','nombre_actividad','institucion','fecha_inicio','fecha_fin','cantidad_horas')

# class PAA_RolForm(forms.ModelForm):
#     class Meta:
#         model = PAA_Rol
#         fields = '__all__'

#     def clean_rol(self):
#         tipo = self.cleaned_data.get('tipo')
#         rol = self.cleaned_data.get('rol')
        
#         # Obtener las opciones de roles para el tipo seleccionado
#         opciones_roles = dict(ROLES_CHOICES.get(tipo, ()))

#         # Verificar si el rol seleccionado es una opción válida
#         if rol not in opciones_roles:
#             raise forms.ValidationError(f"{rol} no eds una opción válida para el tipo {tipo}.")

#         return rol


# @admin.register(PAA_Rol)
# class PAA_RolAdmin(admin.ModelAdmin):
#     list_display = ('planificacion', 'tipo', 'rol')
#     list_filter = ('tipo','rol')

@admin.register(PAA_ObservacionPlanificacion)
class PAA_ObservacionPlanificacionAdmin(admin.ModelAdmin):
    actions = None    
    list_filter = ['usuario__first_name','usuario__last_name','planificacion','observacion','modificado','creado']
    list_display = ('usuario','planificacion','observacion','modificado','creado')
#====================== Planificación Académica ======================