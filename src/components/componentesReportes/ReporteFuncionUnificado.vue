<template>
    <q-card 
            style="margin-right: 0; margin-left: 0; width: 66%; padding-top: 15pt; padding-bottom: 16pt;"            
        >
        <!-- v-if="validaReporteAccionPMI()" -->
            <div class="row" style="border: solid #385280; border-width:0.5px; margin-left:2pt;margin-right:98pt" >
                <p style="color:#385280; margin-bottom:4pt;padding-top:4pt; padding-right:165pt;padding-left:5pt">
                    <b>Evaluación entrega a Medios de Verificación</b>
                </p>            
            </div>  

            <q-card-section style="justify-content: center;margin-left: 10px; text-align: center; flex: 1;">
                <strong style="color: #385280; font-size: 10pt;">Función</strong>
            </q-card-section>
            
            <q-card-section horizontal style="justify-content: center;" class="tarjetaAmarilla">
                <q-card-section style="margin-right: 10px; text-align: right; flex: 0.25;" v-model="model">
                    <strong style="color: #385280; font-size: 10pt;">{{idTactica}}</strong>
                </q-card-section>
                <q-separator vertical class="separator-line"></q-separator>
                <q-card-section style="margin-left: 10px; text-align: left; flex: 1;">
                    <strong style="color: #385280; font-size: 10pt;">{{descripcionTactica}}</strong>
                </q-card-section>
            </q-card-section>

            <q-card-section horizontal style="justify-content: center;">
                <q-card-section style="margin-right: 10px; text-align: center; flex: 1;">
                    <strong style="color: #385280; font-size: 10pt;">MDV</strong>
                </q-card-section>

                <q-card-section style="margin-left: 10px; text-align: center; flex: 1;">
                    <strong style="color: #385280; font-size: 10pt;">Indicador de Avance</strong>
                </q-card-section>
            </q-card-section>

            <q-card-section horizontal style="justify-content: center;">
                <q-card-section class="" style="background-color:#d9e2f3; margin-right: 10px; text-align: center; flex: 1;">
                    <q-expansion-item expand-icon-toggle expand-separator label="Detalle MDVs" :caption="identificador">
                        <div v-for="(indicador) in funciones[pasoFuncion].indicador_set" :key="indicador.id">
                            {{identificador}}_{{idTactica}}_{{indicador.nombreVerificador}}
                        </div>                            
                    </q-expansion-item>
                </q-card-section>
                <q-card-section class="" style="background-color:#d9e2f3; margin-left: 10px; text-align: center; flex: 1;">
                    <q-input
                        :label="labelMetaAvance"
                        input-class="text-right"
                        v-model="indicadorAvance"    
                        borderless
                        suffix="%"
                        readonly
                    />
                </q-card-section>
            </q-card-section>



            <q-card-section style="justify-content: center;margin-left: 10px; text-align: center; flex: 1;">
                <strong style="color: #385280; font-size: 10pt;">Comentarios al Cumplimiento</strong>
            </q-card-section>

            <q-card-section style="background-color:#d9e2f3;justify-content: center;margin-left: 0px; text-align: center; flex: 1;">
                <q-input                                
                                v-model="comentario_cumplimiento"
                                borderless
                                type="textarea"
                                label="Ingresar comentario al cumplimiento"
                                autogrow
                            />
            </q-card-section>

            <q-card-section style="justify-content: center;margin-left: 0px; text-align: center; flex: 1;">
                <hr style="border: 1.5px dashed #385280; padding-top:0pt;">
            </q-card-section>

            <q-card-section style="justify-content: center;margin-left: 10px; text-align: center; flex: 1;">
                <div class="row justify-end q-gutter-sm q-ma-md">
                    <BotonCancelarReporte
                        opcion="funcion"
                        @guardarAvance="guardarAvance" 
                    />
                    <q-btn
                        v-if="validaPasoAtras()"
                        color="btnVolver"
                        @click="cambioAtras"
                        label=" Función Anterior  "
                        class="q-ml-sm"
                    />
                    <q-btn
                        v-if="validaPasoAdelante()"
                        color="btnContinuar"
                        @click="cambioAdelante"
                        label="   Siguiente Función   "
                        class="q-ml-sm"
                    />
                    <q-btn
                        v-if="!validaPasoAdelante()"
                        color="btnContinuar"
                        @click="avanzaReporte"
                        label="   Siguiente   "
                        class="q-ml-sm"
                    />
                </div>
            </q-card-section>

            
        </q-card>
</template>

<script>
    import { ref,toRef,watch, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";

    export default defineComponent({
    components:{
        BotonCancelarReporte,
    },
    props: {
        identificador: String,
        funciones: Array,
        reporteAccion: Object,
    },
    watch: {        
            reporteAccion: async function (newValue, oldValue) {
                this.pasoFuncion = 0;

                if(newValue.reporte_funciones.length){
                    this.comentario_cumplimiento = newValue.reporte_funciones[0].comentario_cumplimiento;                    
                }else{
                    this.comentario_cumplimiento = "";
                }
            },
            funciones: function (newValue, oldValue) {                
                this.funciones = newValue;
                this.descripcionTactica = this.funciones[0].nombre;                
            },
    },
    emits: ["cambioFuncion"],
    setup(props, { emit }) {
        const store = useStore();
        const router = useRouter();
        const nuevoReporte = computed(() => store.state.reporte);
        const acciones = computed(() => store.state.accion);
    
        const funciones = ref(props.funciones);
        const descripcionTactica = ref(funciones.value[0].nombre);
        

        const meta = ref();
        const avance = ref();
        
        const id_tactica = ref();
        
        const entregas = computed(() => store.state.verificador);
        const verificador = ref("");
        const comentario_cumplimiento = ref("");
        
        const pasoFuncion = ref(0);
        
        const getIdTactica = () => {
            const value = pasoFuncion.value + 1;
            if (pasoFuncion.value < 10) {
                return ("F0" + (value).toString());
            }
            else {
                return ("F" + (value).toString());
            }
        };

        const calculoAvance = () => {
            var auxiliarIndicador;
            if(funciones.value[pasoFuncion.value].indicador_set.length);
                auxiliarIndicador = funciones.value[pasoFuncion.value].indicador_set[0].id;

            store.dispatch("verificador/reqVerificadorPorIndicador", auxiliarIndicador);
            store.dispatch("reporte/reqTotalMetasPorFuncion", funciones.value[pasoFuncion.value].indicador_set[0].funcion);

            let metaFuncion = (computed(() => store.state.reporte.total_meta)).value;
            let avanceFuncion = (computed(() => store.state.verificador.avance)).value;
            
            if(avanceFuncion){
                labelMetaAvance.value = "Meta (" + metaFuncion + ") / Avance ("+ avanceFuncion + ")";
                return (Math.floor((avanceFuncion/metaFuncion)*100));
            }else {
                labelMetaAvance.value = "Meta (" + metaFuncion + ") / Avance ("+ 0 + ")";
                return (Math.floor((0/metaFuncion)*100));
            }
        };

        const indicadorAvance = computed((calculoAvance));
        const idTactica = computed((getIdTactica));
        const labelMetaAvance = ref("");
        const mostrar = ref("");
        //const indicadores = ref(funciones.value[0]);

        const model = computed({
            get: () => {
                funciones.value = props.funciones;
            }            
        });
    

        const validaPasoAtras = () =>{
            if(pasoFuncion.value > 0){
                return true;
            }else{
                return false;
            }
        };
        const validaPasoAdelante = () => {
            if(pasoFuncion.value < acciones.value.funciones.length-1){
                return true;
            }else{
                return false;
            }
        };

        const cambioAtras = async () => {
            

            const reporteFuncion = {
                id_tactica : idTactica.value,
                funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                indicador : indicadorAvance.value,
                comentario_cumplimiento : comentario_cumplimiento.value
            };

            
            await store.dispatch("reporte/actualizaNuevoReporteFuncion", reporteFuncion);
            pasoFuncion.value -= 1;

            if(nuevoReporte.value.nuevoReporteFunciones.length){
                comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteFunciones[pasoFuncion.value].comentario_cumplimiento;
                idTactica.value = nuevoReporte.value.nuevoReporteFunciones[pasoFuncion.value].id_tactica;
            }else{
                comentario_cumplimiento.value = "";    
                idTactica.value = getIdTactica();
            }
            
            descripcionTactica.value = funciones.value[pasoFuncion.value].nombre;
            indicadorAvance.value = calculoAvance();
        };

        const cambioAdelante = async () => {
            
            const reporteFuncion = {
                id_tactica : idTactica.value,
                funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                indicador : indicadorAvance.value,
                comentario_cumplimiento : comentario_cumplimiento.value
            };

            
            
            await store.dispatch("reporte/actualizaNuevoReporteFuncion", reporteFuncion);
            pasoFuncion.value += 1;

            if(pasoFuncion.value < (nuevoReporte.value.nuevoReporteFunciones.length)){
                comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteFunciones[pasoFuncion.value].comentario_cumplimiento;
                idTactica.value = nuevoReporte.value.nuevoReporteFunciones[pasoFuncion.value].id_tactica;
            }else{
                comentario_cumplimiento.value = "";    
                idTactica.value = getIdTactica();
            }
            
            descripcionTactica.value = funciones.value[pasoFuncion.value].nombre;
            indicadorAvance.value = calculoAvance();
        };

        const avanzaReporte = async () => {
                
            const reporteFuncion = {
                id_tactica : idTactica.value,
                funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                indicador : indicadorAvance.value,
                comentario_cumplimiento : comentario_cumplimiento.value
            };

            await store.dispatch("reporte/actualizaNuevoReporteFuncion", reporteFuncion);
            store.dispatch("accion/limpiaFunciones");
        };

        const guardarAvance = async () => {
            
            
            const reporteFuncion = {
                id_tactica : idTactica.value,
                funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                indicador : indicadorAvance.value,
                comentario_cumplimiento : comentario_cumplimiento.value
            };

            await store.dispatch("reporte/actualizaNuevoReporteFuncion", reporteFuncion);

            store.dispatch("reporte/postReporte", nuevoReporte.value.nuevoReporte);
            store.dispatch("reporte/limpiaReporteFunciones");
            store.dispatch("reporte/limpiaReporteHitos");
            store.dispatch("reporte/limpiaReporteAccion");
                

            store.dispatch("reporte/reqReportesBorradores");
            store.dispatch("reporte/reqReportesUpci");

            router.push("panelReportesUpci");
        };


        if(nuevoReporte.value.nuevoReporteFunciones.length){
            comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteFunciones[0].comentario_cumplimiento;            
        }


        return {
            validaPasoAtras,
            validaPasoAdelante,
            cambioAtras,
            cambioAdelante,
            avanzaReporte,
            funciones,
            guardarAvance,
            //getIdTactica,
            
            idTactica,
            meta: computed(() => store.state.reporte.total_meta),
            avance: computed(() => store.state.verificador.avance),
            labelMetaAvance,
            indicadorAvance,
            entregas,
            
            pasoFuncion,
            nuevoReporte,
            
            comentario_cumplimiento,
            descripcionTactica,
            id_tactica,
            
            identificador: toRef(props, "identificador"),
            model,
            mostrar,
            acciones,
        };
    },
})
</script>