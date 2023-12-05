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
                <div class="text-h6 text-textoAzul">Ingresar nuevo Proyecto a la Planificación Académica</div>
            </q-card-section>
            
            <q-separator />
            <q-card-section>

                <q-form @submit="handleClick('guardar')" class="text-textoAzul">
                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Proyecto de Invetigación:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-input
                                v-model="form.proyecto"                                
                                style="width: 100%;"
                                :rules="[
                                    val => !!val || '* Este dato es requerido']"
                            />
                        </q-item-section>
                    </q-item>

                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Estado:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-select
                                v-model="form.estado"
                                :options="opcionesEstado"
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
                            />
                        </q-item-section>
                    </q-item>

                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Fuente Financiamiento:</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-input
                                v-model="form.fuente"                                
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
                                :rules="[
                                    val => !!val || '* Este dato es requerido']"
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
                this.form.proyecto &&
                this.form.estado &&
                this.form.horas &&
                this.form.fuente
            );
        },
    },
    methods: {
        limpiarFormulario() {            
            this.form.proyecto = "";
            this.form.estado = "";
            this.form.rol = "";
            this.form.fuente = "";
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
            proyecto : "",
            estado : "",
            rol : "",
            fuente : "",            
            horas: ""
        });
        onMounted(() => {
            form.value.proyecto = "";
            form.value.estado = "";
            form.value.rol = "";
            form.value.fuente = "";
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
            opcionesEstado: [              
                { label: "Preparación y presentación", value: "1" },
                { label: "Aprobado y en desarrollo", value: "2" },
            ],
            opcionesRol: [              
                { label: "Investigador/a principal", value: "Investigador/a principal" },
                { label: "Co-investigador/a", value: "Co-investigador/a" },
                { label: "Responsable de productos", value: "Responsable de Productos" },
            ],
        };
    },
};
</script>