<template>    
    <PopUpIngresoNuevoPrograma
        :cursos="opcionesAsignatura"
        :mostrar="popUpNuevoCurso"
        @update:mostrar="popUpNuevoCurso = $event"
        @respuestaPopup="manejoNuevoPrograma"
    />
    <div class="q-gutter-sm q-mt-sm" v-if="editar">
        <q-btn
            class="q-ma-sm"
            label="Agregar programa a Planificación"
            color="positive"
            @click="ingresarPrograma"
            no-caps
        />
        <q-btn
            v-if="selected.length"
            class="q-ma-sm"
            :label="'Quitar Programa con código ' + selected[0].asignatura.codigo"
            color="btnCancelar"
            @click="quitarPrograma"
            no-caps
        />
    </div>
    <!-- {{ programas }} ¡?? -->
    <q-table
        v-model:selected="selected"
        :rows="programas"
        :columns="opciones"
        :visible-columns="columnasVisibles"
        virtual-scroll
        :rows-per-page-options="[0]"
        style="height: 300px"
        row-key="id"
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
                        @update:modelValue="actualizarPrograma(props.row)"
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
        <template v-slot:body-cell-programa="props">
            <q-td :props="props">
                {{ props.row.programa }}
                <!-- <q-popup-edit v-model="props.row.horas" @save="actualizarRol(props.row)"> -->
                    <q-popup-edit 
                        v-slot="scope" 
                        v-model="props.row.programa"
                        v-if="editar"                        
                        @update:modelValue="actualizarPrograma(props.row)"
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
        <template v-slot:body-cell-programacion="props">
            <q-td :props="props">
                {{ props.row.descripcion }}                
                    <q-popup-edit 
                        v-slot="scope" 
                        v-model="props.row.descripcion"
                        v-if="editar"                        
                        @update:modelValue="actualizarPrograma(props.row)"
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
    </q-table>
</template>

<script>    
    import { ref, toRef, computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    import PopUpIngresoNuevoPrograma from "src/components/componentesPAA/docencia/PopUpIngresoNuevoPrograma.vue"

    export default defineComponent({
        components:{
            PopUpIngresoNuevoPrograma,
        },
        props: {
            programas: Array,
            estadoPlanificacion: String,
            idPlanificacion: Number,
            editar: Boolean,
            opcion: String,
        },
        methods: {
            disableQPopupEdit() {
                this.disable = true;
            },
            actualizarPrograma(row) {
                const copiaRow = { ...row };
                this.$emit("updateProgramas", copiaRow);                
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
            const quitarPrograma = () => {
                emit("deletePrograma", selected.value[0].id);
                selected.value = [];
            }
            const manejoNuevoPrograma = (respuesta) => {
                popUpNuevoCurso.value = false;
                
                if(respuesta.opcion == "guardar"){
                    
                    const nuevaEstructuraAsignatura = {
                        id:             respuesta.data.asignatura.id,
                        nombre:         respuesta.data.asignatura.nombre,
                        codigo:         respuesta.data.asignatura.codigo,
                        departamento:   respuesta.data.asignatura.departamento,
                        estado:         respuesta.data.asignatura.estado,
                        id_ucampus:     respuesta.data.asignatura.id_ucampus,
                        semestre:       respuesta.data.asignatura.semestre,
                        modalidad:      respuesta.data.asignatura.modalidad,
                    };

                    const nuevoPrograma = {
                        planificacion: idPlanificacion.value,
                        asignatura: nuevaEstructuraAsignatura,
                        tipo: "Programa",
                        semestre: "1",
                        cantidad_horas: respuesta.data.horas,
                        programa: respuesta.data.programa,
                        descripcion: respuesta.data.programacion,
                        observacion: respuesta.data.observacion,
                    };

                    emit("insertPrograma", nuevoPrograma);
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
                    name: "semestre",
                    label: "Semestre",
                    field: (row) => (row.semestre ? row.semestre : "Sem"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "codigo",
                    label: "Código",
                    field: (row) => (row.asignatura ? row.asignatura.codigo : "Cpd"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "programa",
                    label: "Programa",
                    field: (row) => (row.programa ? row.programa : "Otro"),
                    align: "left",
                    sortable: true,
                    style: "white-space: normal; max-width: 20px; word-wrap: break-word;",
                },
                {
                    name: "programacion",
                    label: "Programación u otro",
                    field: (row) => (row.descripcion ? row.descripcion : "Sem"),
                    align: "left",
                    style: "white-space: normal; max-width: 80px; word-wrap: break-word;",
                },
                {
                    name: "observacion",
                    label: "Observaciones",
                    field: (row) => (row.observacion ? row.observacion : "Sem"),
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
            const columnasVisibles = ref([
                'asignatura',
                'codigo',
                'semestre',
                'programa',
                'programacion',
                'observaciones',
                'horas'
            ]);
            const opcionesAsignatura = ref([]);
            return {
                disable: false,                
                columnasVisibles,
                opciones,
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                programas: toRef(props,"programas"),
                manejoNuevoPrograma,
                quitarPrograma,
                popUpNuevoCurso,
                mostrar,
                opcionesAsignatura,
                ingresarPrograma :() => {
                    opcionesAsignatura.value = props.programas.map(elemento => {
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