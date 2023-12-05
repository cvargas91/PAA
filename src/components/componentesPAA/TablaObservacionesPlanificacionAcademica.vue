<template>
    <div class="q-px-sm">
        <q-table
            v-if="observaciones.observacionesASubsanar"
            :rows="observaciones.observacionesASubsanar"
            :columns="opciones"
            row-key="id"
            no-data-label="No hay observaciones"
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
        
        <div class="text-center" v-else>
                <q-spinner color="primary" size="3em" />
            </div>        
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
        </div>
    </div>
</template>
<script>
    import { ref, toRef, computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";

    export default defineComponent({
        props: {
            acciones: Array,
            referencia: String,
            origen: String,
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const detalleAccion = computed(() => store.state.accion);
            const usuario = computed(() => store.state.usuarix.usuario);
            const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
            const observaciones = computed(() => store.state.planificacion.observaciones)
            const opciones = [
                {
                    name: "observacion",
                    label: "Observación",
                    field: (row) => (row.observacion ? row.observacion : ""),
                    align: "left",
                    sortable: true,
                    style: "white-space: normal; max-width: 250px; word-wrap: break-word;",
                },
                {
                    name: "autor",
                    label: "Autor",
                    field: (row) => (row.usuario ? row.usuario.email : ""),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "fecha",
                    label: "Fecha",
                    field: (row) => (row.creado ? row.creado : ""),
                    align: "left",
                    style: "white-space: normal",
                },
            ]
            return {
                opciones,
                detalleAccion,
                observaciones,
                usuario,
                origen: toRef(props, "origen"),
                planificacion,
                editarPlanificacion: () => {
                    store.dispatch("planificacion/planificacionAcademica/editarPlanificacion");
                    router.push("planificacionAcademica")
                },
            };
        }        
    })
</script>