<template>    
    <q-dialog 
        v-model="mostrar" 
        persistent 
        transition-show="slide-up"
        transition-hide="slide-down"
        style="width: 2800px;"
        @before-show="limpiarFormulario" 
    >
        <q-card style="width: 800px; max-width: 80vw;">
            <q-card-section>
                <div class="text-h6 text-textoAzul">Vincular Planificación con compromisos del departamento</div>
                <div class="text-caption text-grey">Académic@ {{ planificaciones.planificacionAcademico[0].usuario.nombre + ' ' + 
                    planificaciones.planificacionAcademico[0].usuario.apellido + ', periodo ' + planificaciones.planificacionAcademico[0].anio}}</div>
            </q-card-section>
            <!-- accion {{ accion.detalleAccionesReporte }} -->
            <q-separator />

            <q-card-section>
                <q-form @submit="handleClick('guardar')" class="text-textoAzul">
                    <q-item>
                        <q-item-section>                      
                            <q-item-label><b>Acción responsable</b>:</q-item-label>
                        </q-item-section>

                        <q-item-section>                      
                            <q-select
                                v-model="compromiso"
                                :options="accion.detalleAccionesReporte"
                                style="width: 100%;"
                                option-value="id"
                                option-label="accion"
                                :display-value="`${ compromiso !== '' ? accionSeleccionada(compromiso) : 'Seleccione una acción' }`"
                            >
                                <template v-slot:option="scope">
                                    <q-item v-bind="scope.itemProps">
                                        <q-item-section>
                                            <q-item-label>{{ scope.opt.accion.titulo }}</q-item-label>
                                            <q-item-label caption>{{ scope.opt.accion.id_uaysen }}</q-item-label>
                                        </q-item-section>
                                    </q-item>
                                </template>
                            </q-select>
                        </q-item-section>
                    </q-item>

                    <q-card-section>
                        <div class="row justify-end q-gutter-sm q-ma-md">
                            <q-btn
                                label="Cancelar"
                                color="primary"
                                size="md"
                                no-caps
                                @click="handleClick('cancelar')"
                            />
                            <q-btn
                                label="Vincular Acción con Planificación"
                                color="secondary"
                                size="md"
                                no-caps
                                @click="handleClick('guardar')"
                                :disable="compromiso === ''"
                            />
                        </div>
                    </q-card-section>
                </q-form>
            </q-card-section>
        </q-card>
    </q-dialog>
    <q-dialog v-model="envio" persistent transition-show="scale" transition-hide="scale">
        <q-card class="my-card bg-teal-2" style="width: 990px; max-width: 80vw;">
            <!-- <q-card-section>
                <div class="text-h6">Persistent</div>
            </q-card-section> -->
    
            <q-card-section horizontal>
                <q-card-section>
                    <q-avatar color="white" text-color="cyan-8" icon="done" />
                </q-card-section>
            <q-card-section class="text-textoAzul">
                <div class="text-h6">
                    <b>Planificación actualizada. Acción {{compromiso.accion.id_uaysen}} relacionada con la planificación académica</b>
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
                this.compromiso = "";
                this.envio = false;
            },
            accionSeleccionada (compromiso) {
                return compromiso.accion.titulo;
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
            const accion = computed(() => store.state.accion);
            const usuario = computed(() => store.state.usuarix.usuario);
            const compromiso = ref(null);
            const envio = ref(false);

            const handleClick = (opcion) => {
                let respuesta = {
                    opcion : opcion,
                    data: compromiso.value,
                }
                if(opcion == "guardar") {
                    const compromisoDpto = {
                        'usuario' : usuario.value.id,
                        'planificacion' : planificaciones.value.planificacionAcademico[0].id,
                        'accion' : compromiso.value.accion.id,
                    }
                    store.dispatch("planificacion/planificacionAcademica/vincularCompromisos", compromisoDpto);
                    envio.value = true;
                } else {
                    emit("respuestaPopup", respuesta);
                }                
            };
            const volver = async () => {
                envio.value = false;
                await store.dispatch("planificacion/planificacionAcademica/planificacionesDepartamento", props.periodo)
                emit("respuestaPopup", compromiso.value);
            };
            const mostrar = computed({
                get: () => props.mostrar,
                set: (value) => emit("update:mostrar", value),
            });

            onMounted(() => {
                compromiso.value = "";
                envio.value = false;
            });
            return {
                accion,
                periodo: toRef(props, "periodo"),
                mostrar,
                handleClick,
                compromiso,
                envio,
                entrega,
                planificaciones,
                volver,
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
                        'observacion' : compromiso.value
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