<template>    
    <q-dialog 
        v-model="mostrar" 
        persistent 
        transition-show="slide-up"
        transition-hide="slide-down"
        style="width: 2800px;"
        @before-show="limpiarFormulario" 
    > 
    
        <q-card style="width: 1000px; max-width: 80vw;">
            <q-card-section>
                <div class="text-h6 text-textoAzul">Ingresar nueva Actividad de Vinculación con el Medio a la Planificación Académica</div>
            </q-card-section>
            
            <q-separator />
            <q-card-section>

                <q-form @submit="handleClick('guardar')" class="text-textoAzul">
                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Nombre o descripción de la actividad:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-input
                                v-model="form.nombre"                                
                                style="width: 100%;"
                                :rules="[
                                    val => !!val || '* Este dato es requerido']"
                            />
                        </q-item-section>
                    </q-item>

                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Rol:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-select
                                v-model="form.rol"
                                :options="opcionesRol"
                                style="width: 100%;"
                                :rules="[
                                    val => !!val || '* Este dato es requerido']"
                            />
                        </q-item-section>
                    </q-item>
                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Unidad:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-select
                                v-model="form.unidad"
                                :options="opcionesUnidad"
                                style="width: 100%;"
                                :rules="[
                                    val => !!val || '* Este dato es requerido']"
                            />
                        </q-item-section>
                    </q-item>

                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Horas estimadas:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-input
                                v-model="form.horas"
                                mask="######"
                                style="width: 100%;"
                            />
                        </q-item-section>
                    </q-item>

                    <q-card-section>
                        <div class="row justify-end q-gutter-sm q-ma-md">
                            <q-btn
                                label="Cancelar"
                                color="primary"
                                size="md"
                                @click="handleClick('cancelar')"
                            />
                            <q-btn
                                label="Vinculemos"
                                color="secondary"
                                size="md"
                                @click="handleClick('guardar')"                                
                            />
                            <q-btn
                                label="Guardar cambios"
                                color="secondary"
                                size="md"
                                @click="handleClick('guardar')"
                                :disabled="isFormIncomplete"
                            />
                        </div>
                    </q-card-section>   
                </q-form>                
            </q-card-section>      
        </q-card>
    </q-dialog>
</template>

<script>
import { ref, computed, toRef, onMounted } from "vue";
import { useStore } from "vuex";

export default {
    computed:{
        isFormIncomplete() {
            // Verifica si alguno de los campos clave del formulario está vacío
            return !(            
                this.form.nombre &&
                this.form.unidad &&
                this.form.rol &&
                this.form.linea_accion &&
                this.form.frecuencia &&
                this.form.fecha_inicio &&
                this.form.fecha_fin &&
                this.form.horas
            );
        },
    },
    methods: {
        limpiarFormulario() {
            this.form.nombre = "";
            this.form.unidad = "";
            this.form.rol = "";
            this.form.linea_accion = "";
            this.form.frecuencia = "";
            this.form.fecha_inicio = "";
            this.form.fecha_fin = "";
            this.form.horas = "";
        },
    },
    props: {
        cursos: Array,
        mostrar: Boolean,
    },
    setup(props, { emit }) {
        const store = useStore();
        const miPlanificacion =computed(() => store.state.planificacion.planificacionAcademica);
        const form = ref({
            nombre      : "",
            rol         : "",
            unidad      : "",
            linea_accion: "",
            frecuencia  : "",
            fecha_inicio: "",
            fecha_fin   : "",
            horas       : ""
        });
        onMounted(() => {
            form.value.nombre       = "";
            form.value.rol          = "";
            form.value.unidad       = "";
            form.value.linea_accion = "";
            form.value.frecuencia   = "";
            form.value.fecha_inicio = "";
            form.value.fecha_fin    = "";
            form.value.horas        = "";
        });
        

        const handleClick = (opcion) => {
            let respuesta = {
                opcion : opcion,
                data: form.value,
            }
            
            emit("respuestaPopup", respuesta);
        };
        const mostrar = computed({
            get: () => props.mostrar,
            set: (value) => emit("update:mostrar", value),
        });
        return {
            miPlanificacion,
            form,
            handleClick,
            mostrar,            
            asignatura: null,
            semestre: null,
            rol: null,
            horasEstimadas: null,
            opcionesAsignatura: toRef(props, "cursos"),            
            opcionesUnidad: [              
                { label: "Dirección Vinculación con el Medio", value: 1 },
                { label: "Otra dirección", value: 2 },
                { label: "Departamentos", value: 3 },
                { label: "Carreras", value: 4 },
                { label: "Otra externa", value: 5 },
            ],            
            opcionesRol: [              
                { label: "Principal", value: 1 },
                { label: "Colaborador/a", value: 2 },
                { label: "Responsable productos", value: 3 },
            ],            
        };
    },
};
</script>