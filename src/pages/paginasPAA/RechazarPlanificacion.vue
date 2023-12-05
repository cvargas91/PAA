<template>
    ¿{{ entrega }}?
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
                <div class="text-h6 text-textoAzul">Ingresar observaciones a la Planificación Académica</div>
                <div class="text-caption text-grey">Subtítulo aquí</div>
            </q-card-section>
            
            <q-separator />

            <q-card-section>
                <q-form @submit="handleClick('guardar')" class="text-textoAzul">
                    <q-item>
                        <q-item-section>
                            <q-item-label><b>Descripción de la Actividad</b></q-item-label>
                        </q-item-section>
                        <q-item-section>        
                            <q-input
                                filled
                                v-model="observaciones"
                                :label="'Observación de la Planificación anual, académicx ' +  
                                    planificaciones.planificacionAcademico[0].usuario.nombre + ' ' + 
                                    planificaciones.planificacionAcademico[0].usuario.apellido + ', periodo ' + planificaciones.planificacionAcademico[0].anio"
                                hint="Ingresar comentarios u observaciones a la planificación del academicx para ser subsanadas"
                                lazy-rules
                                type="textarea"
                                :rules="[
                                    (val) => (val && val.length > 10) || 'Escriba por lo menos 10 caracteres',
                                ]"
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
                                label="Enviar observaciones"
                                color="secondary"
                                size="md"
                                @click="handleClick('guardar')"
                            />
                        </div>
                    </q-card-section>
                </q-form>
            </q-card-section>
        </q-card>
    </q-dialog>
    <q-dialog v-model="envio" persistent transition-show="scale" transition-hide="scale">
        <q-card class="bg-teal text-white" style="width: 300px">
            <q-card-section>
                <div class="text-h6">Persistent</div>
            </q-card-section>
    
            <q-card-section horizontal>
                <q-card-section>
                    <q-avatar color="white" text-color="cyan-8" icon="done" />
                </q-card-section>
            <q-card-section class="text-textoAzul">
                <div class="text-h6">
                    <b>Estado de la Planificación actualizado. Enviado de vuelta al académicx para subsanar</b>
                </div>
                Gracias por usar Colabora
            </q-card-section>
            </q-card-section> 
    
            <q-card-actions align="right" class="bg-white text-teal">
                <q-btn flat label="OK" v-close-popup />
            </q-card-actions>
            </q-card>
    </q-dialog>
</template>
<script>
    import { ref, computed, toRef, onMounted } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";

    export default {
        methods: {
            limpiarFormulario() {            
                this.observaciones = "";
                this.envio = false;
            },
        },
        props: {
            cursos: Array,
            mostrar: Boolean,
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const entrega = computed(() => store.state.entrega);
            const planificaciones = computed(() => store.state.planificacion.planificacionAcademica);            
            const usuario = computed(() => store.state.usuarix.usuario);
            const observaciones = ref(null);
            const envio = ref(false);
            const handleClick = (opcion) => {
                let respuesta = {
                    opcion : opcion,
                    data: observaciones.value,
                }
                //emit("respuestaPopup", respuesta);
            };
            const mostrar = computed({
                get: () => props.mostrar,
                set: (value) => emit("update:mostrar", value),
            });

            onMounted(() => {
                observaciones.value = "";
                envio.value = false;
            });
            return {        
                mostrar,
                handleClick,
                observaciones,
                envio,
                entrega,
                planificaciones,
                volver: () => {
                    router.push("panelJefeDepartamento")
                },
                limpiaBandeja: () => {
                    let rutaDestino =
                        entrega.value.aRechazar.mandante == "UPCI"
                        ? "bandejaUPCI"
                        : "bandejaEntregas";
                    store.dispatch("entrega/limpiaEntregas");
                    router.push(rutaDestino);
                },
                onSubmit: () => {
                    const observacion = {
                        'usuario' : usuario.value.id,
                        'planificacion' : planificaciones.value.planificacionAcademico[0].id,
                        'observacion' : observaciones.value
                    }
                    if (confirm("¿Enviar retroalimentación?")) {
                        if(usuario.value.perfil.planificacionAcademica == "Jefe Departamento"){
                            store.dispatch("planificacion/observaciones/workflowJefeDptoRechaza", observacion);
                        }else{
                            console.log("dispatch workflowDireccionRechaza")
                        }
                    }
                },
            };
        },
    };
</script>