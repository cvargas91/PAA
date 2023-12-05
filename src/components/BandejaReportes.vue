<template>
    <PopupGenerarReporte
        :mostrar="mostrarPopupGenerarReporte"
        @update:mostrar="mostrarPopupGenerarReporte = $event"
        @respuestaPopup="mostrarPopupGenerarReporte"
    />    
    <div class="q-px-sm"> 
        <!-- <q-select            
            filled                
            :options="tipoReportes(reportes)"
            label="Tipo de Reporte"
            color="teal"                      
            option-label="optionLabel"
            use-chips                    
            :model-value="tipoReporte"
            @update:model-value="cambio"
            v-if="origen != 'PMI'"
        >  -->
        <q-select  v-if="origen != 'PMI'"
            filled                
            :options="options"
            label="Tipo de Reporte"
            color="teal"                      
            option-label="optionLabel"            
            :model-value="tipoReporte"
            @update:model-value="cambio"            
            @filter="filterFn"
            @filter-abort="abortFilterFn"
        > 
        <!--:model-value="actor"
            @update:model-value="cambio"  -->

            <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps">
                
                    <q-item-section>
                        <q-item-label>{{ scope.opt.label }}</q-item-label>                        
                    </q-item-section>

                </q-item>
            </template> 
        </q-select>      

        <q-separator class="q-mt-lg q-mb-lg" />  

        <q-card
            class="tarjetaAmarilla"
        >        
            <TablaReportes v-if="listaReportes"
                :reportes="listaReportes"
                :reporteSeleccionado="accionesSeleccionadas"
                :opcion="true"
                :tipoReporte="tipoReporte"
                @cambio-seleccion="actualizarSeleccion"
            /> 
        </q-card>       
        

        <TablaReportes v-if="origen == 'PMI'"
            :reportes="reportes['PMI']"
            :reporteSeleccionado="accionesSeleccionadas"
            :opcion="true"
            :tipoReporte="tipoReporte"
            @cambio-seleccion="actualizarSeleccion"
        />

        <div class="q-pa-md" v-if="accionesSeleccionadas.length">
            <div class="row justify-end q-gutter-sm q-ma-md">
                <q-btn
                    class="q-ma-sm"
                    color="btnCancelar"
                    label="   Cancelar   "
                    @click="accionesSeleccionadas = []"
                />
                <q-btn
                    v-if="!validaEstado(tipo)"
                    class="q-ma-sm"
                    color="positive"
                    label="   Editar    "                
                    @click="accionBotonEdicion"
                />
                <q-btn
                    v-if="validaEstado(tipo)"
                    class="q-ma-sm"
                    label="   Marcar como Enviado    "                
                    color="secondary"
                    @click="accionEnviarReporte"
                />
                <q-btn
                    v-if="accionesSeleccionadas[0].tipo == 'Unificado' && accionesSeleccionadas[0].estado == 'Borrador'"
                    class="q-ma-sm"
                    label="   Marcar como Finalizado    "                
                    color="secondary"
                    @click="accionFinalizarUnificado"
                />
                <q-btn
                    v-if="validaEstado(tipo) && accionesSeleccionadas.length < 2"
                    class="q-ma-sm"
                    label="   Descargar    "                
                    color="light-blue-10"
                    @click="accionBotonGeneracion"
                />                
                <q-btn
                    v-if="accionesSeleccionadas[0].tipo == 'Unificado' && accionesSeleccionadas.length > 1"
                    class="q-ma-sm"
                    label="   Unificar    "                
                    color="light-blue-10"
                    @click="accionBotonUnificado"
                />
                <!-- @click="unificarReportes"  -->
            </div>
        </div>
    </div>
    
</template>

<script>
import { ref, toRef,computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

import PopupGenerarReporte from "src/components/componentesReportes/PopupGenerarReporte.vue";
import TablaReportes from "src/components/componentesReportes/TablaReportes.vue";
import reporte from "src/store/reporte";

export default defineComponent({
    components:{
        PopupGenerarReporte,
        TablaReportes
    },
    props: {        
        reportes: Object,
        tipo: String,
        origen: String,
    },
    methods: {
        validaEstado (tipo) {            
            if (tipo == "finalizado"){
                return true;
            }else {
                return false
            }
        },
        tipoReportes (reportes) {
            const options = [];

            for (const key in reportes) {
                if (reportes.hasOwnProperty(key)) {
                    let optionLabel;

                    if (key === 'POA') {
                        optionLabel = 'Reportes POA 2022';
                    } else if (key === 'Unificado') {
                        optionLabel = 'Reportes Unificados';
                    } else {
                        optionLabel = 'Otros';
                    }

                    const option = {
                        value: key,
                        label: optionLabel,
                        reportes: reportes[key] // Lista de reportes asociados a la clave
                    };

                    options.push(option);
                }
            }
            return options;
        },
        actualizarSeleccion(nuevaSeleccion) {
            this.accionesSeleccionadas = nuevaSeleccion;
        },
    },
    setup(props) {
        const store = useStore();        
        const router = useRouter();
        const accionesSeleccionadas = ref([]);
        const actores = computed(() => store.state.actor.actores);
        const tipoReporte = ref(null);
        const listaReportes = ref(null);
        const seRenderea = ref(false);
        const seRendereaUnificado = ref(false);
        const reportes = computed({
            get:() => props.reportes
        });
        const options = ref([]);
        const tipo = computed({
            get:() => props.tipo
        })
        const mostrarPopupGenerarReporte = ref(false);
        onMounted(()=> {            
            store.dispatch("accion/reqAccionesPorRolResponsable", 0);
            store.dispatch("accion/reqAccionesPorRolResponsablePMI", 0);
        });
        
        if (tipo == "finalizado"){
            seRenderea.value = true;
        }

        const cambio = (value, event) => {               
            tipoReporte.value = value.label;
            listaReportes.value = value.reportes;
        };
        const getValor = (actor) => {
            let detalleActor = actores.value.filter(elemento => elemento.id === actor).map(detalle => detalle.id_uaysen);
            return (detalleActor);
        };
        const getValorDireccion = (actor) => {            
            let detalleActor = actores.value.filter(elemento => elemento.id === actor).map(detalle => detalle.dependencia.id_uaysen);
            return (detalleActor);
        };
        return {
            options,
            seRendereaUnificado,
            listaReportes,
            cambio,
            tipoReporte,
            mostrarPopupGenerarReporte,
            filter: ref(''),
            getValor,
            getValorDireccion,
            actores,
            accionesSeleccionadas,
            reportes,
            seRenderea,
            origen: toRef(props, "origen"),
            accionBotonEdicion: async () => {
                const tipo = accionesSeleccionadas.value[0].tipo;
                const actor = accionesSeleccionadas.value[0].actor;

                switch (tipo) {
                    case "POA":
                        await store.dispatch("accion/reqAccionesAReporte", actor);
                        break;  
                    case "Unificado":
                        let rolPeriodo = {
                            'id_actor' : actor,
                            'anio'     : 'None'
                        }
                        await store.dispatch("accion/reqAccionesAReporteUnificado", rolPeriodo);
                        break;  
                    case "PMI":
                        await store.dispatch("accion/reqAccionesAReportePMI", actor);
                        break;
                }


                await store.dispatch("accion/reqDetalleAccion", accionesSeleccionadas.value[0].reporte_acciones[0].accion);
                store.dispatch("accion/reqFuncionesPorAccion", accionesSeleccionadas.value[0].reporte_acciones[0].accion);
                store.dispatch("accion/reqMdvFuncionesEHitosPorAccion", accionesSeleccionadas.value[0].reporte_acciones[0].accion);
                store.dispatch("producto/reqHitosReporte", accionesSeleccionadas.value[0].reporte_acciones[0].accion);
                
                store.dispatch("reporte/setReporteAEditar", accionesSeleccionadas.value[0]);
                store.dispatch("reporte/setReporteHitosAEditar", accionesSeleccionadas.value[0].reporte_acciones[0].reporte_hitos);
                store.dispatch("reporte/setReporteFuncionesAEditar", accionesSeleccionadas.value[0].reporte_acciones[0].reporte_funciones)
                
                if(accionesSeleccionadas.value[0].tipo === "POA"){
                    router.push("reporteUpciEdicion");
                }else{
                    if(accionesSeleccionadas.value[0].tipo === "PMI"){
                        router.push("reporteUpciEdicionPMI");
                    }else{
                        router.push("reporteUpciUnificadoEdicion");
                    }                    
                }
            },
            accionBotonGeneracion: async () => {
                mostrarPopupGenerarReporte.value = true;
                let getActor = getValor(accionesSeleccionadas.value[0].actor);
                getActor.push(accionesSeleccionadas.value[0].modificado.substring(0, 10));

                getActor.push(accionesSeleccionadas.value[0].id);
                
                if(accionesSeleccionadas.value[0].tipo === "POA"){
                    await store.dispatch("reporte/generaReporte", getActor);
                }else{
                    if(accionesSeleccionadas.value[0].tipo === "PMI"){
                        await store.dispatch("reporte/generaReportePMI", getActor);
                    }else{
                        await store.dispatch("reporte/generaReporteUnificadoUnidad", getActor);
                    }
                    
                }
                
                accionesSeleccionadas.value=[];

                mostrarPopupGenerarReporte.value = false;
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");
                router.push("panelReportesUpci");
            },

            accionBotonUnificado: async () => {
                mostrarPopupGenerarReporte.value = true;

                let datosReportesUnificar = {};                            

                datosReportesUnificar['direccion'] = getValorDireccion(accionesSeleccionadas.value[0].actor)[0];
                datosReportesUnificar['reportes'] = accionesSeleccionadas.value.map(reporte => reporte.id);
                                                                            
                await store.dispatch("reporte/generaReporteUnificado", datosReportesUnificar);                                
                
                accionesSeleccionadas.value=[];

                mostrarPopupGenerarReporte.value = false;
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");
                router.push("panelReportesUpci");
            },

            accionEnviarReporte: async () => {            
                mostrarPopupGenerarReporte.value = true;                

                const reporteAGuardar = {
                    id: accionesSeleccionadas.value[0].id,
                    usuario: accionesSeleccionadas.value[0].usuario,
                    actor: accionesSeleccionadas.value[0].actor,
                    estado: "Finalizado",
                    enviado: true,
                    recomendacion: accionesSeleccionadas.value[0].recomendacion,
                    tipo : accionesSeleccionadas.value[0].tipo,
                    reporte_acciones: accionesSeleccionadas.value[0].reporte_acciones
                }
                

                await store.dispatch("reporte/patchReporte", reporteAGuardar);            
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");
                accionesSeleccionadas.value=[];

                mostrarPopupGenerarReporte.value = false;
                router.push("panelReportesUpci");
                
            },
            accionFinalizarUnificado: async () => {            
                mostrarPopupGenerarReporte.value = true;                

                const reporteAGuardar = {
                    id: accionesSeleccionadas.value[0].id,
                    usuario: accionesSeleccionadas.value[0].usuario,
                    actor: accionesSeleccionadas.value[0].actor,
                    estado: "Finalizado",
                    enviado: false,
                    recomendacion: accionesSeleccionadas.value[0].recomendacion,
                    tipo : accionesSeleccionadas.value[0].tipo,
                    reporte_acciones: accionesSeleccionadas.value[0].reporte_acciones
                }
                

                await store.dispatch("reporte/patchReporte", reporteAGuardar);            
                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");
                accionesSeleccionadas.value=[];

                mostrarPopupGenerarReporte.value = false;
                router.push("panelReportesUpci");
                
            },
            filterFn (val, update, abort) {
                // if (options.value !== null) {
                if (Array.isArray(options.value) && options.value.length > 0) {
                    // already loaded
                    update()
                    return
                }

                setTimeout(() => {
                    update(() => {                        
                        for (const key in reportes.value) {
                            if (reportes.value.hasOwnProperty(key)) {
                                let optionLabel;

                                if (key === 'POA') {
                                    optionLabel = 'Reportes POA 2022';
                                } else if (key === 'Unificado') {
                                    optionLabel = 'Reportes Unificados';
                                } else {
                                    optionLabel = 'Otros';
                                }

                                const option = {
                                    value: key,
                                    label: optionLabel,
                                    reportes: reportes.value[key] // Lista de reportes asociados a la clave
                                };

                                options.value.push(option);
                            }
                        }
                    })
                }, 950)
            },

            abortFilterFn () {
                console.log('delayed filter aborted')
            }

        };
    }
    
});
</script>