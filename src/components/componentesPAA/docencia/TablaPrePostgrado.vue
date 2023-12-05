<template>    
    <PopUpIngresoNuevoCUrso
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"        
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevoCurso"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar Asignatura a Planificación"
            color="positive"
            @click="ingresarCurso"
            no-caps
        />
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            :label="'Quitar Asignatura código ' + selected[0].codigo"
            color="btnCancelar"
            no-caps
            @click="quitarAsignatura"
        />
    </div>
    
    <q-table
        v-model:selected="selected"
        :rows="asignaturasPlanificacion"
        :columns="opciones"
        :visible-columns="columnasVisibles"
        virtual-scroll
        :rows-per-page-options="[0]"
        style="height: 400px"
        row-key="id"
        no-data-label="No información disponible"
        class="tarjetaAmarilla my-sticky-virtscroll-table"
        :selection="editar? 'single' : 'none'"
        @selection="seleccionaFila"
    >
        <template v-slot:body-cell-horas="props">
            <q-td :props="props">
                {{ props.row.horas }}
                <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                    <q-popup-edit 
                        v-slot="scope" 
                        v-model="props.row.horas"
                        v-if="editar"                        
                        @update:modelValue="actualizarRol(props.row)"
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
        <template v-slot:body-cell-rol="props">
            <q-td :props="props">
                {{ props.row.rol }}
                <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                    <q-popup-edit 
                        v-slot="scope" 
                        v-model="props.row.rol"
                        v-if="editar"                        
                        @update:modelValue="actualizarRol(props.row)"
                        @hide="disableQPopupEdit"
                    >                    
                        <q-select
                            v-model="scope.value" 
                            :options="opcionesRol"
                            style="width: 100%;"
                            @keyup.enter="scope.set"                        
                            :display-value="`${ scope.value === '-' || scope.value === '' ? '-' : nombreRol(scope.value) }`"
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
    import PopUpIngresoNuevoCUrso from "src/components/componentesPAA/docencia/PopUpIngresoNuevoCurso.vue"

    export default defineComponent({
        components:{
            PopUpIngresoNuevoCUrso,
        },
        props: {
            asignaturasPlanificacion: Array,
            estadoPlanificacion: String,
            idPlanificacion: Number,
            editar: Boolean,
            opcion: String,
        },
        methods: {
            disableQPopupEdit() {
                this.disable = true;
            },
            actualizarRol(row) {                
                const copiaRow = { ...row };
                if (copiaRow.rol){
                    copiaRow.rol = copiaRow.rol.label || this.opcionesRol.find(opcion => opcion.value == copiaRow.rol).label;
                }
                this.$emit("updateAsignaturas", copiaRow);
                // row contiene los datos de la fila editada
            },
            nombreRol (rol) {                
                if (rol !== "-" && rol) {
                    return rol.label || rol;
                } else {
                    return "-";
                }
            },
        },
        // emits:["updateAsignaturas"],
        setup(props, {emit}) {
            const router = useRouter();
            const store = useStore();
            const asignaturasDepartamento = computed(() => store.state.planificacion.asignatura);           
            const selected = ref([]);
            const tab = ref("informacionBasica");
            const mostrar = ref("");
            const idPlanificacion = ref(props.idPlanificacion);
            const popUpNuevoCurso = ref(false);
            const quitarAsignatura = () => {                
                emit("deleteAsignatura", selected.value[0].idPlanificacion);
                selected.value = [];
            }
            const manejoNuevoCurso = (respuesta) => {                
                const opcion = props.opcion.charAt(0).toUpperCase() + props.opcion.slice(1);
                popUpNuevoCurso.value = false;
                const nuevaEstructuraAsignatura = {
                    id: respuesta.data.id,
                    nombre: respuesta.data.nombre,
                    codigo: respuesta.data.codigo,
                    departamento: respuesta.data.departamento,
                    estado: respuesta.data.estado,
                    id_ucampus: respuesta.data.id_ucampus,
                    semestre: respuesta.data.semestre,
                    modalidad: respuesta.data.modalidad,
                };

                // Crear el objeto con la nueva estructura                
                const nuevaAsignaturaModificada = {
                    planificacion: idPlanificacion.value,
                    asignatura: nuevaEstructuraAsignatura,
                    tipo: opcion,
                    semestre: respuesta.data.semestre,
                    rol: respuesta.data.rol,
                    cantidad_horas: respuesta.data.horas, // Asigna las horas
                    programa: "",
                    descripcion: "",
                    observacion: "",
                };

                if(respuesta.opcion == "guardar"){
                    emit("insertAsignatura", nuevaAsignaturaModificada);
                }
            }
            const cambiaTab = (value, event) => {                
                tab.value = value;
                //innerTab.value = "borrador";
            }   
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            }

            const asignatura = [
                {   
                    id: 1,
                    nombre: 'Asignatura_Test1',
                    codigo: 'SA1009',
                    estado: 'No asignado',
                    semestre: '1',
                },
                {
                    id: 2,
                    nombre: 'Asignatura2_Test1',
                    codigo: 'SA1026',
                    estado: 'Asignada',
                    semestre: '1',
                }

            ]
            const opciones = [
                {
                    name: "id",
                    label: "Id planificacion",
                    field: (row) => (row.idPlanificacion? row.idPlanificacion : "id"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "asignatura",
                    label: "Asignatura",
                    field: (row) => (row.nombre ? row.nombre : "Otro"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "codigo",
                    label: "Código",                    
                    field: (row) => (row.codigo ? row.codigo : "Cepd"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "semestre",
                    label: "Semestre",
                    field: (row) => (row.semestre ? row.semestre : "Sem"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "rol",
                    label: "Rol",
                    field: (row) => (row.rol ? row.rol : "-"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "horas",
                    label: "Horas estimadas",
                    field: (row) => (row.horas ? row.horas : "Sin"),
                    align: "left",
                    style: "white-space: normal",
                },
            ]
            const opcionesAsignatura = ref([]);
            // : ref('asignatura','codigo','semestre','rol','horas'),
            const columnasVisibles = ref([
                'asignatura',
                'codigo',
                'semestre',
                'rol',
                'horas'
            ]);
            return {
                disable: false,
                columnasVisibles,
                asignaturasDepartamento,
                opciones,                
                asignatura,
                selected,
                seleccionaFila: seleccionaFila,
                opcionesRol: [              
                    { label: "Responsable del curso", value: "Responsable del curso" },
                    { label: "Co-responsable", value: "Co-responsable" },
                    { label: "Parte del equipo", value: "Parte del equipo" },
                    { label: "Coordinador/a equipo docente", value: "Coordinador/a equipo docente" },
                ],
                cambiaTab,
                tab,
                asignaturasPlanificacion: toRef(props,"asignaturasPlanificacion"),
                editar: toRef(props, "editar"),
                manejoNuevoCurso,
                quitarAsignatura,
                popUpNuevoCurso,
                mostrar,
                opcionesAsignatura,
                ingresarCurso :() => {                    

                    opcionesAsignatura.value = props.asignaturasPlanificacion.map(elemento => {
                        let opcion = {
                            label : elemento.nombre,
                            value : elemento.id,
                            codigo: elemento.codigo
                        }
                        return opcion;
                    });                   
                    
                    popUpNuevoCurso.value = true;
                },
                idPlanificacion,
            };
        }        
    })
</script>

<style lang="sass">
.my-sticky-virtscroll-table
    height: 10px

    .q-table__top,
    .q-table__bottom,
    thead tr:first-child th
        background-color: #fcefd5

    thead tr th
        position: sticky
        z-index: 1

    thead tr:last-child th
        top: 1px
    thead tr:first-child th
        top: 0

    tbody
        scroll-margin-top: 1px
</style>