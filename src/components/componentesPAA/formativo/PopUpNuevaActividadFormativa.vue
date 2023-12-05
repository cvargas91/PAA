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
                <div class="text-h6 text-textoAzul">Ingresar nueva Actividad Formativa a la Planificación Académica</div>
            </q-card-section>
            
            <q-separator />
            <q-card-section>

                <q-form @submit="handleClick('guardar')" class="text-textoAzul">
                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Nombre de la actividad formativa:</b></q-item-label>
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
                            <q-item-label><b>Institución que realiza la actividad:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-input
                                v-model="form.institucion"                                
                                style="width: 100%;"
                                :rules="[
                                    val => !!val || '* Este dato es requerido']"
                            />
                        </q-item-section>
                    </q-item>
                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Fecha inicio actividad:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>
                            <q-input filled v-model="form.fecha_inicio" mask="date">
                                <template v-slot:append>
                                    <q-icon name="event" class="cursor-pointer">
                                        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                            <q-date v-model="form.fecha_inicio">
                                                <div class="row items-center justify-end">
                                                    <q-btn v-close-popup label="Ok!" color="possitive" flat />
                                                </div>
                                            </q-date>
                                        </q-popup-proxy>
                                    </q-icon>
                                </template>
                            </q-input>                                    
                        </q-item-section>
                    </q-item>

                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Fecha termino actividad:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-input filled v-model="form.fecha_fin" mask="date">
                                <template v-slot:append>
                                    <q-icon name="event" class="cursor-pointer">
                                        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                            <q-date v-model="form.fecha_fin">
                                                <div class="row items-center justify-end">
                                                    <q-btn v-close-popup label="Ok!" color="possitive" flat />
                                                </div>
                                            </q-date>
                                        </q-popup-proxy>
                                    </q-icon>
                                </template>
                            </q-input> 
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
                this.form.institucion &&
                this.form.fecha_inicio &&
                this.form.fecha_fin &&
                this.form.horas
            );
        },
    },
    methods: {
        limpiarFormulario() {
            this.form.nombre = "";
            this.form.institucion = "";
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
            nombre : "",
            institucion : "",
            fecha_inicio : "",
            fecha_fin : "",
            horas: ""
        });
        onMounted(() => {
            form.value.nombre = "";
            form.value.institucion = "";
            form.value.fecha_inicio = "";
            form.value.fecha_fin = "";
            form.value.horas = "";
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
        };
    },
};
</script>