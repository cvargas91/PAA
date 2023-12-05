<template>    
    <q-tabs
        v-model="tab"
        @update:model-value="cambiaTab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
    >   
        <q-tab name="pregrado" label="Pregrado" />
        <q-tab name="postgrado" label="Postgrado" />
        <q-tab name="programa" label="Programas u otro material docente"/>
        <q-tab name="otrasActividades" label="Otras actividades de docencia"/>
    </q-tabs>
    
    <q-separator />

    <q-tab-panels v-model="tab" animated class="tarjetaAmarilla">
        <q-tab-panel name="pregrado" >
            <div class="text-h5">
                Docencia de Pregrado
            </div>
            <div class="text-subtitle1">
                
            </div>
            <q-separator></q-separator>            
            <TablaPrePostgrado
                :asignaturasPlanificacion="asignaturasPregrado"                
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateAsignaturas="actualizarArreglo"
                @insertAsignatura="nuevaAsignatura"
                @deleteAsignatura="quitarAsignatura"
            />
        </q-tab-panel>
        <q-tab-panel name="postgrado">
            <div class="text-h5">
                Docencia de Postgrado
            </div>
            <div class="text-subtitle1">
                
            </div>
            <q-separator></q-separator>
            <TablaPrePostgrado
                :asignaturasPlanificacion="asignaturasPostgrado"                
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateAsignaturas="actualizarArreglo"
                @insertAsignatura="nuevaAsignatura"
                @deleteAsignatura="quitarAsignatura"
            />
        </q-tab-panel>
        <q-tab-panel name="programa">
            <div class="text-h5">
                Elaboración de Programas
            </div>
            <div class="text-subtitle1">
                programación u otro material docente
            </div>
            <q-separator></q-separator>
            <TablaProgramas
                :programas="programas"
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateProgramas="actualizarArregloPrograma"
                @insertPrograma="nuevoPrograma"
                @deletePrograma="quitarPrograma"
            />
        </q-tab-panel>
        <q-tab-panel name="otrasActividades">
            <div class="text-h5">
                Otras actividades de docencia comprometidas
            </div>
            <div class="text-subtitle1">
                o proyectadas para {{periodo}} (supervisión de prácticas; direcciones de tesis; tutorías; talleres de apoyo por reforzamiento, entre otras).
            </div>
            <q-separator></q-separator>
            <TablaActividadesComprometidas
                :otrasActividades="otrasActividades"
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateActividades="actualizarArregloActividades"
                @insertActividad="nuevaActividad"
                @deleteActividad="quitarActividad"
            />
        </q-tab-panel>

    </q-tab-panels>
    
</template>
<script>    
    import { ref, toRef,computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    import TablaPrePostgrado from "./TablaPrePostgrado.vue";
    import TablaProgramas from "./TablaProgramas.vue"
    import TablaActividadesComprometidas from "./TablaActividadesComprometidas.vue";

    export default defineComponent({
        components:{
            TablaPrePostgrado,
            TablaProgramas,
            TablaActividadesComprometidas
        },
        props: {
            idPlanificacion: Number,
            cursosAcademico: Array,
            planificacionAcademico: Array,
            estadoPlanificacion: String,
            opcion: Boolean,
            periodo: String,
        },
        computed: {
            asignaturasPregrado() {
                return this.planificacionAcademica
                .filter((item) => item.tipo === "Pregrado")
                .map((item) => {
                    const asignatura = { ...item.asignatura };
                    asignatura.horas = item.cantidad_horas;
                    asignatura.idPlanificacion = item.id;
                    asignatura.rol = item.rol;
                    return asignatura;
                });
            },
            asignaturasPostgrado() {
                //Se envía a Tabla las asignaturas de Postgrado
                return this.planificacionAcademica
                .filter((item) => item.tipo === "Postgrado")
                .map((item) => {
                    const asignatura = { ...item.asignatura };
                    asignatura.horas = item.cantidad_horas;
                    asignatura.idPlanificacion = item.id;
                    asignatura.rol = item.rol;
                    return asignatura;
                });
            },
            programas () {
                return this.planificacionAcademica
                .filter((item) => item.tipo === "Programa")
                .map(item => ({ ...item }));
            },
            otrasActividades () {
                return this.planificacionAcademica
                .filter((item) => item.tipo === "OtraActividad")
                .map(item => ({ ...item }));
            }
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const detalleAccion = computed(() => store.state.accion);
            const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
            const selected = ref([]);
            const tab = ref("pregrado");
            const cambiaTab = (value, event) => {
                if(value === "postgrado" || value == "pregrado"){
                    store.dispatch("planificacion/asignatura/getCursosPorDepartamento");
                }
                tab.value = value;                
            }   
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            };
            //Manejo actividades Pre y postgrado
            const actualizarArreglo = (nuevaAsignatura) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloAsignaturas", nuevaAsignatura);
            };
            const nuevaAsignatura = (nuevaAsignatura) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloAsignaturas", nuevaAsignatura);
            };
            const quitarAsignatura = (asignaturaId) => {
                store.dispatch("planificacion/planificacionAcademica/eliminarAsignatura", asignaturaId);
            };

            //Manejo Programas docencia
            const actualizarArregloPrograma = (nuevaPrograma) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloProgramas", nuevaPrograma);
            };
            const nuevoPrograma = (nuevaPrograma) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloProgramas", nuevaPrograma);
            };
            const quitarPrograma = (programa) => {
                store.dispatch("planificacion/planificacionAcademica/eliminarPrograma", programa);
            };

            //Manejo Actividades docencia
            const actualizarArregloActividades = (nuevaActividad) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloActividadesDocencia", nuevaActividad);
            };
            const nuevaActividad = (nuevaActividad) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloActividadesDocencia", nuevaActividad);
            };
            const quitarActividad = (actividad) => {
                store.dispatch("planificacion/planificacionAcademica/eliminarActividadDocencia", actividad);
            };

            onMounted(() => {
                store.dispatch("planificacion/asignatura/getCursosPorDepartamento");                
            });
            
            const asignatura = props.cursosAcademico;
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
                    label: "Código",
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
                    name: "rol",
                    label: "Rol",
                    field: (row) => (row.rol ? row.rol : "Sin"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "horas",
                    label: "Horas estimadas",
                    field: (row) => (row.horas ? row.horas : "Sin"),
                    align: "left",
                    style: "white-space: normal",
                },
            ]
            return {
                opciones,
                detalleAccion,
                asignatura: toRef(props,"cursosAcademico"),
                periodo: toRef(props,"periodo"),
                opcion: toRef(props,"opcion"),
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                planificacionAcademica: toRef(props,"planificacionAcademico"),
                actualizarArreglo,
                nuevaAsignatura,
                quitarAsignatura,
                actualizarArregloActividades,
                actualizarArregloPrograma,
                nuevoPrograma,
                nuevaActividad,
                quitarPrograma,
                quitarActividad,
                idPlanificacion: toRef(props,"idPlanificacion"),
            };
        }        
    })
</script>