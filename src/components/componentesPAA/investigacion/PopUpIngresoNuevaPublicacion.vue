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
                <div class="text-h6 text-textoAzul">Ingresar nueva Publicación a la Planificación Académica</div>
            </q-card-section>
            
            <q-separator />
            <q-card-section>

                <q-form @submit="handleClick('guardar')" class="text-textoAzul">
                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Descripción de la actividad:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-input
                                v-model="form.descripcion"                                
                                style="width: 100%;"
                                :rules="[
                                    val => !!val || '* Este dato es requerido']"
                            />
                        </q-item-section>
                    </q-item>

                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Calidad de autoría:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-select
                                v-model="form.autoria"
                                :options="opcionesAutoria"
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
                this.form.autoria &&
                this.form.horas
            );
        },
    },
    methods: {
        limpiarFormulario() {
            this.form.descripcion = "";
            this.form.autoria = "";
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
            descripcion : "",
            autoria : "",
            horas: ""
        });
        onMounted(() => {
            form.value.descripcion = "";
            form.value.autoria = "";
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
            opcionesAutoria: [              
                { label: "Autor libro", value: 1 },
                { label: "Editor o compilador", value: 2 },
                { label: "Primer autor capítulo", value: 3 },
                { label: "Co-autor capítulo", value: 4 },
            ],            
        };
    },
};
</script>