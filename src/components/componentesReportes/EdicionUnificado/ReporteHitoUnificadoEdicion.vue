<template>
    <q-card 
            style="margin-right: 0; margin-left: 0; width: 66%; padding-top: 0; padding-bottom: 16pt;"            
        >
        <!-- v-if="validaReporteAccionPMI()" -->
            <!-- HABILITAR EN HITO -->
            <div class="row" style="border: solid #385280; border-width:0.5px; margin-left:2pt;margin-right:98pt" >
                <p style="color:#385280; margin-bottom:4pt;padding-top:4pt; padding-right:165pt;padding-left:5pt">
                    <b>Evaluación entrega a Medios de Verificación</b>
                </p>            
            </div> 

            <q-card-section style="justify-content: center;margin-left: 10px; text-align: center; flex: 1;">
                <strong style="color: #385280; font-size: 10pt;">Hito</strong>
            </q-card-section>
            
            <q-card-section horizontal style="justify-content: center;" class="tarjetaAmarilla">
                <q-card-section style="margin-right: 10px; text-align: right; flex: 0.25;">
                    <strong style="color: #385280; font-size: 10pt;">{{idTactica}}</strong>
                </q-card-section>
                <q-separator vertical class="separator-line"></q-separator>
                <q-card-section style="margin-left: 10px; text-align: left; flex: 1;">
                    <strong style="color: #385280; font-size: 10pt;">{{descripcionTactica}}</strong>
                </q-card-section>
            </q-card-section>

            <q-card-section horizontal style="justify-content: center;">
                <q-card-section style="margin-right: 10px; text-align: center; width: calc(50% - 10px);">
                    <strong style="color: #385280; font-size: 10pt;">MDV</strong>
                </q-card-section>
                <q-card-section style="margin-right: 10px; margin-left: 10px; text-align: center; width: calc(25% - 20px);">
                    <strong style="color: #385280; font-size: 10pt;">Logro</strong>
                </q-card-section>
                <q-card-section style="margin-left: 10px; text-align: center; width: calc(50% - 10px);">
                    <strong style="color: #385280; font-size: 10pt;">Indicador de Avance</strong>
                </q-card-section>
            </q-card-section>
            
            <q-card-section horizontal style="justify-content: center;">
                <q-card-section style="background-color: #d9e2f3; margin-right: 10px; text-align: center; width: calc(50% - 10px);">
                    <strong style="color: #385280; font-size: 10pt;">
                        <q-expansion-item
                            expand-icon-toggle
                            expand-separator
                            label="Detalle MDVs"
                            :caption="identificador"
                            v-model="model"
                        >
                            <div v-for="(hitoEnReporte) in acciones.detalleMDVAReporte" :key="hitoEnReporte.id" style="word-wrap:break-word">
                                {{identificador}}_{{idTactica}}_{{hitoEnReporte.label}}
                            </div>
                        </q-expansion-item>        
                    </strong>
                </q-card-section>
                <q-card-section style="background-color: #d9e2f3; margin-right: 10px; margin-left: 10px; text-align: center; width: calc(25% - 20px);">
                    <strong style="color: #385280; font-size: 10pt;">
                        <q-input
                            input-class="text-right"
                            v-model="porcentajeLogro"
                            borderless
                            suffix="%"
                            readonly  
                        />
                    </strong>
                </q-card-section>
                <q-card-section style="background-color: #d9e2f3; margin-left: 10px; text-align: center; width: calc(50% - 10px);">
                    <strong style="color: #385280; font-size: 10pt;">
                        <q-select
                            v-model="indicadorLogro" 
                            :options="opcionesLogro"                             
                            style="width: 100%"
                        >
                            <template v-slot:option="scope">
                                <q-item v-bind="scope.itemProps">                                
                                    <q-item-section>
                                        <q-item-label>{{ scope.opt.label }}</q-item-label>
                                        <q-item-label caption>{{ scope.opt.description }}</q-item-label>
                                    </q-item-section>
                                </q-item>
                            </template> 
                        </q-select>
                    </strong>
                </q-card-section>
            </q-card-section>
            
            <q-card-section style="justify-content: center;margin-left: 10px; text-align: center; flex: 1;">
                <strong style="color: #385280; font-size: 10pt;">Comentarios al Cumplimiento</strong>
            </q-card-section>

            <q-card-section style="background-color:#d9e2f3;justify-content: center;margin-left: 0px; text-align: center; flex: 1;">
                <q-input
                    autogrow
                    v-model="comentario_cumplimiento"
                    borderless
                    type="textarea"
                    label="Ingresar comentario al cumplimiento"
                    />
            </q-card-section>

            <q-card-section style="justify-content: center;margin-left: 0px; text-align: center; flex: 1;">
                <hr style="border: 1.5px dashed #385280; padding-top:0pt;">
            </q-card-section>

            <q-card-section style="justify-content: center;margin-left: 0px; text-align: center; flex: 1;">
                <div class="row justify-end q-gutter-sm q-ma-md" style="margin-right:0pt">
                    <BotonCancelarReporte 
                        opcion="hito"
                        @guardarAvance="guardarAvance"
                    />
                    <q-btn
                        v-if="validaPasoFuncionAtras()"
                        color="btnVolver"
                        @click="pasoAtras"
                        label=" Volver a Funciones  "
                        class="q-ml-sm"
                    />
                    <q-btn
                        v-if="validaPasoAtras()"
                        color="btnVolver"
                        @click="cambioAtras"
                        label=" Hito Anterior  "
                        class="q-ml-sm"
                    />
                    <q-btn
                        v-if="validaPasoAdelante()"
                        color="btnContinuar"
                        @click="cambioAdelante"
                        label="   Siguiente Hito   "
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
    import { ref,toRef, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { watch } from 'vue';
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";

    export default defineComponent({        
        components:{
            BotonCancelarReporte,
        },
        props: {
            reporteAccion: Object,
            identificador: String,        
        },
        watch: {        
            // reporteAccion: async function (newValue, oldValue) {                
            //     this.pasoHito = 0;

            //     if(newValue.reporte_hitos.length){
            //         this.comentario_cumplimiento = newValue.reporte_hitos[0].comentario_cumplimiento;
            //     }else{
            //         this.comentario_cumplimiento = "";
            //     }

            // },
            // mdvs: function (newValue, oldValue) {
            //     this.mdvs = newValue;
            //     //this.descripcionTactica = this.mdvs[0].label;
            // },
            // hitos: function (newValue, oldValue) {

            //     this.hitos = newValue;
            //     this.descripcionTactica = this.hitos[0].label;
            // },
        },
        setup(props) {   
            const store = useStore();
            const router = useRouter();
            const porcentaje = ref("");
            const acciones = computed(() => store.state.accion);
            const nuevoReporte = computed(() => store.state.reporte);
            const reporteHitos = computed(() => store.state.reporte);
            const mdv = ref(acciones.value.detalleAccion.mdvs);
            const hitos = ref(acciones.value.detalleAccion.hitos);
            
            const hitosIngresados = acciones.value.detalleAccion.hitos;
            const reporteAccion = computed(() => store.state.reporte);

            const indicadorLogro = ref("");
            const indicador = computed(() => indicadorLogro.value ? indicadorLogro.value.value : '')
            const opcionesLogro = [
                {
                    label: 'Logrado',
                    value: 'Logrado',
                    description: 'Hito cumplido dentro de los plazos comprometidos',                    
                },
                {
                    label: 'Logrado parcialmente',
                    value: 'Logrado parcialmente',
                    description: 'Hito no cumplido, reporta avances parciales',                    
                },
                {
                    label: 'Logrado con atrasos',
                    value: 'Logrado con atrasos',
                    description: 'Hito cumplido fuera de los plazos comprometidos',                    
                },                
                {
                    label: 'No logrado',
                    value: 'No logrado',
                    description: 'Hito no cumplido, no presenta avances dentro de los plazos comprometidos',                    
                },
            ];
            
        
            const detalleProductos = computed(() => store.state.producto.totalHitos);
                
            const comentario_cumplimiento = ref('');
            const identificador = ref(props.identificador);

            // const mdvs = ref(props.mdvs);
            // const hitos = ref(props.hitos);
            // const mdvs = toRef(props, 'mdvs');
            // const hitos = toRef(props, 'hitos');
            const descripcionTactica = ref('');
            
            const pasoHito =  ref(0);
            const arrayIdMDVReporte = ref('');
            const calculoAvance = () => {

                const detalle = {
                    idHito: hitos.value[pasoHito.value].value,
                    detalleProductos: detalleProductos.value
                };

                store.dispatch("accion/reqDetalleHitosAReporte", detalle);
                arrayIdMDVReporte.value = acciones.value.mdvsAReporte;
                
                if(arrayIdMDVReporte.value.length){
                    return 100; 
                }else{
                    return 0;
                }
            };
            const getIdTactica = () => {
                const value = pasoHito.value + 1;
                if (pasoHito.value < 10) {
                    return ("H0" + (value).toString());
                }
                else {
                    return ("H" + (value).toString());
                }
            };
            const idTactica = computed((getIdTactica));
            const id_tactica = computed((getIdTactica));

            const porcentajeLogro = computed((calculoAvance));

            const model = computed({
                get:() => {
                    mdv.value = acciones.value.detalleAccion.mdvs;
                    hitos.value = acciones.value.detalleAccion.hitos;
                    
                    if(reporteHitos.value.reporteHitosAEditar.length){
                        comentario_cumplimiento.value = reporteHitos.value.reporteHitosAEditar[0].comentario_cumplimiento;
                        indicadorLogro.value = reporteHitos.value.reporteHitosAEditar[0].indicador_logro;
                        id_tactica.value = reporteHitos.value.reporteHitosAEditar[0].id_tactica;
                    }else{
                        comentario_cumplimiento.value = "";
                        indicadorLogro.value = "";
                        id_tactica.value = getIdTactica();
                    }

                    descripcionTactica.value = hitos.value[0].label;
                }
            });
            

            const validaPasoAtras = () =>{
                if(pasoHito.value > 0){
                    return true;
                }else{
                    return false;
                }
            };

            const validaPasoAdelante = () => {
                if(pasoHito.value < acciones.value.detalleAccion.hitos.length - 1){
                    return true;
                }else{
                    return false;
                }
            };

            const validaIndicador = (indicador) => {                
                return typeof indicador === 'object' && indicador !== null ? indicador.value : indicador;
            }

            const cambioAtras = async () => {

                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: validaIndicador(indicadorLogro.value),
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);
                pasoHito.value -= 1;

                comentario_cumplimiento.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].comentario_cumplimiento;
                id_tactica.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].id_tactica;
                indicadorLogro.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].indicador_logro;
                descripcionTactica.value = hitos.value[pasoHito.value].label;

                porcentajeLogro.value = calculoAvance();
            };

            const cambioAdelante = async () => {
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: validaIndicador(indicadorLogro.value),                    
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                
                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);
                pasoHito.value += 1;

                if(pasoHito.value < (reporteHitos.value.reporteHitosAEditar.length)){
                    indicadorLogro.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].indicador_logro;
                    comentario_cumplimiento.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].comentario_cumplimiento;
                    id_tactica.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].id_tactica;
                }else{
                    indicadorLogro.value = "";
                    comentario_cumplimiento.value = "";
                    id_tactica.value = getIdTactica();
                }

                descripcionTactica.value = hitos.value[pasoHito.value].label;
                porcentajeLogro.value = calculoAvance();
            };

            const avanzaReporte = async () => {

                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: validaIndicador(indicadorLogro.value),
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);
                store.dispatch("accion/limpiaDetalleAccion");
            };

            const pasoAtras = async () => {

                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: validaIndicador(indicadorLogro.value),
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);

                store.dispatch("accion/reqFuncionesPorAccion", reporteAccion.value.reporteAccionesAEditar.accion);
            };

            const validaPasoFuncionAtras = () => {
                if ((pasoHito.value === 0) && (reporteHitos.value.reporteFuncionesAEditar.length)){
                    return true;
                }else{
                    return false;
                }
            }

            const guardarAvance = async () => {

                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: validaIndicador(indicadorLogro.value),
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);
                
                store.dispatch("reporte/patchReporte", reporteHitos.value.aEditar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };


            if (reporteHitos.value.reporteHitosAEditar.length){
                indicadorLogro.value = reporteHitos.value.reporteHitosAEditar[0].indicador_logro;
                comentario_cumplimiento.value = reporteHitos.value.reporteHitosAEditar[0].comentario;
            }

            return { 
                indicador,
                validaPasoAtras,
                validaPasoAdelante,
                pasoAtras,
                validaPasoFuncionAtras,
                cambioAtras,
                cambioAdelante,
                avanzaReporte,
                nuevoReporte,
                guardarAvance,

                idTactica,
                arrayIdMDVReporte,
                acciones,
                hitosIngresados,
                detalleProductos,
                mdv,
                hitos,

                id_tactica: toRef(props, "stepPasoHito"), 
                
                porcentajeLogro,
                porcentaje,
                pasoHito,
                model,
                indicadorLogro,
                comentario_cumplimiento,
                
                opcionesLogro,
                descripcionTactica,
                identificador,
            }
        }
    })
</script>
