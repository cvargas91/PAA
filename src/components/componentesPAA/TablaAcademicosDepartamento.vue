<template>
    <div class="q-px-sm">
        <div class="q-pa-md" v-if="selected.length">
            <q-card class="tarjetaAmarilla">
                <div class="text-h6 q-mb-md">
                    <b>{{ selected[0].username }}</b>
                </div>
                <div v-if="asignatura.cursosAcademicx">
                    <div class="text-h6 q-mb-md">
                        <b>Asignaturas dictadas para el periodo</b>
                    </div>
                    <div class="text-subtitle1">
                        Información obtenida desde ucampus.uaysen.cl:
                    </div>
                    <q-separator/>
                    <q-list bordered separator>
                        <q-item
                            v-ripple
                            v-for="(item, index) in asignatura.cursosAcademicx"
                            :key="item.codigo"
                        >   
                            <q-item-section>
                                <q-item-label>{{ item.nombre }}</q-item-label>
                                <q-item-label caption lines="1">
                                    Asignatura {{ item.semestre}}, con modalidad {{ item.modalidad }} del departamento {{ item.departamento }}.
                                </q-item-label>
                                <q-item-label caption lines="1">
                                    <b>Estado : {{ item.estado }}</b> a la planificación anual académica.
                                </q-item-label>
                            </q-item-section>
                            <q-item-section side top>
                                <q-item-label caption>{{ item.codigo }}</q-item-label>
                            </q-item-section>
                            <!-- <q-item-section>{{ item.nombre }} </q-item-section>
                            <q-item-section> </q-item-section>
                            <q-item-section>{{ item.estado }} </q-item-section> -->
                        </q-item>
                    </q-list>
                </div>
                <div v-else>
                    <div class="text-center">
                        <q-spinner color="primary" size="3em" />
                    </div>
                </div>
                <div class="row justify-end q-gutter-sm q-ma-md">
                    <!-- v-if="selected[0].estado == 'No asignado'" -->
                    <!-- <q-btn
                        
                        class="q-ma-sm"
                        color="positive"
                        label="Editar Planificación"
                        @click="submitPlanificacionEdicion"
                    /> -->
                    </div>
            </q-card>
        </div>
        
        <q-table
            v-model:selected="selected"
            :rows="planificacion.academicxs"
            :columns="opciones"
            :visible-columns="columnasVisibles"
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
            const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
            const asignatura = computed(() => store.state.planificacion.asignatura);
            const selected = ref([]);
            const seleccionaFila = async (detalles) => {
                store.dispatch("planificacion/asignatura/limpiaCursosAcademicx");
                let data = {
                    'nombre' :  detalles.rows[0].nombre,
                    'apellido' : detalles.rows[0].apellido,
                    'anio' :    props.periodo
                }
                store.dispatch("planificacion/asignatura/getCursosAcademicx",data)
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            }
            const opciones = [
                {
                    name: "id",
                    label: "Id Académic@",
                    field: (row) => (row.id ? row.id : "id"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "id",
                    label: "Id Actor",
                    field: (row) => (row.perfil ? row.perfil.actor_id : "id_actor"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "academicx",
                    label: "Académic@",
                    field: (row) => (row.nombre ? row.nombre +" "+ row.apellido : "Otro"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "email",
                    label: "Email",
                    field: (row) => (row.email ? row.email : " - "),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "unidad",
                    label: "Unidad / Departamento",
                    field: (row) => (row.perfil ? row.perfil.actor_nombre : " - "),
                    align: "left",
                    style: "white-space: normal",
                },
            ]
            const columnasVisibles = ref([
                'academicx',
                'email',
                'unidad',
            ]);
            const submitPlanificacionEdicion = () => {
                store.dispatch("planificacion/planificacionAcademica/editarPlanificacion");
                router.push("planificacionAcademica")
            }
            return {
                columnasVisibles,
                opciones,
                asignatura,
                // asignatura: toRef(props,"cursosAcademico"),
                planificacion,
                periodo: toRef(props,"periodo"),
                selected,
                seleccionaFila: seleccionaFila,
                submitPlanificacionEdicion,
            };
        }        
    })
</script>