<template>    
    <PopUpIngresoNuevoProyecto
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevoProyecto"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar un Proyecto a Planificación"
            color="positive"
            no-caps
            @click="ingresarProyecto"
        />        
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            :label="truncarLabel(selected[0].nombre_proyecto)"
            color="btnCancelar"
            no-caps
            @click="quitarProyecto"
        />
    </div>    
    <q-table
        v-model:selected="selected"
        :rows="proyectos"
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
                    @update:modelValue="actualizarProyecto(props.row)"
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
    <template v-slot:body-cell-estado="props">
        <q-td :props="props">
            {{nombreEstado(props.row.estado_proyecto)}}
            <!-- {{ props.row.estado_proyecto }} -->
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.estado_proyecto"
                    v-if="editar"
                    @hide="disableQPopupEdit"
                    @update:modelValue="actualizarProyecto(props.row)"
                >   
                    <q-select
                        v-model="scope.value" 
                        :options="opcionesEstadoProyecto"
                        style="width: 100%;"
                        @keyup.enter="scope.set"
                        :display-value="nombreEstado(scope.value)"
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
    <template v-slot:body-cell-fuente="props">
        <q-td :props="props">
            {{ props.row.fuente_financiamiento }}                
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.fuente_financiamiento"
                    v-if="editar"
                    @hide="disableQPopupEdit"
                    @update:modelValue="actualizarProyecto(props.row)"
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
    <template v-slot:body-cell-nombre="props">
        <q-td :props="props">
            {{ props.row.nombre_proyecto }}                
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.nombre_proyecto"
                    v-if="editar"
                    @hide="disableQPopupEdit"
                    @update:modelValue="actualizarProyecto(props.row)"
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
    <template v-slot:body-cell-rol="props">
        <q-td :props="props">
            <!-- {{ nombreRol(props.row.rol) }} -->
            {{ props.row.rol }}
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.rol"
                    v-if="editar"
                    @hide="disableQPopupEdit"
                    @update:modelValue="actualizarProyecto(props.row)"
                >   
                    <q-select
                        v-model="scope.value" 
                        :options="opcionesRol"
                        style="width: 100%;"
                        @keyup.enter="scope.set"                        
                        :display-value="nombreRol(scope.value)"
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
    import PopUpIngresoNuevoProyecto from "src/components/componentesPAA/investigacion/PopUpIngresoNuevoProyecto.vue"

    export default defineComponent({
        components:{
            PopUpIngresoNuevoProyecto,
        },
        props: {
            proyectos: Array,
            estadoPlanificacion: String,
            idPlanificacion: Number,
            editar: Boolean,
            opcion: String,
        },
        computed: {
            truncarLabel() {
                const label = "Quitar Proyecto: "
                return (nombre_proyecto) => {
                    if (nombre_proyecto.length > 60) {
                        return label + nombre_proyecto.substring(0, 60) + '....';
                    }
                    return label + nombre_proyecto;
                };
            },
        },
        methods: {
            disableQPopupEdit() {
                this.disable = true;
            },
            nombreRol (rol) {
                if (rol !== "-" && rol) {
                    return rol.label || rol;
                } else {
                    return "-";
                }
            },
            nombreEstado (estado){
                if (estado !== "-" && estado) {
                    return estado.label || this.opcionesEstadoProyecto.find(opcion => opcion.value == estado).label;
                } else {
                    return "-";
                }
            },
            actualizarProyecto(row) {
                const copiaRow = { ...row };
                
                if (copiaRow.rol){
                    copiaRow.rol = copiaRow.rol.label || this.opcionesRol.find(opcion => opcion.value == copiaRow.rol).label;
                } 
                if (copiaRow.estado_proyecto){
                    if (copiaRow.estado_proyecto !== '1' && copiaRow.estado_proyecto !== '2'){
                        copiaRow.estado_proyecto = copiaRow.estado_proyecto.value || this.opcionesEstadoProyecto.find(opcion => opcion.label == copiaRow.estado_proyecto).value;
                    }
                }
                this.$emit("updateProyectos", copiaRow);
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
            const quitarProyecto = () => {
                emit("deleteProyecto", selected.value[0].id);
                selected.value = [];
            };
            const manejoNuevoProyecto = (respuesta) => {
                popUpNuevoCurso.value = false;
                if(respuesta.opcion == "guardar"){

                    const nuevoProyecto = {
                        planificacion: idPlanificacion.value,
                        tipo: "Proyecto",
                        nombre_proyecto: respuesta.data.proyecto,
                        descripcion: "",
                        cantidad_horas: respuesta.data.horas,
                        estado_proyecto:respuesta.data.estado.value,
                        rol:respuesta.data.rol.label,
                        autoria: null,
                        fuente_financiamiento: respuesta.data.fuente,

                    };

                    emit("insertProyecto", nuevoProyecto);
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
                    label: "Nombre proyecto Investigación",
                    field: (row) => (row.nombre_proyecto ? row.nombre_proyecto : "Otro"),
                    align: "left",
                    sortable: true,
                    style: "white-space: normal; max-width: 20px; word-wrap: break-word;",
                },
                {
                    name: "estado",
                    label: "Estado",
                    field: (row) => {                        
                        if(row.estado_proyecto){
                            if (row.estado_proyecto == "1")
                                return "Preparación y presentación";
                            if (row.estado_proyecto == "2")
                                return "Aprobado y en desarrollo"
                        }

                    },
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
                    name: "fuente",
                    label: "Fuente de Financiamiento",
                    field: (row) => (row.fuente_financiamiento ? row.fuente_financiamiento : "Sem"),
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
                'estado',
                'fuente',
                'rol',
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
                proyectos: toRef(props,"proyectos"),
                manejoNuevoProyecto,
                columnasVisibles,
                quitarProyecto,
                popUpNuevoCurso,
                mostrar,
                opcionesAsignatura,
                ingresarProyecto :() => {
                    selected.value = [];
                    opcionesAsignatura.value = props.proyectos.map(elemento => {
                        let opcion = {
                            label : elemento.nombre,
                            value : elemento.id,
                            codigo: elemento.codigo
                        }
                        return opcion;
                    })
                    popUpNuevoCurso.value = true;
                },
                opcionesEstadoProyecto: [              
                    { label: "Preparación y presentación", value: "1" },
                    { label: "Aprobado y en desarrollo"  , value: "2" },
                ],
                opcionesRol: [
                    { label: "Investigador/a principal", value: "Investigador/a principal" },
                    { label: "Co-investigador/a", value: "Co-investigador/a" },
                    { label: "Responsable de Productos", value: "Responsable de Productos" },
                ],
            };
        }        
    })
</script>