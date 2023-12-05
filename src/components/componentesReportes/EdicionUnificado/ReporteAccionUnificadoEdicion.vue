<template>
    <q-card style="margin-right: 0; margin-left: 0; width: 66%; padding-top: 0; padding-bottom: 0pt;" bordered>
        <q-card-section horizontal style="justify-content: center;">
            <q-card-section style="margin-right: 10px; text-align: center; flex: 0.25;">
                <strong style="color: #385280; font-size: 10pt;">Estado de Ejecución:</strong>
            </q-card-section>

            <q-card-section style="margin-left: 10px; text-align: center; flex: 1;">
                <strong style="color: #385280; font-size: 10pt;">Recomendaciones:</strong>
            </q-card-section>
        </q-card-section>

        <q-card-section horizontal style="justify-content: center;" v-model="model">
            <q-card-section class="" style="background-color: #d9e2f3; margin-right: 10px; text-align: center; flex: 0.25;">
                <q-select v-model="indicadorLogro" :options="getOptions(opcionesJustificacion)">
                    <template v-slot:append>
                        {{ getDescriptionAll(indicadorLogro, opcionesJustificacion) }}
                    </template>
                    <q-tooltip>
                        {{ getDescription(indicadorLogro, opcionesJustificacion) }}
                    </q-tooltip>
                </q-select>
            </q-card-section>
            <q-card-section class="" style="background-color: #d9e2f3; margin-left: 10px; text-align: center; flex: 1;">
                <q-input
                    v-model="recomendaciones"
                    type="textarea"
                
                    autogrow
                />
            </q-card-section>
        </q-card-section>

        <q-card-section style="justify-content: center;margin-left: 0px; text-align: center; flex: 1;">
            <div class="row justify-end q-gutter-sm q-ma-md" style="margin-right:0pt">
                <BotonCancelarReporte 
                    opcion="accion"
                    @guardarAvance="guardarAvance"
                />
                <q-btn
                    v-if="validaLabelBoton()"
                    color="btnVolver"
                    @click="cambioAtras"
                    :label="labelBotonAtras"
                    class="q-ml-sm"
                />
                <q-btn
                    v-if="!validaUltimaAccion()"
                    color="btnContinuar"
                    @click="siguienteAccion"
                    label="   Siguiente Acción    "
                    class="q-ml-sm"
                />
                <BotonGuardarReporte 
                    opcion="accion"
                    @guardarAvance="guardarAvance"
                    @guardarFinalizado="guardarFinalizado"                    
                />
                <!-- <q-btn
                    v-if="validaUltimaAccion()"
                    color="btnAdjuntar"
                    @click="cambioAdelante"
                    label="   Guardar Borrador 1   "
                    class="q-ml-sm"
                />
                <q-btn
                    v-if="!validaUltimaAccion()"
                    class="q-ml-sm"
                    color="light-blue-10"
                    label="   Guardar Borrador 2 "
                    @click="guardarBorrador"
                /> -->
            </div>
        </q-card-section>
    </q-card>
</template>

<script>
    import { ref,toRef, watch ,watchEffect, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";
    import BotonGuardarReporte from "src/components/componentesReportes/BotonGuardarReporte.vue";

    export default defineComponent({        
        components:{
            BotonCancelarReporte,
            BotonGuardarReporte
        },
        props: {
            opcionesJustificacion: Array,
            reporteAccion: Object,
            indiceReporteAccion: Number,                        
        },
        watch: {        
            reporteAccion: async function (newValue, oldValue) {                
                const reporteAccion = {
                    accion: oldValue.accion,
                    estado_ejecucion: this.indicadorEstadoEjecucion,
                    justificacion_contingencia: this.justificacion,
                    reporte_justificacion_contingencia: this.reporteJustificacion,
                    indicador: this.indicador,
                    indicador_logro: this.indicadorLogro,
                    reporte_funciones: oldValue.reporte_funciones,                    
                    reporte_hitos: oldValue.reporte_hitos,
                    recomendacion: oldValue.recomendacion

                };                
                await this.$store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);
            },
        },
        methods: {
            getOptions(opcionesJustificacion) {
                return Object.keys(opcionesJustificacion)
            },
            getDescription(indicadorLogro, opcionesJustificacion){
                
                if (typeof indicadorLogro === 'undefined') {
                    return "Seleccione un Estado de Ejecución";
                } else {
                    return opcionesJustificacion[indicadorLogro];
                }
            },
            getDescriptionAll(value, value2){
                
            }
        },
        emits:["cambioReporteAccion","guardarReporte", "siguienteReporteAccion","guardarReporteFinalizado"],
        setup(props, {emit}) {
            const store = useStore();
            const router = useRouter();
            const accion = computed(() => store.state.accion);
            const accionesAReportar = computed(() => store.state.accion.aReportar.acciones);

            const reportes = computed(() => store.state.reporte);
            const nuevoReporte = computed(() => store.state.reporte);

            const opcionesEjecucion = ["Si", "No"];
            const opcionesLogro = ['No logrado','Logrado con atrasos','Logrado'];
            const recomendaciones = ref("");

            const labelBotonAtras = ref("Atras");
            const indicadorLogro = ref(props.reporteAccion.indicador_logro);
            const indicadorEstadoEjecucion = ref(props.reporteAccion.estado_ejecucion);
            const reporteJustificacion = ref(props.reporteAccion.reporte_justificacion_contingencia);
            const justificacion = ref(props.reporteAccion.justificacion_contingencia);
            const indicador = ref(props.reporteAccion.indicador);
            const accionesPendientes = ref(true);
            const idAccion = ref(props.reporteAccion.accion);

            const model = computed({
                get:() => {                    
                    idAccion.value = props.reporteAccion.accion;
                    indicadorLogro.value = props.reporteAccion.indicador_logro;
                    recomendaciones.value = props.reporteAccion.recomendacion
                }
            })

            const cambioAdelante = async () => {
                
                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                    recomendacion: recomendaciones.value
                };

                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);

                emit('guardarReporte', true);
            };

            const guardarBorrador = async () => {
                
                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                    recomendacion: recomendaciones.value
                };

                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);

                emit('guardarReporte', true);
            };



            const siguienteAccion = async () => {                                

                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                    recomendacion: recomendaciones.value
                };

                
                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);
            
                emit('siguienteReporteAccion', props.indiceReporteAccion + 1);
            };

            const cambioAtras = async () => {                                
                
                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                    recomendacion: recomendaciones.value
                }
                
                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);

                store.dispatch("accion/reqDetalleAccion", idAccion.value);
                store.dispatch("accion/reqFuncionesPorAccion", idAccion.value);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", idAccion.value);
                store.dispatch("producto/reqHitosReporte", idAccion.value);

                store.dispatch("reporte/setReporteHitosAEditar", props.reporteAccion.reporte_hitos);
                store.dispatch("reporte/setReporteFuncionesAEditar", props.reporteAccion.reporte_funciones);
                emit('cambioReporteAccion', reporteAccion);
            };

            const validaLabelBoton = () => {                
                if(props.reporteAccion.reporte_funciones.length && props.reporteAccion.reporte_hitos.length){
                    labelBotonAtras.value = "Volver a Funciones e Hitos";
                }else{
                    if(props.reporteAccion.reporte_funciones.length && !props.reporteAccion.reporte_hitos.length){
                        labelBotonAtras.value = "Volver a Funciones";
                    }else{
                        labelBotonAtras.value = "Volver a Hitos";
                    }
                }

                return true;
            };

            const validaUltimaAccion = () => {
                if(props.indiceReporteAccion === (reportes.value.aEditar.reporte_acciones.length - 1)){
                    return true;
                }else{
                    return false;
                }
            }

            const guardarAvance = async () => {                
                
                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                    recomendacion: recomendaciones.value
                };

                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);
                                
                store.dispatch("reporte/patchReporte", reportes.value.aEditar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };

            const guardarFinalizado = async () => {
                                
                const reporteAccion = {
                    accion: idAccion.value,
                    estado_ejecucion: indicadorEstadoEjecucion.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    reporte_funciones: reportes.value.reporteFuncionesAEditar,
                    reporte_hitos: reportes.value.reporteHitosAEditar,
                    indicador: indicador.value,
                    indicador_logro: indicadorLogro.value,
                    recomendacion: recomendaciones.value
                };

                await store.dispatch("reporte/actualizaReporteAcciones", reporteAccion);                

                emit('guardarReporteFinalizado', "Finalizado");
            };

            return {
                reportes,
                guardarBorrador,
                recomendaciones,
                nuevoReporte,
                labelBotonAtras,
                model,
                cambioAdelante,
                siguienteAccion,
                cambioAtras,
                validaLabelBoton,
                validaUltimaAccion,
                guardarAvance,
                guardarFinalizado,
                opcionesLogro,
                indicadorLogro,
                accionesAReportar,
                idAccion,
                accion,
                accionesPendientes,
                
                opcionesJustificacion: toRef(props,"opcionesJustificacion"),
                opcionesEjecucion,
                
                justificacion,
                indicador,
                indicadorEstadoEjecucion,

                reporteJustificacion,
                indiceReporteAccion: toRef(props, "indiceReporteAccion"),
            }
        }
    })
</script>
