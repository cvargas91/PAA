<template>
    Página en construcción/Edición Reporte Unificado URY-PMI-TRANSVERSAL    
    <q-scroll-area style="height: 700px;">
        <q-card 
            class="my-card" 
            align="center"
            flat bordered
            v-if="dataReady"
            style="height:770pt"
        >
            <q-card-actions align="around" style="padding-bottom:0pt" >
                <div style="padding-left:40pt">
                    <p style="margin-top:5pt; margin-bottom:0pt; text-align:left; color:#385280; font-size:11pt">
                        <strong>Reporte Medios de Verificación</strong>                        
                    </p>
                    <p style="margin-top:0pt; margin-bottom:0pt; text-align:left; color:#385280; font-size:8pt">
                        Planificación Operativa Anual
                    </p>
                    <p style="margin-top:0pt; margin-bottom:0pt; text-align:left; color:#385280; font-size:7pt">
                        <span style="background-color:#d9e2f3"> 
                            {{mes}} {{anio}}
                        </span>
                    </p>
                </div>
                <q-card-section horizontal style="padding-right:30pt">
                    <div style="margin-top:9pt; margin-right:5pt">
                        <img 
                            id="logo"
                            src="/static/webapp/Colabora-logo_recortado.png"
                            name="image1.jpg" 
                            align="center" 
                            width="140" 
                            height="30" 
                        />
                            <p align="center" style="color:#385280; font-size:5pt;padding-left:4pt; padding-top:0pt">
                                Plataforma de Planificación y Coordinación <br/>
                                Institucional UAysén
                            </p>
                    </div>
            
                    <img 
                        id="logo"
                        src="/static/webapp/uaysen-nuevo-1.png"
                        name="image1.jpg" 
                        width="50" 
                        height="50" 
                        style="margin-top:9pt; margin-right:5pt"
                    />
                </q-card-section>    
            </q-card-actions>

            <hr style="border: 1.5px dashed #385280; margin-right:178pt; margin-left:178pt; padding-top:0pt;">

            <q-card style="margin-right: 0; margin-left: 0; width: 66%; padding-top: 0; padding-bottom: 36pt;">
                <q-card-section horizontal style="justify-content: center;">
                    <q-card-section style="margin-right: 10px; text-align: center; flex: 1;">
                        <strong style="color: #385280; font-size: 10pt;">Líder Estratégico</strong>
                    </q-card-section>
    
                    <q-card-section style="margin-left: 10px; text-align: center; flex: 1;">
                        <strong style="color: #385280; font-size: 10pt;">Líder Ejecutivo</strong>
                    </q-card-section>
                </q-card-section>
                <q-card-section horizontal style="justify-content: center;">
                    <q-card-section class="tarjetaAmarilla" style="margin-right: 10px; text-align: center; flex: 1;">                        
                        <p style="color: #385280; font-size: 10pt; padding-top:10pt">{{defineActorEstrategico(accionesAReportar.rol_set)}}</p> 
                    </q-card-section>
    
                    <q-card-section class="tarjetaAmarilla" style="margin-left: 10px; text-align: center; flex: 1;">                        
                        <p style="color: #385280; font-size: 10pt;padding-top:10pt">{{defineActor(accionesAReportar.rol_set)}}</p>
                    </q-card-section>
                </q-card-section>
            </q-card>

            <hr style="border: 1.5px dashed #385280; margin-right:178pt; margin-left:178pt; padding-top:0pt;">

            <q-card style="margin-right: 0; margin-left: 0; width: 66%; padding-top: 0; padding-bottom: 2pt;">
                <q-card-section horizontal style="justify-content: center;">
                    <q-card-section style="margin-right: 10px; text-align: center; flex: 0.25;">
                        <strong style="color: #385280; font-size: 10pt;">Identificador de la Acción</strong>
                    </q-card-section>
    
                    <q-card-section style="margin-left: 10px; text-align: center; flex: 1;">
                        <strong style="color: #385280; font-size: 10pt;">Título</strong>
                    </q-card-section>
                </q-card-section>
    
                <q-card-section horizontal style="justify-content: center;">
                    <q-card-section class="tarjetaAmarilla" style="margin-right: 10px; text-align: center; flex: 0.25;">                                            
                        <q-select
                            v-model="model"
                            :options="opciones"
                            :option-label="(item) => item === null ? 'Null' : getAccion(item.accion)"
                            @update:model-value="cambio"
                            style="width: 100%; height:40%; margin-left:0pt; margin-bottom:0pt"
                            item-aligned 
                        />
                    </q-card-section>
    
                    <q-card-section class="tarjetaAmarilla" style="margin-left: 10px; text-align: center; flex: 1;">
                        <p style="color: #385280; font-size: 10pt; padding-top: 20pt;">{{accionesAReportar.titulo}}</p>
                    </q-card-section>
                </q-card-section>            
            </q-card> 
            
            <ReporteFuncionUnificadoEdicion v-if="acciones.funciones.length && dataFuncionHito"
                :reporteAccion="model"
                :reporteFunciones="model.reporte_funciones"
                :identificador="accionesAReportar.id_uaysen"                
            />
            
            <ReporteHitoUnificadoEdicion v-if="validaReporteHito() && dataFuncionHito"
                :reporteAccion="model"
                :identificador="accionesAReportar.id_uaysen"                                
            />
            
            <ReporteAccionUnificadoEdicion v-if="validaReporteAccion() && dataFuncionHito"
                :opcionesJustificacion="opcionesJustificacion"
                :indiceReporteAccion="indiceReporteAccion"
                :reporteAccion="model"
                @cambioReporteAccion="cambioReporteAccion"
                @guardarReporte="guardarReporte"
                @guardarReporteFinalizado="guardarReporteFinalizado"
                @siguienteReporteAccion="siguienteReporteAccion"
            />
        </q-card>        
    </q-scroll-area>
</template>

<script>
    import { ref, toRef, watch ,watchEffect, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    

    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";    
    import ReporteAccionUnificadoEdicion from "src/components/componentesReportes/EdicionUnificado/ReporteAccionUnificadoEdicion.vue";
    import ReporteFuncionUnificadoEdicion from "src/components/componentesReportes/EdicionUnificado/ReporteFuncionUnificadoEdicion.vue";
    import ReporteHitoUnificadoEdicion from "src/components/componentesReportes/EdicionUnificado/ReporteHitoUnificadoEdicion.vue";

    export default defineComponent({
        components:{                    
            BotonCancelarReporte,
            ReporteHitoUnificadoEdicion,
            ReporteAccionUnificadoEdicion,
            ReporteFuncionUnificadoEdicion,
        },
        props: {
                usuario: Object,
                entrega: Object,
                tipoEntrega: String,
        },
        methods:{
            defineActor(rol_set){
                return rol_set[0].actor.id_uaysen
            },
            defineActorEstrategico(rol_set){
                let estrategico = this.actores.find(element => element.id === rol_set[0].actor.dependencia);
                return estrategico.id_uaysen
            },
            getAccion(accion){                
                if(this.acciones.detalleAccionesReporte){
                    const idUaysen = this.acciones.detalleAccionesReporte.find(element => element.accion.id === accion);                    
                    return idUaysen.accion.id_uaysen;
                }
            },
            validaReporteHito(){
                if((!this.acciones.funciones.length) && (this.acciones.detalleAccion && this.acciones.detalleAccion.mdvs.length)){
                    return true;
                }else{
                    return false;
                }
            },
            validaReporteAccion(){
                if((!this.acciones.funciones.length) && (!this.acciones.detalleAccion || !this.acciones.detalleAccion.mdvs.length)){
                    return true;
                }else {
                    return false;
                }
            },
            validaFinReporte(){
                if(!(this.stepPasoAccion)){
                    return true;
                }else {
                    return false;
                }
            },
        },
        setup() {
            const store = useStore();
            const router = useRouter();
            const TIMESTAMP  = Date.now();
            const fechaActual = new Date(TIMESTAMP);
            const fechaFormateada = fechaActual.toLocaleDateString();
            const anio = fechaActual.getFullYear();
            const MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
                            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",];
            const date = new Date();
            const mes = MESES[date.getMonth()];            
            const actores = computed(() => store.state.actor.actores);
            const reporte = computed(() => store.state.reporte);

            const reporteAEditar = computed(() => store.state.reporte.aEditar);
            const accionesAReportar = computed(() => store.state.accion.acciones);
            //const funcion = computed(() => store.state)
            const acciones = computed(() => store.state.accion);
            const detalleProductos = computed(() => store.state.producto.totalHitos);

            const model = ref(reporteAEditar.value.reporte_acciones[0]);
            //const model = ref(reporte.value.nuevoReporte.reporte_acciones[0]);
            const indiceReporteAccion = ref(0);

            const usuario = computed(() => store.state.usuarix.usuario);
            const opcionesJustificacion = {
                "Implementado" : "Todos los MDV fueron cumplidos en el plazo establecido en la acción.",                
                "En Proceso"  : "Se reporta al menos un MdV, acción se implementa en el plazo de ejecución del plan operativo.",
                "Pendiente" : "No se cumple ni un MDV, pero la acción sigue en plazo de ejecución.",
                "No cumplido" : "No se ejecuta la acción."
            };
            
            //["Implementado", "No implementado", "En proceso", "Pendiente", "No aplicable", "No cumplido"];
            const dataReady = ref(false);
            const dataFuncionHito = ref(true);
            const recomendacion = ref(reporteAEditar.value.recomendacion);
            const stepPasoFuncion = ref(0);
            const stepPasoHito    = ref(0);
            const stepPasoAccion = ref(0);
            const finReporteAccion = ref(false);
            
            onMounted( async () => {
                await store.dispatch("accion/reqDetalleAccion", model.value.accion);
                store.dispatch("reporte/setReporteAccionesAEditar",model.value);                              
                dataReady.value = true;
            });

            const totalFunciones = ref();
            const totalMDV = ref();
            const totalHito = ref();
            const pasoFuncion = ref(false);
            

            const detalleIdUaysen = computed(() => store.state.accion.detalleIdUaysen);

            const opciones = reporteAEditar.value.reporte_acciones;

            const cambio = async () => {                
                dataFuncionHito.value = false;
                indiceReporteAccion.value = getIndex(model.value.accion);

                await store.dispatch("accion/reqDetalleAccion", model.value.accion);
                await store.dispatch("accion/reqFuncionesPorAccion", model.value.accion);
                await store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", model.value.accion);
                await store.dispatch("producto/reqHitosReporte", model.value.accion);
                
                store.dispatch("reporte/setReporteHitosAEditar", model.value.reporte_hitos);
                store.dispatch("reporte/setReporteFuncionesAEditar", model.value.reporte_funciones);
                store.dispatch("reporte/setReporteAccionesAEditar",model.value);
                dataFuncionHito.value = true;                
            };

            const getIndex = (accion) => {
                //return reporte.value.nuevoReporte.reporte_acciones.map(object => object.accion).indexOf(accion);
                return reporte.value.aEditar.reporte_acciones.map(object => object.accion).indexOf(accion);
            };

            const siguienteReporteAccion = async (indice) => {
                model.value = reporteAEditar.value.reporte_acciones[indice];                
                cambio();
            };

            const finReporte = (data) => {
                finReporteAccion.value = data;
            };

            const guardarAvance = async () => {
                const nuevoReporte = {
                    id : reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporteAEditar.value.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "Unificado",
                    reporte_acciones: reporteAEditar.value.reporte_acciones
                };

                await store.dispatch("reporte/setReporteAEditar", nuevoReporte);

                store.dispatch("reporte/patchReporte", reporteAEditar.value);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                

                await store.dispatch("reporte/reqReportesBorradores");
                await store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };

            const cambioAtras = async () => {            
                const nuevoReporte = {
                    id : reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporteAEditar.value.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "Unificado",
                    reporte_acciones: reporteAEditar.value.reporte_acciones
                };

                await store.dispatch("reporte/setReporteAEditar", nuevoReporte);

                model.value = reporte.reporte_acciones[0];
                store.dispatch("accion/reqDetalleAccion", model.value.accion);
                store.dispatch("accion/reqFuncionesPorAccion", model.value.accion);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", model.value.accion);
                store.dispatch("producto/reqHitosReporte", model.value.accion);
                store.dispatch("reporte/setReporteHitosAEditar", model.value.reporte_hitos);
                store.dispatch("reporte/setReporteFuncionesAEditar", model.value.reporte_funciones)
                finReporteAccion.value = false;
            };
            const cambioReporteAccion = async (reporteAccion) => {                
                model.value = reporteAccion;
            };

            const guardarReporte = () => {
                const reporteAGuardar = {
                    id: reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporteAEditar.value.actor,
                    estado: "Borrador",
                    recomendacion: recomendacion.value,
                    tipo : "Unificado",
                    reporte_acciones: reporteAEditar.value.reporte_acciones
                }

                store.dispatch("reporte/patchReporte", reporteAGuardar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };

            const guardarReporteFinalizado = () => {
                const reporteAGuardar = {
                    id: reporteAEditar.value.id,
                    usuario: usuario.value.id,
                    actor: reporteAEditar.value.actor,
                    estado: "Finalizado",
                    recomendacion: recomendacion.value,
                    tipo : "Unificado",
                    reporte_acciones: reporteAEditar.value.reporte_acciones
                }

                store.dispatch("reporte/patchReporte", reporteAGuardar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };
            return {
                reporteAEditar,
                guardarReporte,
                guardarReporteFinalizado,
                indiceReporteAccion,
                detalleIdUaysen,
                actores,
                opciones,
                model,
                cambio,
                reporte,
                dataReady,
                dataFuncionHito,
                cambioReporteAccion,
                finReporte,
                siguienteReporteAccion,
                cambioAtras,
                guardarAvance,

                detalleProductos,
                fechaFormateada,
                stepPasoAccion,
                pasoFuncion,
                finReporteAccion,

                stepPasoFuncion,
    
                stepPasoHito,

                acciones,
                totalFunciones,
                totalMDV,
                totalHito,

                anio,
                mes,
                accionesAReportar,
                usuario,

                recomendacion,
                opcionesJustificacion,
                //guardarReporte,
            }
        }
    });

</script>