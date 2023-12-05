<template>
    <div class="q-px-sm">                        
        <br/>        
        <q-dialog v-model="envio" persistent transition-show="scale" transition-hide="scale">
            <q-card class="my-card bg-teal-2" style="width: 990px; max-width: 80vw;">
                <q-card-section horizontal>
                    <q-card-section>
                        <q-avatar color="white" text-color="cyan-8" icon="done" />
                    </q-card-section>
                <q-card-section class="text-textoAzul">
                    <div class="text-h6">
                        <b>Estado de la Planificación actualizado. Enviado a Jefe de departamento</b>
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
        <q-table
            :rows="resumenHoras"
            :columns="opciones"
            :rows-per-page-options="[6]"
            row-key="id"
            no-data-label="No hay información disponible"
            class="tablaAcciones">    
        </q-table>
        <div class="row justify-end q-gutter-sm q-ma-md" v-if="origen == 'academicx' 
            && planificacion.planificacionAcademico
            && planificacion.planificacionAcademico.length">
            <q-btn
                v-if="planificacion.planificacionAcademico[0].estado == 'Pendiente'"
                class="q-ma-sm"
                color="positive"
                label="Editar Planificación"
                @click="editarPlanificacion"
            />
            <q-btn
                class="q-ma-sm"
                color="btnContinuar"
                label="Ver Planificación"
                @click="verPlanificacion"
            />
            <q-btn
                v-if="planificacion.planificacionAcademico[0].estado == 'Pendiente'"
                class="q-ma-sm"
                label="Enviar a Jefe Departamento"                
                color="light-blue-10"
                @click="enviarPlanificacion"
            />
        </div>
        <template v-else>
            <div class="text-center" v-if="origen == 'academicx'">
                <q-spinner color="second" size="3em" />
            </div>
            </template> 
    </div>
</template>
<script>
    import { ref, computed, onMounted, defineComponent, toRef } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";

    export default defineComponent({
        props: {
            resumenHoras: Object,
            origen: String,
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
            const envio = ref(false);
            const opciones = [
                {
                    name: "actividad",
                    label: "Actividad",
                    field: (row) => {
                        if(row){
                            if (row.actividad == 'docencia')
                                return "Docencia";
                            if (row.actividad == 'investigacion')
                                return "Investigación"
                            if (row.actividad == 'vinculacion')
                                return "Vinculación con el Medio"
                            if (row.actividad == 'gestion')
                                return "Gestión Institucional"
                            if (row.actividad == 'formacion')
                                return "Actividades Formativas"
                            if (row.actividad == 'total')
                                return "Total"                    
                        }else{
                            return "";
                        }
                    },
                    align: "left",
                    sortable: true,
                },
                {
                    name: "totalHoras",
                    label: "Total horas anuales",
                    field: (row) => (row ? row.total_horas : "0"),
                    align: "right",
                    style: "white-space: normal",
                },
                {
                    name: "porcentaje",
                    label: "Porcentaje (%)",
                    field: (row) => (row ? row.porcentaje : "0"),
                    align: "right",
                    style: "white-space: normal",
                },
            ];

            const enviarPlanificacion = async () => {
                envio.value = true;
                const observacion = {
                    'planificacion' : planificacion.value.planificacionAcademico[0].id
                }
                await store.dispatch("planificacion/observaciones/workflowEnvioAJefeDpto", observacion);
                await store.dispatch("planificacion/planificacionAcademica/getMisPlanificaciones");
            };
            return {
                envio,
                opciones,
                planificacion,
                resumenHoras: toRef(props, "resumenHoras"),
                origen: toRef(props, "origen"),
                verPlanificacion: () => {
                    router.push("planificacionAcademica")
                },
                editarPlanificacion: () => {
                    store.dispatch("planificacion/planificacionAcademica/editarPlanificacion");
                    router.push("planificacionAcademica")
                },
                enviarPlanificacion,
            };
        }        
    })
</script>