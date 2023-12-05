<template>
    <div class="q-px-sm">
        <div class="q-pa-md" v-if="selected.length">
            <q-card class="tarjetaAmarilla">
                <div class="text-h6 q-mb-md">
                    <b>{{ selected[0].nombre }}</b>
                </div>
                Curso con <b>código</b> {{ selected[0].codigo }} del departamento de {{ selected[0].departamento }}. Modalidad {{ selected[0].modalidad }}
                <div v-if="selected[0].estado == 'No asignado'">
                    Sin incluir en Planificación Académica {{ periodo }}
                </div>
                <div v-else>
                    Asignatura incluida en Planificación Académica {{ periodo }}
                </div>
                <div class="row justify-end q-gutter-sm q-ma-md">                
                    <q-btn
                        
                        class="q-ma-sm"
                        color="positive"
                        label="Incluir en Planificación (Pregrado)"
                        no-caps
                        @click="submitPlanificacionEdicion"
                        :disable="planificacion.planificacionAcademico[0].estado !== 'Pendiente' || selected[0].estado !== 'No asignado'"
                    >
                        <q-tooltip v-if="planificacion.planificacionAcademico[0].estado !== 'Pendiente'"
                            class="tablaAcciones">
                            Planificación enviada a Jefe Departamento o superior
                        </q-tooltip>
                        <q-tooltip v-if="selected[0].estado !== 'No asignado'"
                            class="tablaAcciones">
                            Asignatura ya ingresada a la Planificación
                        </q-tooltip>
                    </q-btn>
                    </div>
            </q-card>
        </div>
        <q-table
            v-model:selected="selected"
            :rows="asignatura"
            :columns="opciones"
            @selection="seleccionaFila"
            selection="single"
            row-key="id"
            no-data-label="No información disponible"
            class="tablaAcciones"
        >
            <template v-slot:top-right>
                <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>
            </template>
        </q-table>
    </div>
</template>
<script>
    import { ref, toRef,computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";

    export default defineComponent({
        props: {
            cursosAcademico: Array,
            periodo: String,
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const detalleAccion = computed(() => store.state.accion);
            const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
            const selected = ref([]);
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            }
            const opciones = [
                {
                    name: "asignatura",
                    label: "Asignatura",
                    field: (row) => (row.nombre ? row.nombre : "Otro"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "codigo",
                    label: "Codigo",
                    field: (row) => (row.codigo ? row.codigo : "Cpd"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "semestre",
                    label: "Semestre",
                    field: (row) => (row.semestre ? row.semestre : "Sem"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "estado",
                    label: "Estado Asignatura",
                    field: (row) => (row.estado ? row.estado + ' en Planificación Académica' : "Sin"),
                    align: "left",
                    style: "white-space: normal",
                },   
            ]
            const submitPlanificacionEdicion = async () => {
                await store.dispatch("planificacion/planificacionAcademica/editarPlanificacion");
                if (planificacion.value.planificacionAcademicaEdicion){
                    for (let i=0; i<selected.value.length; i++){
                        const nuevaAsignatura = {
                            planificacion: planificacion.value.planificacionAcademico.id,
                            // asignatura: selected.value[i].id,
                            asignatura: {
                                'id'            :selected.value[i].id,
                                'id_ucampus'    :selected.value[i].id_ucampus,
                                'modalidad'     :selected.value[i].modalidad,
                                'nombre'        :selected.value[i].nombre,
                                'semestre'      :selected.value[i].semestre,
                                'codigo'        :selected.value[i].codigo,
                                'departamento'  :selected.value[i].departamento,
                                'estado'        :selected.value[i].estado,
                            },
                            tipo: "Pregrado",
                            semestre: "",
                            rol: "",
                            cantidad_horas: "", // Asigna las horas
                            programa: "",
                            descripcion: "",
                            observacion: "",
                        };
                        store.dispatch("planificacion/planificacionAcademica/actualizarArregloAsignaturas", nuevaAsignatura);
                    }
                }
                //store.dispatch("planificacion/planificacionAcademica/editarPlanificacion");
                router.push("planificacionAcademica")
            }
            return {
                opciones,
                detalleAccion,
                asignatura: toRef(props,"cursosAcademico"),
                periodo: toRef(props,"periodo"),
                selected,
                seleccionaFila: seleccionaFila,
                submitPlanificacionEdicion,
                planificacion,
            };
        }        
    })
</script>