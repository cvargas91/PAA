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
        <q-tab name="proyectos" label="Proyectos de investigación" />
        <q-tab name="publicaciones" label="Publicaciones" />
        <q-tab name="eventos" label="Participación en eventos académicos"/>        
    </q-tabs>
    
    <q-separator />

    <q-tab-panels v-model="tab" animated class="tarjetaAmarilla">
        <q-tab-panel name="proyectos" class="tarjetaAmarilla">
            <div class="text-h4">
                Proyectos de investigación a elaborar
            </div>
            <div class="text-subtitle1">
                (a presentar a concursos internos y/o externos) y a ejecutar en el periodo 
            </div>
            <q-separator></q-separator>
            <TablaProyectos
                :proyectos="proyectos"
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateProyectos="actualizarArregloInvestigaciones"
                @insertProyecto="nuevaInvestigacion"
                @deleteProyecto="quitarInvestigacion"
            />
        </q-tab-panel>
        <q-tab-panel name="publicaciones">
            <div class="text-h4">
                Publicaciones a elaborar y enviar
            </div>
            <div class="text-subtitle1">
                Indique nombre Revista e Indexación.
            </div>
            <q-separator></q-separator>

            <TablaPublicaciones
                :publicaciones="publicaciones"
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updatePublicaciones="actualizarArregloInvestigaciones"
                @insertPublicacion="nuevaInvestigacion"
                @deletePublicacion="quitarInvestigacion"
            />
        </q-tab-panel>
        <q-tab-panel name="eventos">
            <div class="text-h4">
                Participación en eventos académicos y otros
            </div>
            <div class="text-subtitle1">
                congresos, asociaciones de investigación, comités editoriales de revistas y otras actividades del ámbito de la investigación, 
                comprometidas o proyectadas para
            </div>
            <q-separator></q-separator>
            <TablaEventos
                :eventos="eventos"
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateEventos="actualizarArregloInvestigaciones"
                @insertEvento="nuevaInvestigacion"
                @deleteEvento="quitarInvestigacion"
            />
        </q-tab-panel>        

    </q-tab-panels>
    
</template>
<script>    
    import { ref, toRef,computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    import TablaEventos from "./TablaEventos.vue";
    import TablaProyectos from "./TablaProyectos.vue"
    import TablaPublicaciones from "./TablaPublicaciones.vue";

    export default defineComponent({
        components:{
            TablaEventos,
            TablaProyectos,
            TablaPublicaciones,
        },
        props: {
            idPlanificacion: Number,
            investigaciones: Array,
            estadoPlanificacion: String,
            opcion: Boolean,
        },
        computed: {
            proyectos () {
                return this.investigaciones
                    .filter((item) => item.tipo === "Proyecto")
                    .map((item) => ({...item}));
            },
            publicaciones () {
                return this.investigaciones
                .filter((item) => item.tipo === "Publicacion")
                .map((item) => ({...item}));
            },
            eventos () {
                return this.investigaciones
                .filter((item) => item.tipo === "Evento")
                .map((item) => ({...item}));
            },
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const detalleAccion = computed(() => store.state.accion);
            const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
            const selected = ref([]);
            const tab = ref("proyectos")
            const cambiaTab = (value, event) => {                
                tab.value = value;                
                //innerTab.value = "borrador";
            }   
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            };
            const actualizarArregloInvestigaciones = (nuevaInvestigacion) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloInvestigaciones", nuevaInvestigacion);
            };
            const nuevaInvestigacion = (nuevaInvestigacion) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloInvestigaciones", nuevaInvestigacion);
            };
            const quitarInvestigacion = (investigacionId) => {
                store.dispatch("planificacion/planificacionAcademica/eliminarInvestigacion", investigacionId);
            };           
            
            return {                
                detalleAccion,                
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                investigaciones: toRef(props,"investigaciones"),
                opcion: toRef(props,"opcion"),
                idPlanificacion: toRef(props,"idPlanificacion"),
                actualizarArregloInvestigaciones,
                nuevaInvestigacion,
                quitarInvestigacion,
            };
        }        
    })
</script>