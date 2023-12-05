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
                <div class="text-h6 text-textoAzul">Ingresar observaciones a la Planificación Académica</div>
                <div class="text-caption text-grey">Académic@ {{ planificaciones.planificacionAcademico[0].usuario.nombre + ' ' + 
                    planificaciones.planificacionAcademico[0].usuario.apellido + ', periodo ' + planificaciones.planificacionAcademico[0].anio}}</div>
            </q-card-section>
            
            <q-separator />

            <q-card-section>
                <q-form @submit="handleClick('guardar')" class="text-textoAzul">
                    <q-item>
                        <q-item-section>        
                            <q-input
                                filled
                                v-model="observaciones"
                                label="Observación de la Planificación anual académica."
                                hint="Ingresar comentarios u observaciones a la planificación del academic@ para ser subsanadas."
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
                                :disable="observaciones.length <= 10"
                            />
                        </div>
                    </q-card-section>
                </q-form>
            </q-card-section>
        </q-card>
    </q-dialog>
    <q-dialog v-model="envio" persistent transition-show="scale" transition-hide="scale">
        <q-card class="my-card bg-teal-2" style="width: 990px; max-width: 80vw;">

            <q-card-section horizontal>
                <q-card-section>
                    <q-avatar color="white" text-color="cyan-8" icon="done" />
                </q-card-section>
            <q-card-section class="text-textoAzul">
                <div class="text-h6" v-if="usuario.perfil.planificacionAcademica == 'Jefe Departamento'">
                    <b>Estado de la Planificación actualizado. Enviado de vuelta al académic@ para subsanar</b>
                </div>
                <div class="text-h6" v-else>
                    <b>Estado de la Planificación actualizado?. Enviado de vuelta a jefe de departamento para correcciones</b>
                </div>
                
                Gracias por usar Colabora
            </q-card-section>
            </q-card-section> 
    
            <q-card-actions align="right" class="bg-white text-teal">
                <q-btn 
                    flat 
                    label="Volver al panel" 
                    @click="volver"
                />
            </q-card-actions>
            </q-card>
    </q-dialog>

    <br/>
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
            periodo: String,
            mostrar: Boolean,
        },
        setup(props, { emit }) {
            const router = useRouter();
            const store = useStore();
            const entrega = computed(() => store.state.entrega);
            const planificaciones = computed(() => store.state.planificacion.planificacionAcademica);
            const usuario = computed(() => store.state.usuarix.usuario);
            const observaciones = ref(null);
            const envio = ref(false);
            const handleClick = (opcion) => {
                if(opcion == "guardar") {
                    const observacion = {
                        'usuario' : usuario.value.id,
                        'planificacion' : planificaciones.value.planificacionAcademico[0].id,
                        'observacion' : observaciones.value
                    }

                    if(usuario.value.perfil.planificacionAcademica == "Jefe Departamento"){
                        store.dispatch("planificacion/observaciones/workflowJefeDptoRechaza", observacion);
                    }else{
                        console.log("dispatch workflowDireccionRechaza")
                    }
                    envio.value = true;
                }
                //emit("respuestaPopup", respuesta);
            };
            const volver = async () => {
                envio.value = false;
                await store.dispatch("planificacion/planificacionAcademica/planificacionesDepartamento", props.periodo)
                emit("respuestaPopup");
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
                usuario,
                periodo: toRef(props, "periodo"),
                mostrar,
                handleClick,
                observaciones,
                envio,
                entrega,
                planificaciones,
                volver,
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