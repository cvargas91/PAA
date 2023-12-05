<template>    
    <PopUpIngresoNuevoEvento
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevoEvento"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar evento a planificación"
            color="positive"
            no-caps
            @click="ingresarEvento"
        />
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            label="Quitar evento"
            color="btnCancelar"
            no-caps
            @click="quitarEvento"
        />
    </div>    
    <q-table
        v-model:selected="selected"
        :rows="eventos"
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
                    @hide="disableQPopupEdit"
                    @update:modelValue="actualizarEvento(props.row)"
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
                    @hide="disableQPopupEdit"
                    @update:modelValue="actualizarEvento(props.row)"
                >   
                    <q-input
                        v-model="scope.value"                        
                        dense
                        autofocus
                        autogrow
                        @keyup.enter="scope.set"
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
    import PopUpIngresoNuevoEvento from "src/components/componentesPAA/investigacion/PopUpIngresoNuevoEvento.vue"

    export default defineComponent({
        components:{
            PopUpIngresoNuevoEvento,
        },
        props: {
            eventos: Array,
            estadoPlanificacion: String,
            idPlanificacion: Number,
            editar: Boolean,
            opcion: String,
        },
        methods: {
            disableQPopupEdit() {
                this.disable = true;
            },
            actualizarEvento(row) {
                const copiaRow = { ...row };
                this.$emit("updateEventos", copiaRow);
                // row contiene los datos de la fila editada
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
            const quitarEvento = () => {
                emit("deleteEvento", selected.value[0].id);
                selected.value = [];
            }
            const manejoNuevoEvento = (respuesta) => {
                popUpNuevoCurso.value = false;
                if(respuesta.opcion == "guardar"){

                    const nuevoEvento = {
                        planificacion: idPlanificacion.value,
                        tipo: "Evento",
                        nombre_proyecto: "",
                        descripcion: respuesta.data.descripcion,
                        cantidad_horas: respuesta.data.horas,
                        estado_proyecto:null,
                        autoria: null,
                        fuente_financiamiento: null,

                    };

                    emit("insertEvento", nuevoEvento);
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
                    style: "white-space: normal; max-width: 90px; word-wrap: break-word;",
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
                'horas'
            ]);

            const opcionesAsignatura = ref([]);
            return {
                disable: false,
                opciones,                
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                eventos: toRef(props,"eventos"),
                manejoNuevoEvento,
                quitarEvento,
                columnasVisibles,
                popUpNuevoCurso,
                mostrar,
                opcionesAsignatura,
                ingresarEvento :() => {
                    selected.value = [];
                    opcionesAsignatura.value = props.eventos.map(elemento => {
                        let opcion = {
                            label : elemento.nombre,
                            value : elemento.id,
                            codigo: elemento.codigo
                        }
                        return opcion;
                    })
                    popUpNuevoCurso.value = true;
                },
            };
        }        
    })
</script>