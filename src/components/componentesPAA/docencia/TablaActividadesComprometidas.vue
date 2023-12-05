<template>    
    <PopUpIngresoNuevasActividades
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevoCurso"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar actividad a Planificación"
            color="positive"
            no-caps
            @click="ingresarActividad"
        />
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            no-caps
            :label="truncarLabel(selected[0].descripcion)"
            color="btnCancelar"
            @click="quitarActividad"
        />
    </div>
    <!-- {{ otrasActividades }} ¡?? -->
    <q-table
        v-model:selected="selected"
        :rows="otrasActividades"
        :columns="opciones"
        virtual-scroll
        :rows-per-page-options="[0]"
        style="height: 300px"
        row-key="id"
        no-data-label="No información disponible"
        class="tarjetaAmarilla"
        :selection="editar? 'single' : 'none'"
        @selection="seleccionaFila"
    >
    <template v-slot:body-cell-descripcion="props">
        <q-td :props="props">
            {{ props.row.descripcion }}
            <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.descripcion"
                    v-if="editar"                    
                    @update:modelValue="actualizarActividad(props.row)"
                    @hide="disableQPopupEdit"
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
    <template v-slot:body-cell-horas="props">
        <q-td :props="props">
            {{ props.row.cantidad_horas }}
            <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.cantidad_horas"
                    v-if="editar"                    
                    @update:modelValue="actualizarActividad(props.row)"
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
    </q-table>
</template>

<script>    
    import { ref, toRef, computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    import PopUpIngresoNuevasActividades from "src/components/componentesPAA/docencia/PopUpIngresoNuevasActividades.vue"

    export default defineComponent({
        components:{
            PopUpIngresoNuevasActividades,
        },
        props: {
            otrasActividades: Array,
            estadoPlanificacion: String,
            idPlanificacion: Number,
            editar: Boolean,
            opcion: String,
        },
        computed: {
            truncarLabel() {
                const label = "Quitar actividad: "
                return (descripcion) => {
                    if (descripcion.length > 60) {
                        return label + descripcion.substring(0, 60) + '....';
                    }
                    return label + descripcion;
                };
            },
        },
        methods: {
            disableQPopupEdit() {
                this.disable = true;
            },
            actualizarActividad(row) {
                const copiaRow = { ...row };
                this.$emit("updateActividades", copiaRow);                
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
            const quitarActividad = () => {
                emit("deleteActividad", selected.value[0].id);
                selected.value = [];
            }
            const manejoNuevoCurso = (respuesta) => {
                popUpNuevoCurso.value = false;
                if(respuesta.opcion == "guardar"){

                    const nuevaActividad = {
                        planificacion: idPlanificacion.value,
                        asignatura: null,
                        tipo: "OtraActividad",
                        semestre: "1",
                        cantidad_horas: respuesta.data.horas,
                        programa: "",
                        descripcion: respuesta.data.descripcion,
                        observacion: "",
                    };

                    emit("insertActividad", nuevaActividad);
                }
            };

            const cambiaTab = (value, event) => {                
                tab.value = value;
                //innerTab.value = "borrador";
            }   
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            }

            const opciones = [
                {
                    name: "descripcion",
                    label: "Descripción de la actividad",
                    field: (row) => (row.descripcion ? row.descripcion : "Sem"),
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
            ]
            const opcionesAsignatura = ref([]);
            return {
                opciones,                
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                otrasActividades: toRef(props,"otrasActividades"),
                manejoNuevoCurso,
                popUpNuevoCurso,
                quitarActividad,
                mostrar,
                opcionesAsignatura,
                disable: false,
                ingresarActividad :() => {
                    opcionesAsignatura.value = props.otrasActividades.map(elemento => {
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
