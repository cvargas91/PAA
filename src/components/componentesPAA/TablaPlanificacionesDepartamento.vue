<template>
    <PopUpRechazarPlanificacion
        :periodo="periodo"
        :mostrar="popUpNuevoCurso"        
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoRechazo"
    />
    <PopUpVincularCompromisosDpto
        :periodo="periodo"
        :mostrar="popUpVincularCompromiso"        
        @update:mostrar="popUpVincularCompromiso = $event"
        @respuestaPopup="manejoVincularCompromiso"
    />
    <q-dialog v-model="envio" persistent transition-show="scale" transition-hide="scale">
        <q-card class="my-card bg-teal-2" style="width: 990px; max-width: 80vw;">
            <q-card-section horizontal>
                <q-card-section>
                    <q-avatar color="white" text-color="cyan-8" icon="done" />
                </q-card-section>
            <q-card-section class="text-textoAzul">
                <div class="text-h6">
                    <b>Estado de la Planificación actualizado. Enviado a Desarrollo académico</b>
                </div>
                Gracias por usar Colabora
            </q-card-section>
            </q-card-section> 
    
            <q-card-actions align="right" class="bg-white text-teal">
                <q-btn 
                    flat 
                    label="Volver al panel" 
                    v-close-popup
                />
            </q-card-actions>
            </q-card>
    </q-dialog>
    <div class="">
        <div class="" v-if="selected.length">
            <div ref="scrollTargetRef" class="q-pa-xs" style="max-height: 480px; overflow: auto;" v-if="selected.length">
                <q-infinite-scroll @load="onLoadRef" :offset="480" :scroll-target="scrollTargetRef">
                    <q-card class="tarjetaAmarilla" >
                        <q-card-section>
                            <div class="text-h6 q-mb-md">
                                <b>Detalle Planificación Anual Académica {{selected[0].usuario.fullname}}</b>
                            </div>
                            <template v-if="planificaciones.resumenHoras">                                
                                <TablaResumenPlanificacionAcademica
                                    style="padding-left: 3pt;"
                                    :resumenHoras="planificaciones.resumenHoras"
                                    origen="jefeDepartamento"
                                />
                                <div class="row justify-end q-gutter-sm q-ma-md">
                                    
                                    <q-btn                    
                                        class="q-ma-sm"
                                        label="Ingresar observaciones"
                                        color="btnVolver"
                                        no-caps
                                        @click="rechazarPlanificacion"
                                    />
                                    <q-btn                    
                                        class="q-ma-sm"
                                        label="Relacionar"
                                        color="primary"
                                        no-caps
                                        @click="relacionarAccion"
                                    />
                                    <q-btn
                                        class="q-ma-sm"
                                        color="btnContinuar"
                                        label="Ver Planificación"
                                        no-caps
                                        @click="verPlanificacion"
                                    />
                                    <q-btn
                                        class="q-ma-sm"
                                        label="Enviar a Desarrollo académico"
                                        color="light-blue-10"
                                        no-caps
                                        @click="enviarPlanificacion"
                                    />
                                </div>
                                
                            </template>
                        </q-card-section>
                    </q-card>
                </q-infinite-scroll>                
            </div>
        </div>
        
        <q-table
            v-if="planificaciones.planificacionesDepartamento"
            :rows="planificaciones.planificacionesDepartamento"
            :columns="opciones"
            :rows-per-page-options="[6]"
            selection="single"
            @selection="seleccionaFila"
            v-model:selected="selected"
            row-key="id"
            no-data-label="No hay información disponible"
            class="tablaAcciones">    
        </q-table>
        <!--  -->
    </div>
</template>
<script>
    import { ref, computed, onMounted, defineComponent, toRef } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";
    import InformacionBasica from "src/components/componentesPAA/InformacionBasica.vue";
    import TablaResumenPlanificacionAcademica from "src/components/componentesPAA/TablaResumenPlanificacionAcademica.vue";
    import PopUpRechazarPlanificacion from "src/components/componentesPAA/PopUpRechazarPlanificacion.vue";
    import PopUpVincularCompromisosDpto from "src/components/componentesPAA/PopUpVincularCompromisosDpto.vue";

    export default defineComponent({
        components:{
            InformacionBasica,
            TablaResumenPlanificacionAcademica,
            PopUpRechazarPlanificacion,
            PopUpVincularCompromisosDpto,
        },
        props: {
            resumenHoras: Object,
            periodo: String,
        },
        setup(props, {emit}) {
            const router = useRouter();
            const store = useStore();
            const planificaciones = computed(() => store.state.planificacion.planificacionAcademica);            
            const usuario = computed(() => store.state.usuarix.usuario);
            const selected = ref([]);
            const scrollTargetRef = ref(null);
            const popUpNuevoCurso = ref(false);
            const popUpVincularCompromiso = ref(false);
            const mostrar = ref("");
            const envio = ref(false);

            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });

                if (detalles.added) {
                    await store.dispatch(
                        "planificacion/planificacionAcademica/planificacionAcademicx", detalles.rows[0].id                        
                    );
                    await store.dispatch(
                        "planificacion/planificacionAcademica/resumenActividadesAcademico", detalles.rows[0].id)
                }
            };

            const opciones = [
                {
                    name: "academico",
                    label: "Planificación Académicx",
                    field: (row) => (row.usuario ? row.usuario.email : "email"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "total",
                    label: "Total horas anuales",
                    field: (row) => (row.total_horas ? row.total_horas : "horas"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "accion",
                    label: "Compromiso(s)/Acción",
                    field: (row) => (row.accion ? row.accion.id_uaysen : "accion"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "creado",
                    label: "Fecha de creación",
                    field: (row) => (row.creado ? row.creado : "creado"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "modificado",
                    label: "Fecha de modificación",
                    field: (row) => (row.modificado ? row.modificado : "modificado"),
                    align: "left",
                    sortable: true,
                },
            ];
            const manejoRechazo = () => {                
                popUpNuevoCurso.value = false;
                selected.value = [];
            };

            const manejoVincularCompromiso = (respuesta) => {
                popUpVincularCompromiso.value = false;
                const observacion = {
                    'usuario' : usuario.value.id,
                    'planificacion' : planificaciones.value.planificacionAcademico[0].id,
                    'observacion' : respuesta.data
                }
            };
            const enviarPlanificacion = async () => {
                console.log("Inivio encio")
                envio.value = true;
                const observacion = {
                    'planificacion' : planificaciones.value.planificacionAcademico[0].id
                }
                console.log("props , ", props.periodo)
                await store.dispatch("planificacion/observaciones/workflowEnvioADireccion", observacion);
                await store.dispatch("planificacion/planificacionAcademica/planificacionesDepartamento", props.periodo)
                selected.value = [];
            };
            return {
                envio,
                enviarPlanificacion,
                manejoRechazo,
                manejoVincularCompromiso,
                mostrar,
                opciones,
                popUpNuevoCurso,
                popUpVincularCompromiso,
                scrollTargetRef,
                selected,
                seleccionaFila: seleccionaFila,
                planificaciones,
                resumenHoras: toRef(props, "resumenHoras"),
                periodo: toRef(props, "periodo"),
                verPlanificacion: () => {
                    router.push("planificacionAcademica")
                },
                rechazarPlanificacion: () => {
                    //router.push("rechazarPlanificacion");
                    popUpNuevoCurso.value = true;
                },
                relacionarAccion: () => {
                    popUpVincularCompromiso.value = true;
                    //router.push("rechazarPlanificacion");
                    //popUpNuevoCurso.value = true;
                },
            };
        }        
    })
</script>