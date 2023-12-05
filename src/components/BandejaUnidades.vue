<template>    
    <div class="q-gutter-y-md">        
        <div class="text-subtitle1 text-textoAzul" v-if="seRenderea">
                <b>Unidad: {{ actor.nombre }} - Período: {{modelPeriodo}}</b>
        </div>
        <div class="q-gutter-y-md">
            <q-card>                
                <q-card-section>
                    <div class="q-gutter-md row" v-if="origen=='POA'">
                        <q-select
                            
                            v-model="modelPeriodo"
                            :options="accion.anios.periodo"
                            label="Año"
                            style="width: 30em"
                        />
                        
                                                
                        
                    </div>
                    <br/>   
                    <div class="q-gutter-md row" v-if="modelPeriodo != 2022 && !isNaN(parseFloat(modelPeriodo))">
                        <q-select
                            v-model="modelDireccion"
                            :options="actorStore.direccion"
                            label="Dirección"
                            style="width: 20em"
                            option-label="nombre"
                            
                            @update:model-value="cambioDireccion"
                        />  
                            <!-- 
                                Regla de validación de año requerido
                                :rules="[val => !!isNaN(parseFloat(val)) || 'Field is required']"
                            -->
                            <!-- @update:model-value="cambioDireccion"
                                @update:model-value="cambioUnidad"
                            -->                                           
                        <q-select
                            v-model="modelUnidad"
                            :options="actorStore.unidad"
                            label="Unidad"
                            style="width: 20em"
                            option-label="nombre"   
                            @update:model-value="cambioUnidad"                 
                        />
                    </div>
                    
                        <q-select
                            v-if="modelPeriodo == 2022 && !isNaN(parseFloat(modelPeriodo)) || origen=='PMI'"
                            filled                
                            :options="actores"
                            label="Unidades"
                            color="teal"
                            clearable
                            options-selected-class="text-deep-orange"                
                            option-label="sigla"                    
                            :model-value="actor"
                            @update:model-value="cambio"
                        >
                        <!--:model-value="actor"
                        @update:model-value="cambio"-->
                        <template v-slot:option="scope">
                            <q-item v-bind="scope.itemProps">
                            
                                <q-item-section>
                                    <q-item-label>{{ scope.opt.sigla }}</q-item-label>
                                    <q-item-label caption>{{ scope.opt.nombre }}</q-item-label>
                                </q-item-section>
    
                            </q-item>
                        </template>                
                    </q-select>
                    
                    
                </q-card-section>
                <q-card-section v-if="seRenderea" v-model="actor">
                    <!--<q-card >-->
                        <TablaAccionesUnidad v-if="modelPeriodo == 2022" 
                            :id_responsable="actor.id"
                            :acciones="accion.acciones"
                            :origen="origen"
                            :reportes="reportes"
                        />
                    <!--</q-card>-->
                </q-card-section>
                <q-card-section v-if="(typeof modelUnidad != 'string')" v-model="modelUnidad">
                    
                    <TablaAccionesUnidad v-if="modelPeriodo !== 2022" 
                            :id_responsable="modelUnidad.id"
                            :acciones="accion.acciones"
                            origen="Unificado"
                            :reportes="reportes"
                        /> 
                    <!--<q-card >-->
                        <!-- <TablaAccionesUnidad 
                            :id_responsable="modelUnidad.id"
                            :acciones="accion.acciones"
                            :origen="origen"
                            :reportes="reportes"
                        /> -->
                    <!--</q-card>-->
                </q-card-section>      
            </q-card>                                
        </div>
    </div>
    
</template>
<script>
import { ref, toRef, computed, onMounted, onUnmounted,beforeMount, defineComponent } from "vue";
import { useStore } from "vuex";
import TablaAccionesUnidad from "src/components/TablaAccionesUnidad.vue";


export default defineComponent({
    components:{
        TablaAccionesUnidad,
    },
    props:{
        origen: String,
        reportes: Array,
    },
    setup(props) {
        const store = useStore();
        const actorStore = computed(() => store.state.actor);
        const actores = computed(() => store.state.actor.actores);
        const accion = computed(() => store.state.accion);
        const actorInicial = "Seleccione una Unidad";
        const actor = ref(null);
        const detalleActor = ref("");
        const seRenderea = ref(null);
        const id_responsable = ref("");
        const model = ref(null);        
        const modelDireccion = ref("Seleccione la Dirección");
        const modelUnidad = ref("Seleccione la Unidad");
        const modelActor = ref({ label: "Todos", value: "Todos" });
        const modelPeriodo = ref("Seleccione el periodo del Reporte");

        onMounted(async () => {
            await store.dispatch("actor/reqActores");
            store.dispatch("accion/reqAniosDisponibles");
            await store.dispatch("actor/reqDirecciones");
            await store.dispatch("actor/reqUnidades");
            store.dispatch("accion/limpiaAcciones");
        });

        const cambioDireccion = (value) => {
            store.dispatch("actor/limpiaUnidad");
            store.dispatch("actor/limpiaActores");
            modelUnidad.value = "Seleccione la Unidad";            
      
            if(value !== "Todos"){
                store.dispatch("actor/reqUnidad", value.id);
            }else{
                store.dispatch("actor/reqUnidades");
                store.dispatch("actor/reqActores");
            }
        };

        const cambio = (value, event) => {
            if(value){                
                seRenderea.value = false;
                store.dispatch("accion/limpiaAcciones");                
                if(props.origen === "POA"){
                    store.dispatch("accion/reqAccionesPorRolResponsable", value.id);
                }else{
                    store.dispatch("accion/reqAccionesPorRolResponsablePMI", value.id);
                }
                actor.value = value;
                id_responsable.value = value.id;
                detalleActor.value = value.nombre;
                seRenderea.value = true;
            } else{
                seRenderea.value = false;
                actor.value = actorInicial;              
                store.dispatch("accion/limpiaAcciones");
            }
        };

        const cambioUnidad = (value) => {
            store.dispatch("actor/limpiaActores");
            store.dispatch("accion/limpiaAcciones");
            
            const rolPeriodo = {
                id_actor: value.id,
                anio: modelPeriodo.value,
            };
            
            store.dispatch("accion/reqAccionesPorRolResponsableUnificado", rolPeriodo);
            store.dispatch("actor/reqActores");
            // if(value !== "Todos"){
            //     store.dispatch("actor/reqFiltroActores", value.id);
      
        };        

        return {
            cambioUnidad,
            modelUnidad,
            modelPeriodo,
            cambioDireccion,
            actorStore,
            modelActor,
            modelDireccion,
            model,
            actor,
            actores,
            cambio,
            seRenderea,
            accion,
            id_responsable,
            detalleActor,
            origen: toRef(props, "origen"),
            reportes: toRef(props, "reportes")
        };
    },
});
</script>