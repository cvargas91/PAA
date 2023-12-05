<template>    
    <q-tabs
        v-model="tab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
    >   
        <q-tab name="actividades" label="Actividades de vinculación con el medio" />
    </q-tabs>
    
    <q-separator />

    <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="actividades" class="tarjetaAmarilla">                        
            <div class="text-h4">
                Proyectos, cursos u otras actividades de vinculación con el medio 
            </div>
            <div class="text-subtitle1">
                aprobados o programados
            </div>
            <q-separator></q-separator>                                              
            <TablaVinculacionConElMedio
                :vinculacionCEMedio="arregloVinculacionCEMedio"                
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateVinculaciones="actualizarArregloVinculacion"
                @insertVinculacion="nuevaActividadVinculacion"
                @deleteVinculacion="quitarActividadVinculacion"

            />  
        </q-tab-panel>
    </q-tab-panels>
    
</template>
<script>    
    import { ref, toRef,computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    import TablaVinculacionConElMedio from "./TablaVinculacionConElMedio.vue";    

    export default defineComponent({
        components:{
            TablaVinculacionConElMedio,            
        },
        props: {
            idPlanificacion: Number,
            vinculacionCEMedio: Array,
            estadoPlanificacion: String,
            opcion: Boolean,
        },
        computed: {
            arregloVinculacionCEMedio() {
                return this.vinculacionCEMedio
                .map((item) => ({...item}));
            },
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const detalleAccion = computed(() => store.state.accion);
            const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
            const selected = ref([]);
            const tab = ref("actividades")
            const cambiaTab = (value, event) => {                
                tab.value = value;
                //innerTab.value = "borrador";
            }   
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            };
            const actualizarArregloVinculacion = (nuevaActividadVinculacion) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloVinculacion", nuevaActividadVinculacion);
            };
            const nuevaActividadVinculacion = (nuevaActividadVinculacion) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloVinculacion", nuevaActividadVinculacion);
            };
            const quitarActividadVinculacion = (vinculacionId) => {                
                store.dispatch("planificacion/planificacionAcademica/eliminarActividadVinculacion", vinculacionId);
            };                      
            return {
                actualizarArregloVinculacion,
                quitarActividadVinculacion,
                nuevaActividadVinculacion,
                detalleAccion,                
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                vinculacionCEMedio: toRef(props,"vinculacionCEMedio"),
                idPlanificacion: toRef(props,"idPlanificacion"),
                opcion: toRef(props,"opcion"),
            };
        }        
    })
</script>