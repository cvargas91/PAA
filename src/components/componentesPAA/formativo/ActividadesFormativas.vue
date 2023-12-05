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
        <q-tab name="actividades" label="Actividades Formativas" />
    </q-tabs>
    
    <q-separator />

    <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="actividades" class="tarjetaAmarilla">                        
            <div class="text-h4">
                Participación en talleres, curso o seminarios 
            </div>
            <div class="text-subtitle1">
                internos o externos presenciales u online orientados a fortalecer capacidades de docencia y/o de investigación
            </div>
            <q-separator></q-separator>
            <TablaActividadesFormativas
                :actividadesFormativas="arregloActividadesFormativas"                
                :estadoPlanificacion="estado"
                :idPlanificacion="idPlanificacion"
                :opcion="tab"
                :editar="opcion"
                @updateActividades="actualizarActividadesFormativas"
                @insertActividadFormativa="nuevaActividadFormativa"
                @deleteActividad="quitarActividadFormativa"
            />
        </q-tab-panel>
    </q-tab-panels>
    
</template>
<script>    
    import { ref, toRef,computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    import TablaActividadesFormativas from "./TablaActividadesFormativas.vue";    

    export default defineComponent({
        components:{
            TablaActividadesFormativas,            
        },
        props: {
            idPlanificacion: Number,
            actividadesFormativas: Array,
            estadoPlanificacion: String,
            opcion: Boolean,
        },
        computed: {
            arregloActividadesFormativas() {                
                return this.actividadesFormativas.map((item) => {
                    const newItem = { ...item }; // Copia superficial del objeto original
                    if (newItem.fecha_inicio && newItem.fecha_fin) {
                        newItem.fechas = {
                            from: newItem.fecha_inicio,
                            to: newItem.fecha_fin
                        };
                    } else {
                        newItem.fechas = { from: '', to: '' }; // Ajustar si las fechas no están definidas
                    }
                return newItem;
                });
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
            const actualizarActividadesFormativas = (nuevaActividad) => {                
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloFormacion", nuevaActividad);
            };
            const nuevaActividadFormativa = (nuevaActividad) => {
                store.dispatch("planificacion/planificacionAcademica/actualizarArregloFormacion", nuevaActividad);
            };
            const quitarActividadFormativa = (actividadId) => {
                store.dispatch("planificacion/planificacionAcademica/eliminarActividadFormativa", actividadId);
            };                      
            return {                
                detalleAccion,                
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                actividadesFormativas: toRef(props,"actividadesFormativas"),
                idPlanificacion: toRef(props,"idPlanificacion"),
                opcion: toRef(props,"opcion"),
                actualizarActividadesFormativas,
                quitarActividadFormativa,
                nuevaActividadFormativa,
            };
        }        
    })
</script>