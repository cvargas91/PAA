<template>    
    <PopUpNuevaActividadFormativa
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevaActividadFormativa"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar nueva actividad Formativa"
            color="positive"
            no-caps
            @click="ingresarActividadFormativa"
        />
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            :label="truncarLabel(selected[0].nombre_actividad)"
            color="btnCancelar"
            no-caps
            @click="quitarActividadFormativa"
        />
    </div>  
    <!-- actividaddes -> {{ actividadesFormativas  }}   -->
    <q-table
        v-model:selected="selected"
        :rows="actividadesFormativas"
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
                    @update:modelValue="actualizarActividadFormativa(props.row)"
                    @hide="disableQPopupEdit"
                >   
                    <q-input
                        v-model="scope.value"                        
                        dense
                        autofocus
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
    <template v-slot:body-cell-institucion="props">
        <q-td :props="props">
            {{ props.row.institucion }}
            <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.institucion"
                    v-if="editar"                    
                    @update:modelValue="actualizarActividadFormativa(props.row)"
                    @hide="disableQPopupEdit"
                >   
                    <q-input
                        v-model="scope.value"                        
                        dense
                        autofocus
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
    <template v-slot:body-cell-fechas="props">
        <q-td :props="props">
            {{ props.row.fecha_inicio }} / {{ props.row.fecha_fin }}
            <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.fechas"
                    v-if="editar"
                    @update:modelValue="actualizarActividadFormativaFechas(props.row)"
                    @hide="disableQPopupEdit"
                >                       
                    <q-date 
                        v-model="scope.value" 
                        @keyup.enter="scope.set" 
                        range
                        mask="YYYY-MM-DD"
                    />
                    <q-separator></q-separator>
                    <div class="row justify-end q-gutter-sm q-ma-md">
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
                    @update:modelValue="actualizarActividadFormativa(props.row)"
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
    import PopUpNuevaActividadFormativa from "src/components/componentesPAA/formativo/PopUpNuevaActividadFormativa.vue"

    export default defineComponent({
        components:{
            PopUpNuevaActividadFormativa,
        },
        props: {
            actividadesFormativas: Array,
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
            actualizarActividadFormativa(row) {
                const copiaRow = { ...row };
                this.$emit("updateActividades", copiaRow);
                // row contiene los datos de la fila editada
            },
            actualizarActividadFormativaFechas(row) {
                const copiaRow = { ...row };
                copiaRow.fecha_inicio = copiaRow.fechas.from;
                copiaRow.fecha_fin = copiaRow.fechas.to;
                this.$emit("updateActividades", copiaRow);
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
            const quitarActividadFormativa = () => {
                emit("deleteActividad", selected.value[0].id);
                selected.value = [];
            };

            const manejoNuevaActividadFormativa = (respuesta) => {
                popUpNuevoCurso.value = false;
                if(respuesta.opcion == "guardar"){

                    const nuevaActividadFormativa = {
                        planificacion: idPlanificacion.value,
                        nombre_actividad: respuesta.data.nombre,
                        cantidad_horas: respuesta.data.horas,
                        institucion:respuesta.data.institucion,
                        fecha_inicio:respuesta.data.fecha_inicio.replace(/\//g, '-'),
                        fecha_fin:respuesta.data.fecha_fin.replace(/\//g, '-'),
                    };

                    emit("insertActividadFormativa", nuevaActividadFormativa);
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
                    label: "Nombre Actividad Formativa",
                    field: (row) => (row.nombre_actividad ? row.nombre_actividad : "Otro"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "institucion",
                    label: "Institucion que realiza la Actividad",
                    field: (row) => (row.institucion ? row.institucion : "institucion"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "fechas",
                    label: "Fechas",
                    field: (row) => {
                        console.log("Fecha? ", row)
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
                'institucion',
                'fechas',
                'horas'
            ]);
            return {
                opciones,
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                actividadesFormativas: toRef(props,"actividadesFormativas"),
                manejoNuevaActividadFormativa,
                quitarActividadFormativa,
                columnasVisibles,
                popUpNuevoCurso,
                mostrar,
                opcionesAsignatura,
                ingresarActividadFormativa :() => {
                    selected.value = [];
                    opcionesAsignatura.value = props.actividadesFormativas.map(elemento => {
                        let opcion = {
                            label : elemento.nombre,
                            value : elemento.id,
                            codigo: elemento.codigo
                        }
                        return opcion;
                    })
                    popUpNuevoCurso.value = true;
                },
                disable: false,
            };
        }        
    })
</script>