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
        <q-tab name="actividades" label="Actividades de gestión institucional" />        
    </q-tabs>
    
    <q-separator />

    <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="actividades" class="tarjetaAmarilla">                        
            <div class="text-h4">
                Actividades de gestión o de construcción institucional
            </div>
            <div class="text-subtitle1">
                comprometidas o proyectadas para el periodo.
            </div>
            <q-separator></q-separator>
            <TablaActividadesGestionInstitucional
                :gestiones="arregloGestiones"                
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateGestiones="actualizarArregloGestiones"
                @insertGestion="nuevaGestion"
                @deleteGestion="quitarGestion"
            />
        </q-tab-panel>
    </q-tab-panels>
    
</template>
<script>    
    import { ref, toRef,computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    import TablaActividadesGestionInstitucional from "./TablaActividadesGestionInstitucional.vue";    

    export default defineComponent({
        components:{
            TablaActividadesGestionInstitucional,            
        },
        props: {
            idPlanificacion: Number,
            gestiones: Array,
            estadoPlanificacion: String,
            opcion: Boolean,
        },
        computed: {        
            arregloGestiones() {
                //Se envía una copia de las gestiones
                return this.gestiones                
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
            const actualizarArregloGestiones = (nuevaGestion) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloGestion", nuevaGestion);
            };
            const nuevaGestion = (nuevaGestion) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloGestion", nuevaGestion);
            };
            const quitarGestion = (gestionId) => {
                store.dispatch("planificacion/planificacionAcademica/eliminarGestion", gestionId);
            };                        
            return {                
                detalleAccion,
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                gestiones: toRef(props,"gestiones"),
                idPlanificacion: toRef(props,"idPlanificacion"),
                opcion: toRef(props,"opcion"),
                actualizarArregloGestiones,
                nuevaGestion,
                quitarGestion,
            };
        }        
    })
</script>