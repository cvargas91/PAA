<template>    
    <PopUpIngresoNuevaVinculacionCEMedio
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevaActividadVinculacion"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar nueva actividad"
            color="positive"
            no-caps
            @click="ingresarActividadVinculacion"
        />
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            :label="truncarLabel(selected[0].nombre_actividad)"
            color="btnCancelar"
            no-caps
            @click="quitarActividadVinculacion"
        />
    </div>
    <!-- vinculaciones-> {{ vinculacionCEMedio }} -->
    <q-table
        v-model:selected="selected"
        :rows="vinculacionCEMedio"
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
                    @update:modelValue="actualizarVinculacionCEMedio(props.row)"
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
    <template v-slot:body-cell-rol="props">
        <q-td :props="props">
            {{ props.row.rol }}
            <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.rol"
                    v-if="editar"                    
                    @update:modelValue="actualizarVinculacionCEMedio(props.row)"
                    @hide="disableQPopupEdit"
                >   
                    <q-select
                        v-model="scope.value" 
                        :options="opcionesRol"
                        style="width: 100%;"
                        @keyup.enter="scope.set"                        
                        :display-value="`${ scope.value === '-' ? '-' : nombreRol(scope.value) }`"
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
                    @update:modelValue="actualizarVinculacionCEMedio(props.row)"
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
    <template v-slot:body-cell-unidad="props">
        <q-td :props="props">
            {{ nombreUnidad(props.row.unidad) }}
                <q-popup-edit 
                    v-slot="scope" 
                    v-model="props.row.unidad"
                    v-if="editar"                    
                    @update:modelValue="actualizarVinculacionCEMedio(props.row)"
                    @hide="disableQPopupEdit"
                >
                    <q-select
                        v-model="scope.value" 
                        :options="opcionesUnidad"
                        style="width: 100%;"
                        @keyup.enter="scope.set"                        
                        :display-value="nombreUnidad(scope.value)"
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
    import PopUpIngresoNuevaVinculacionCEMedio from "src/components/componentesPAA/vinculacion/PopUpIngresoNuevaVinculacionCEMedio.vue"

    export default defineComponent({
        components:{
            PopUpIngresoNuevaVinculacionCEMedio,
        },
        props: {
            vinculacionCEMedio: Array,
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
            actualizarVinculacionCEMedio(row) {
                const copiaRow = { ...row };
                const unidadesPermitidas = this.opcionesUnidad.map(opcion => opcion.value);
                if (copiaRow.rol){
                    copiaRow.rol = copiaRow.rol.label || this.opcionesRol.find(opcion => opcion.value == copiaRow.rol).label;
                }

                if (copiaRow.unidad){                    
                    if (!unidadesPermitidas.includes(copiaRow.unidad)){
                        copiaRow.unidad = copiaRow.unidad.value || this.opcionesUnidad.find(opcion => opcion.label == copiaRow.unidad).value;
                    }
                }
                this.$emit("updateVinculaciones", copiaRow);
                // row contiene los datos de la fila editada
            },
            nombreRol (rol) {
                if (rol !== "-" && rol) {                    
                    return rol.label || rol;
                } else {
                    return "-";
                }
            },
            nombreUnidad (unidad){                
                if (unidad !== "-" && unidad) {
                    return unidad.label || this.opcionesUnidad.find(opcion => opcion.value == unidad).label;
                } else {
                    return "-";
                }
            },
            nombreUnidadObjeto (unidad){                
                if(unidad){
                    if (unidad == "1" || unidad == 1)
                        return "Dirección Vinculación con el Medio";
                    if (unidad == "3" || unidad == 3)
                        return "Otra dirección"
                    if (unidad == "2" || unidad == 2)
                        return "Departamentos"
                    if (unidad == "4" || unidad == 4)
                        return "Carreras"
                    if (unidad == "5" || unidad == 5)
                        return "Otra externa"                    
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
            const quitarActividadVinculacion = () => {                
                emit("deleteVinculacion", selected.value[0].id);
                selected.value = [];
            };
            const manejoNuevaActividadVinculacion = (respuesta) => {
                popUpNuevoCurso.value = false;
                if(respuesta.opcion == "guardar"){                    

                    const nuevaActividadVinculacion = {
                        planificacion: idPlanificacion.value,
                        nombre_actividad: respuesta.data.nombre,
                        cantidad_horas: respuesta.data.horas,
                        unidad:respuesta.data.unidad.value,
                        rol:respuesta.data.rol.value,
                        linea_accion:respuesta.data.linea_accion.value,
                        frecuencia:respuesta.data.frecuencia.label,
                        fecha_inicio:!respuesta.data.fecha_inicio.length ? null : respuesta.data.fecha_inicio.replace(/\//g, '-'),
                        fecha_fin:   !respuesta.data.fecha_fin.length ? null : respuesta.data.fecha_fin.replace(/\//g, '-'),
                    };                    
                    emit("insertVinculacion", nuevaActividadVinculacion);

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
                    label: "Nombre o Descripción de la actividad",
                    field: (row) => (row.nombre_actividad ? row.nombre_actividad : "Otro"),
                    align: "left",
                    sortable: true,
                    style: "white-space: normal; max-width: 20px; word-wrap: break-word;",
                },
                {
                    name: "rol",
                    label: "Rol",
                    field: (row) => (row.rol ? row.rol : "-"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "unidad",
                    label: "Unidad",
                    field: (row) => {
                        if (row.unidad){
                            if (row.unidad == "1")
                                return "Dirección Vinculación con el Medio"
                            if (row.unidad == "2")
                                return "Otra dirección"
                            if (row.unidad == "3")
                                return "Departamentos"
                            if (row.unidad == "4")
                                return "Carreras"
                            if (row.unidad == "5")
                                return "Otra externa"
                            
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
                'unidad',
                'rol',
                'horas'
            ]);
            return {                
                opciones,                                
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                vinculacionCEMedio: toRef(props,"vinculacionCEMedio"),
                manejoNuevaActividadVinculacion,
                quitarActividadVinculacion,
                columnasVisibles,
                popUpNuevoCurso,
                mostrar,
                opcionesAsignatura,
                ingresarActividadVinculacion :() => {                    
                    selected.value = [];
                    opcionesAsignatura.value = props.vinculacionCEMedio.map(elemento => {
                        let opcion = {
                            label : elemento.nombre,
                            value : elemento.id,
                            codigo: elemento.codigo
                        }
                        return opcion;
                    })                    
                    popUpNuevoCurso.value = true;
                },
                opcionesUnidad: [              
                    { label: "Dirección Vinculación con el Medio", value: "1" },
                    { label: "Otra dirección"                    , value: "2" },
                    { label: "Departamentos"                     , value: "3" },
                    { label: "Carreras"                          , value: "4" },
                    { label: "Otra externa"                      , value: "5" },
                ],
                opcionesRol: [
                    { label: "Principal", value: "Principal" },
                    { label: "Colaborador/a", value: "Colaborador/a" },
                    { label: "Responsable productos", value: "Responsable productos" },
                ],
                disable: false,
            };
        }        
    })
</script>