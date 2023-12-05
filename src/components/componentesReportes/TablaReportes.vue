
<template>        
    <q-select v-if="tipoReporte == 'Reportes Unificados'"
            :options="opcionDireccion(reportes)"
            label="Dirección"
            color="teal"                      
            option-label="optionLabel"                                         
            style="width: 20em"
            v-model="modelDireccion"
            @update:model-value="cambioDireccion"
            >
        <!--:options="tipoReportes(reportes)"
            :model-value="actor"
            @update:model-value="cambio"  -->

            <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps">
                
                    <q-item-section>
                        <q-item-label>{{ Object.keys(scope.opt)[0] }}</q-item-label>                        
                    </q-item-section>

                </q-item>
            </template> 
    </q-select>      
    
    
    <q-table v-if="tipoTabla(tipoReporte)"
        :title="tipoReporte"
        :rows="modelDireccion? reportesUnificados.reportesUnificados : reportes"
        :columns="opciones"
        :selection="setOpcion(opcion)"
        row-key="id"
        v-model:selected="accionesSeleccionadas"
        @update:selected="emitirSeleccion()"
        no-data-label="No hay acciones para el filtro aplicado"
        :filter="filter"
        class="tablaAcciones"
    >
        <template v-slot:top-right>
            <q-input borderless dense debounce="300" v-model="filter" placeholder="Filtrar">
                <template v-slot:append>
                    <q-icon name="search" />
                </template>
            </q-input>
        </template>
        <!--<template v-slot:header-cell-checkBox="props">
            <q-checkbox v-model="props.accionesSeleccionadas" />
        </template>-->
    
        <template v-slot:body-cell-checkBox="props">
            <q-checkbox :model-value="props.accionesSeleccionadas" @update:model-value="(val, evt) => { val }" />
        </template>

        <template v-slot:body-cell-infoButton="props">
            <q-tr :props="props" style="height:55px;">
                <q-td auto-width>
                    <q-btn 
                        size="sm" 
                        color="btnAdjuntar" 
                        round dense 
                        @click="toggleExpandAndFilter(props)"
                        :icon="expandedRows.includes(props.key) ? 'remove' : 'add'"                        
                    />
                </q-td>
                <q-td
                    v-for="col in props.cols"
                    :key="col.name"
                    :props="props"                    
                >
                    {{ col.value }}
                </q-td>
            </q-tr>
            <!-- <q-tr v-show="props.expand" :props="props"> -->

            <q-tr v-show="expandedRows.includes(props.key)" :props="props">                
                <q-td colspan="100%">
                    <div class="text-left">
                        Acciones en Reporte N°{{ props.row.id }}: 
                        <li v-for="(item, id) in idUaysenAcciones[props.key]" :key="id">{{ item }}</li>
                    </div>    
                </q-td>                
            </q-tr>
        </template>
    </q-table>
</template>

<script>
import { ref, toRef,computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
    props: {
        reportes: Array,
        reporteSeleccionado: Object,
        opcion: Boolean,
        tipoReporte: String,
    },
    methods: {
        async emitirSeleccion() {                
            await this.$emit("cambio-seleccion", this.accionesSeleccionadas);            
        },
        toggleExpandAndFilter(props) {            
            const keyFila = props.key;
            const isExpanded = this.expandedRows.includes(keyFila);
            
            if (isExpanded) {                
                //this.expandedRows.splice(isExpanded, 1); // La fila ya estaba expandida, la contraemos
                this.expandedRows = this.expandedRows.filter(elemento => elemento != keyFila)
            } else {
                this.expandedRows.push(keyFila);
                this.filtrarAcciones(props);
            }        
        },
        setOpcion (opcion) {
            if(opcion){
                if(this.reportes[0].tipo == "Unificado"){
                    return "multiple";
                }else{
                    return "single";
                }                
            }else{
                return "none"
        }
        },
        filtrarAcciones(props) {                 
            const key = props.key;
            const reporteAcciones = props.row.reporte_acciones;

            if (this.idUaysenAcciones.hasOwnProperty(key)) {
                // La clave ya existe
                return;
            }

            this.idUaysenAcciones[key] = reporteAcciones.map(accion => {
                const idUaysenIncluidos = this.accion.acciones.find(elemento => elemento.accion.id === accion.accion);

                return idUaysenIncluidos ? idUaysenIncluidos.accion.id_uaysen : "no se encontró ID accion";
            });            
        },
        opcionDireccion(opciones) {
            const actorDependenciaMap = {};

            opciones.forEach((opcion) => {
                const actor = this.actores.find((a) => a.id === opcion.actor);
                    const dependenciaNombre = actor.dependencia.nombre;
    
                    if (!actorDependenciaMap[dependenciaNombre]) {
                        actorDependenciaMap[dependenciaNombre] = [];
                    }
                    actorDependenciaMap[dependenciaNombre].push(opcion.actor);
            });

            return Object.entries(actorDependenciaMap).map(([nombreDependencia, actores]) => ({
                [nombreDependencia]: actores,
            }));            
        },
        tipoTabla(tipoTabla) {
            if (tipoTabla == "Reportes Unificados"){
                if(this.modelDireccion){
                    return true;
                }else{
                    return false;
                }
            }else {
                return true;
            }
        },
        
    },
    watch: {
        reporteSeleccionado(nuevoValor){            
            this.accionesSeleccionadas = nuevoValor;
        },
        reportes(newValue){
            this.modelDireccion = null;
        },
    },
    setup(props) {        
        const store = useStore();    
        const accion = computed(() => store.state.accion);
        const reportesUnificados = computed(() => store.state.reporte)
        ///const idUaysenAcciones = ref([]);
        const idUaysenAcciones = ref({});
        const expandedRows = ref([]);
        //const opcion = ref("");
        const reportes = computed({
            get:() => props.reportes
        });
        const seRenderea = ref(false);
        const actores = computed(() => store.state.actor.actores);
        const accionesSeleccionadas = ref([]);
        const modelDireccion = ref(null);
        const reporteSeleccionado = computed({
            get: () => props.reporteSeleccionado
        });

        const getValor = (actor) => {
            let detalleActor = actores.value.filter(elemento => elemento.id === actor).map(detalle => detalle.id_uaysen);
            return (detalleActor[0]);
        };
        if(props.reportes.length){
            if(props.reportes[0].estado === "Finalizado"){
                seRenderea.value = true;
            }
        }    

        // if(props.opcion){
        //     opcion.value = "single"
        // }else{
        //     opcion.value = "none"
        // }

        const cambioDireccion = (value) => {            
            if (reportes.value[0].estado == "Finalizado") {
                store.dispatch("reporte/setReporteAUnificarFinalizado", value[Object.keys(value)[0]]);
            }else {
                store.dispatch("reporte/setReporteAUnificarBorrador", value[Object.keys(value)[0]]);
            }
            
            modelDireccion.value = Object.keys(value)[0]
        };

        return {
            reportesUnificados,
            modelDireccion,
            cambioDireccion,
            tipoReporte: toRef(props, "tipoReporte"),
            opcion: toRef(props, "opcion"),
            filter: "",
            expandedRows,            
            accion,
            idUaysenAcciones,
            reportes,
            seRenderea,
            actores,
            getValor,
            accionesSeleccionadas,
            reporteSeleccionado,            
            opciones: [
                { name: 'infoButton', field: 'infoButton', align: 'left', sortable: false, label: 'Ver Acciones' },
                {
                    name: "reporte",
                    label: "N° Reporte",
                    field: "id",
                    align: "left",
                },
                {
                    name: "unidad",
                    label: "Unidad",
                    field: (row) => (getValor(row.actor)),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "creado",
                    label: "Creado",
                    field: "creado",
                    align: "left",
                    sortable: true,
                },
                {
                    name: "creado",
                    label: "Modificado",                    
                    field: "modificado",
                    align: "left",
                    sortable: true,
                },
                {
                    name: "enviado",
                    label: "Enviado",
                    field: (row) => {
                        if(row.enviado)
                            return "Enviado a " + getValor(row.actor);
                        else
                            return "-"
                    },
                    align: "left",
                    sortable: true,
                }
            ]

        }
    }

})
</script>
    