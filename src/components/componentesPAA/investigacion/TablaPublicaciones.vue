<template>    
    <PopUpIngresoNuevaPublicacion
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevaPublicacion"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar publicación a planificación"
            color="positive"
            no-caps
            @click="ingresarPublicacion"
        />
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            label="Quitar publicación"
            color="btnCancelar"
            no-caps
            @click="quitarPublicacion"
        />
    </div>    
    <q-table
        v-model:selected="selected"
        :rows="publicaciones"
        :columns="opciones"
        row-key="id"
        :visible-columns="columnasVisibles"
        virtual-scroll
        :rows-per-page-options="[0]"
        style="height: 300px"
        no-data-label="No información disponible"
        class="tarjetaAmarilla"
        :selection="editar? 'single' : 'none'"
        @selection="seleccionaFila"
    >
    <template v-slot:body-cell-horas="props">
        <q-td :props="props">
            {{ props.row.cantidad_horas }}                
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.cantidad_horas"
                    v-if="editar"                    
                    @update:modelValue="actualizarPublicacion(props.row)"
                    @hide="disableQPopupEdit"
                >   
                    <q-input
                        v-model="scope.value"                        
                        dense
                        autofocus
                        @keyup.enter="scope.set"
                        mask="#####"                            
                    />
                    <div class="q-gutter-sm">
                        <q-btn
                        label="Cancelar"
                        @click="scope.cancel"
                        color="btnVolver"
                    />
                    <q-btn
                        label="Guardar"
                        @click="scope.set"
                        color="btnContinuar"
                    />
                    </div>
            </q-popup-edit>
        </q-td>            
    </template>  
    <template v-slot:body-cell-nombre="props">
        <q-td :props="props">
            {{ props.row.descripcion }}                
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.descripcion"
                    v-if="editar"                    
                    @update:modelValue="actualizarPublicacion(props.row)"
                    @hide="disableQPopupEdit"
                >   
                    <q-input
                        v-model="scope.value"                        
                        dense
                        autofocus
                        @keyup.enter="scope.set"
                        autogrow
                    />
                    <div class="q-gutter-sm">
                        <q-btn
                            label="Cancelar"
                            @click="scope.cancel"
                            color="btnVolver"
                        />
                        <q-btn
                            label="Guardar"
                            @click="scope.set"
                            color="btnContinuar"
                        />
                    </div>
            </q-popup-edit>
        </q-td>            
    </template>  
    <template v-slot:body-cell-calidad="props">
        <q-td :props="props">
            {{nombreAutoria(props.row.autoria)}}
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.autoria"
                    v-if="editar"
                    @hide="disableQPopupEdit"
                    @update:modelValue="actualizarPublicacion(props.row)"
                >   
                    <q-select
                        v-model="scope.value" 
                        :options="opcionesAutoria"
                        style="width: 100%;"
                        @keyup.enter="scope.set"                        
                        :display-value="nombreAutoria(scope.value)"
                    />
                    <div class="q-gutter-sm">
                        <q-btn
                            label="Cancelar"
                            @click="scope.cancel"
                            color="btnVolver"
                        />
                        <q-btn
                            label="Guardar"
                            @click="scope.set"
                            color="btnContinuar"
                        />
                    </div>
            </q-popup-edit>
        </q-td>            
    </template>  
    </q-table>
</template>

<script>    
    import { ref, toRef, computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    import PopUpIngresoNuevaPublicacion from "src/components/componentesPAA/investigacion/PopUpIngresoNuevaPublicacion.vue"

    export default defineComponent({
        components:{
            PopUpIngresoNuevaPublicacion,
        },
        props: {
            publicaciones: Array,
            estadoPlanificacion: String,
            idPlanificacion: Number,
            editar: Boolean,
            opcion: String,
        },
        methods: {
            disableQPopupEdit() {
                this.disable = true;
            },
            nombreAutoria (autoria){
                if (autoria !== "-" && autoria) {
                    return autoria.label || this.opcionesAutoria.find(opcion => opcion.value == autoria).label;
                } else {
                    return "-";
                }
            },
            actualizarPublicacion(row) {
                const copiaRow = { ...row };
                const unidadesPermitidas = this.opcionesAutoria.map(opcion => opcion.value);
                if (copiaRow.autoria){                    
                    if (!unidadesPermitidas.includes(copiaRow.autoria)){
                        copiaRow.autoria = copiaRow.autoria.value || this.opcionesAutoria.find(opcion => opcion.label == copiaRow.autoria).value;
                    }
                }
                // if (typeof(row.autoria) !== 'number')
                //     row.autoria = row.autoria.value;
                this.$emit("updatePublicaciones", copiaRow);                
            },
        },
        setup(props, {emit}) {
            const router = useRouter();
            const store = useStore();            
            const selected = ref([]);
            const tab = ref("informacionBasica");
            const mostrar = ref("");
            const popUpNuevoCurso = ref(false);
            const idPlanificacion = ref(props.idPlanificacion);
            const quitarPublicacion = () => {
                emit("deletePublicacion", selected.value[0].id);
                selected.value = [];
            }
            const manejoNuevaPublicacion = (respuesta) => {
                popUpNuevoCurso.value = false;
                if(respuesta.opcion == "guardar"){

                    const nuevaPublicacion = {
                        planificacion: idPlanificacion.value,
                        tipo: "Publicacion",
                        nombre_proyecto: "",
                        descripcion: respuesta.data.descripcion,
                        cantidad_horas: respuesta.data.horas,
                        estado_proyecto:null,
                        autoria: respuesta.data.autoria.value,
                        fuente_financiamiento: null,

                    };
                    emit("insertPublicacion", nuevaPublicacion);
                }
            }
            const cambiaTab = (value, event) => {                
                tab.value = value;
                //innerTab.value = "borrador";
            }   
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            }

            const opciones = [
                {
                    name: "id",
                    label: "Id planificacion",
                    field: (row) => (row.id ? row.id : "id"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "nombre",
                    label: "Descripción de la actividad",
                    field: (row) => (row.descripcion ? row.descripcion : "Otro"),
                    align: "left",
                    sortable: true,
                    style: "white-space: normal; max-width: 20px; word-wrap: break-word;",
                },
                {
                    name: "calidad",
                    label: "Calidad de autoría",
                    field: (row) => {
                        if(row.autoria){
                            if (row.autoria == "1")
                                return "Autor libro";
                            if (row.autoria == "2")
                                return "Editor o compilador"
                            if (row.autoria == "3")
                                return "Primer autor capítulo"
                            if (row.autoria == "4")
                                return "Co-autor capítulo"
                        }

                    },
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "horas",
                    label: "Horas estimadas",
                    field: (row) => (row.cantidad_horas ? row.cantidad_horas : "Sin"),
                    align: "left",
                    style: "white-space: normal",
                },
            ];
            
            const columnasVisibles = ref([
                'nombre',
                'calidad',
                'horas'
            ]);

            const opcionesAsignatura = ref([]);
            return {
                opciones,
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                publicaciones: toRef(props,"publicaciones"),
                manejoNuevaPublicacion,
                columnasVisibles,
                quitarPublicacion,
                popUpNuevoCurso,
                mostrar,
                opcionesAsignatura,
                ingresarPublicacion :() => {
                    selected.value = [];
                    opcionesAsignatura.value = props.publicaciones.map(elemento => {
                        let opcion = {
                            label : elemento.nombre,
                            value : elemento.id,
                            codigo: elemento.codigo
                        }
                        return opcion;
                    })
                    popUpNuevoCurso.value = true;
                },
                opcionesAutoria: [              
                    { label: "Autor libro",            value: "1" },
                    { label: "Editor o compilador",     value: "2" },
                    { label: "Primer autor capítulo",   value: "3" },
                    { label: "Co-autor capítulo",       value: "4" },
                ],
                disable: false,    
            };
        }        
    })
</script>