<template>    
    <PopUpIngresoNuevaGestionInstitucional
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevaGestion"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar nueva actividad de Gestión"
            color="positive"
            no-caps
            @click="ingresarGestion"
        />
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            no-caps
            :label="truncarLabel(selected[0].nombre_actividad)"
            color="btnCancelar"
            @click="quitarGestion"
        />
    </div>
    <!-- Evento-> {{ gestiones }} -->
    <q-table
        v-model:selected="selected"
        :rows="gestiones"
        :columns="opciones"
        :visible-columns="columnasVisibles"
        row-key="id"
        virtual-scroll
        :rows-per-page-options="[0]"
        style="height: 300px"
        no-data-label="No información disponible"
        class="tarjetaAmarilla"
        :selection="editar? 'single' : 'none'"
        @selection="seleccionaFila"
    >
    <template v-slot:body-cell-nombre="props">
        <q-td :props="props">
            {{ props.row.nombre_actividad }}
            <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.nombre_actividad"
                    v-if="editar"                    
                    @update:modelValue="actualizarGestion(props.row)"
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
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.cantidad_horas"
                    v-if="editar"                    
                    @update:modelValue="actualizarGestion(props.row)"
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
    <template v-slot:body-cell-cargo="props">
        <q-td :props="props">
            {{ nombreCargo(props.row.cargo) }}
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.cargo"
                    v-if="editar"                    
                    @update:modelValue="actualizarGestion(props.row)"
                    @hide="disableQPopupEdit"
                >
                    <q-select
                        v-model="scope.value" 
                        :options="opcionesCargo"
                        style="width: 100%;"
                        @keyup.enter="scope.set"                        
                        :display-value="nombreCargo(scope.value)"
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
    import PopUpIngresoNuevaGestionInstitucional from "src/components/componentesPAA/gestion/PopUpIngresoNuevaGestionInstitucional.vue"

    export default defineComponent({
        components:{
            PopUpIngresoNuevaGestionInstitucional,
        },
        props: {
            gestiones: Array,
            estadoPlanificacion: String,
            idPlanificacion: Number,
            editar: Boolean,
            opcion: String,
        },
        computed: {
            truncarLabel() {
                const label = "Quitar actividad: "
                return (nombre_actividad) => {
                    if (nombre_actividad.length > 60) {
                        return label + nombre_actividad.substring(0, 60) + '....';
                    }
                    return label + nombre_actividad;
                };
            },
        },
        methods: {
            disableQPopupEdit() {
                this.disable = true;
            },
            actualizarGestion(row) {
                const copiaRow = { ...row };
                const cargos = this.opcionesCargo.map(opcion => opcion.value);
                if (copiaRow.cargo){                    
                    if (!cargos.includes(copiaRow.cargo)){
                        copiaRow.cargo = copiaRow.cargo.value || this.opcionesCargo.find(opcion => opcion.label == copiaRow.cargo).value;
                    }
                }

                this.$emit("updateGestiones", copiaRow);
                // row contiene los datos de la fila editada
            },
            nombreCargo (cargo){
                
                if (cargo !== "-" && cargo) {
                    return cargo.label || this.opcionesCargo.find(opcion => opcion.value == cargo).label;
                } else {
                    return "-";
                }
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
            const quitarGestion = () => {
                emit("deleteGestion", selected.value[0].id);
                selected.value = [];
            };
            const manejoNuevaGestion = (respuesta) => {
                popUpNuevoCurso.value = false;
                if(respuesta.opcion == "guardar"){

                    const nuevaGestion = {
                        planificacion: idPlanificacion.value,
                        nombre_actividad: respuesta.data.nombre,
                        cantidad_horas: respuesta.data.horas,
                        cargo:respuesta.data.cargo.value,
                    };
                    emit("insertGestion", nuevaGestion);
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
                    label: "Nombre actividad de gestión y/o comité y comisión",
                    field: (row) => (row.nombre_actividad ? row.nombre_actividad : "Otro"),
                    align: "left",
                    sortable: true,
                    style: "white-space: normal; max-width: 20px; word-wrap: break-word;",
                },
                {
                    name: "cargo",
                    label: "Cargo",
                    field: (row) => {
                        if (row.cargo){
                            if (row.cargo == "1")
                                return "Coordinador o Jefe de equipo"
                            if (row.cargo == "2")
                                return "Participante o miembro del equipo"
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
            ]
            const opcionesAsignatura = ref([]);
            const columnasVisibles = ref([
                'nombre',
                'cargo',
                'horas'
            ]);
            return {
                opciones,                
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                gestiones: toRef(props,"gestiones"),
                manejoNuevaGestion,
                quitarGestion,
                columnasVisibles,
                popUpNuevoCurso,
                mostrar,
                opcionesAsignatura,
                ingresarGestion :() => {

                    selected.value = [];
                    opcionesAsignatura.value = props.gestiones.map(elemento => {
                        let opcion = {
                            label : elemento.nombre,
                            value : elemento.id,
                            codigo: elemento.codigo
                        }
                        return opcion;
                    })
                    popUpNuevoCurso.value = true;
                },
                opcionesCargo: [              
                    { label: "Coordinador o Jefe de equipo",        value: "1" },
                    { label: "Participante o miembro del equipo"  , value: "2" },
                ],
                disable: false,
            };
        }        
    })
</script>