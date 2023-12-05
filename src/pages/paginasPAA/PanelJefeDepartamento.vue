<template>
    <q-card
        dense

    >
        <div class="q-pa-md text-textoAzul">
            <div class="text-h6"><b>Panel Planificación Anual Académica</b></div>

        </div>
        <div>
            <q-splitter
                v-model="splitterModel"
                style="height: auto"
            >
        
                <template v-slot:before>
                    <q-tabs
                        :model-value="tab"
                        @update:model-value="cambiaTab"
                        vertical
                        class="text-teal"
                    >
                        <q-tab name="planificaciones" icon="route" label="Planificaciones" />
                        <q-tab name="asignaciones" icon="local_offer" label="Asignaciones de Cursos" />
                        <q-tab name="observaciones" icon="alt_route" label="Observaciones" />
                    </q-tabs>
                </template>
            
                <template v-slot:after>
                    <q-tab-panels
                        v-model="tab"
                        animated
                        swipeable
                        vertical
                        transition-prev="jump-up"
                        transition-next="jump-up"
                    >                  
                        <q-tab-panel name="planificaciones">
                            <div class="row q-mb-md">
                                <div class="col text-textoAzul text-h4">Planificaciones Académicas</div>
                                <div class="col">
                                    <q-select
                                        v-model="modelPeriodo"
                                        label="Año"
                                        style="width: 10em; margin-left: 315pt"
                                    />
                                </div>
                            </div>
                                <template v-if="planificacion.planificacionesDepartamento">                                    
                                    <TablaPlanificacionesDepartamento                                        
                                        :resumenHoras="planificacion.resumenHoras"
                                        :periodo="modelPeriodo"
                                    />
                                </template>
                                <template v-else>
                                <div class="text-center">
                                    <q-spinner color="primary" size="3em" />
                                </div>
                                </template>                            
                        </q-tab-panel>
                    
                        <q-tab-panel name="asignaciones">
                            <div class="row q-mb-md">
                                <div class="col text-textoAzul text-h4">Asignaciones de cursos</div>
                                <div class="col">
                                    <q-select
                                        v-model="modelPeriodo"
                                        label="Año"
                                        style="width: 10em; margin-left: 315pt"
                                    />
                                </div>
                            </div>
                            <template v-if="planificacion.academicxs">
                                <TablaAcademicosDepartamento
                                    style="padding-left: 3pt;"
                                    
                                    :periodo="modelPeriodo"
                                    origen="jefe"
                                />
                                <!-- <TablaAsignaturasAcademico
                                    style="padding-left: 3pt;"
                                    :cursosAcademico="cursos.misCursos"
                                    :periodo="modelPeriodo"
                                    origen="jefe"
                                /> -->
                            </template>
                            <template v-else>
                                <div class="text-center">
                                    <q-spinner color="primary" size="3em" />
                                </div>
                            </template>
                        </q-tab-panel>
                    
                        <q-tab-panel name="observaciones">
                            <div class="row q-mb-md">
                                <div class="col text-textoAzul text-h4">Observaciones a Planificación Anual Académica</div>
                                <div class="col text-right">
                                    <q-select
                                        v-model="modelPeriodo"
                                        label="Año"
                                        style="width: 10em; margin-left: 315pt"
                                    />
                                </div>
                            </div>
                            <TablaObservacionesPlanificacionAcademica
                                style="padding-left: 3pt;"
                                origen="jefe"
                            />                            
                        </q-tab-panel>
                    </q-tab-panels>
                </template>
            
            </q-splitter>
        </div>

    </q-card>
</template>

<script>
import { ref, computed, onMounted, defineComponent } from "vue";
import { useStore } from "vuex";
import TablaPlanificacionesDepartamento from "src/components/componentesPAA/TablaPlanificacionesDepartamento.vue";
import TablaObservacionesPlanificacionAcademica from "src/components/componentesPAA/TablaObservacionesPlanificacionAcademica.vue";
import TablaAsignaturasAcademico from "src/components/componentesPAA/TablaAsignaturasAcademico.vue";
import TablaAcademicosDepartamento from "src/components/componentesPAA/TablaAcademicosDepartamento.vue";
//import PanelBandejaEntrega from "src/components/PanelBandejaEntrega.vue";

export default defineComponent({
    components: {
  //      PanelBandejaEntrega,
        TablaPlanificacionesDepartamento,
        TablaObservacionesPlanificacionAcademica,
        TablaAsignaturasAcademico,
        TablaAcademicosDepartamento,
    },

    setup() {
        const modelPeriodo = ref("2023");
        const usuario = computed(() => store.state.usuarix.usuario);
        const tab = ref("planificaciones");
        const store = useStore();
        const cursos = computed(() => store.state.planificacion.asignatura);
        const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
        onMounted(async ()=>  {
            await store.dispatch("planificacion/planificacionAcademica/planificacionesDepartamento", modelPeriodo.value)
            await store.dispatch("planificacion/asignatura/getCursos");
            await store.dispatch("planificacion/planificacionAcademica/getAcademicos");
            await store.dispatch("accion/reqAccionesPorRolResponsableUnificadoDetalle", 
            {
                'id_actor' : usuario.value.perfil.actor_id,
                'anio' : modelPeriodo.value
            }
            );
            //await store.dispatch("planificacion/asignatura/getMisCursos");
            //await store.dispatch("planificacion/planificacionAcademica/getMisPlanificaciones");
        })
        const cambiaTab = async (value, event) => {
            //store.dispatch("accion/limpiaAcciones");
            
            if (value == "planificaciones") 
                await store.dispatch("planificacion/planificacionAcademica/planificacionesDepartamento", modelPeriodo.value)                
            else if (value == "asignaciones")
                //store.dispatch("verificador/reqMisVerificadores");
                await store.dispatch("planificacion/asignatura/getCursos");
            else if (value == "observaciones"){
                store.dispatch("planificacion/observaciones/getObservacionesUsuario");
            }

            tab.value = value;
            //innerTab.value = "planificaciones";
        };
        return {
            modelPeriodo,
            tab,
            splitterModel: ref(15),
            cambiaTab,
            cursos,
            planificacion,
        }
    },
});
</script>
