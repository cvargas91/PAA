<template>
    <PopupCancelarPlanificacion
        :mostrar="mostrarPopupCancelar"
        @update:mostrar="mostrarPopupCancelar = $event"
        @respuestaPopup="handlerPopupCancelar"
    />
    <PopUpRechazarPlanificacion
        v-if="planificacion.planificacionAcademico"
        :periodo="planificacion.planificacionAcademico[0].anio"
        :mostrar="mostrarPopUpRechazo"        
        @update:mostrar="mostrarPopUpRechazo = $event"
        @respuestaPopup="manejoRechazo"
    />
    <div class="" v-if="planificacion.planificacionAcademico">         
        <q-card class="">
            <div class="text-h4 text-textoAzul">
                Planificación Anual Académica
            </div>
            <q-separator></q-separator>
            
            <q-carousel
                v-model="slide"
                vertical
                transition-prev="slide-down"
                transition-next="slide-up"
                swipeable
                animated
                control-color="btnContinuar"
                navigation-icon="radio_button_unchecked"
                navigation
                padding
                height="550px"
                class="shadow-1 rounded-borders"
                infinite
                ref="carousel"
            >
                <q-carousel-slide name="infoBasica" class="">
                    <InformacionBasica
                            :planificacionAcademico="planificacion.planificacionAcademico[0]"
                            :estadoPlanificacion="planificacion.planificacionAcademico[0].estado"
                            :opcion="planificacion.planificacionAcademicaEdicion ? 'edicion' : 'vista'"
                            :usuario="usuario.perfil.planificacionAcademica != 'Académico' ? planificacion.planificacionAcademico[0].usuario : usuario"
                    />
                </q-carousel-slide>
                <q-carousel-slide name="docencia" class="">
                    <!-- :planificacionAcademico="planificacion.planificacionAcademico[0].planificaciones_docencia" -->
                    <Docencia
                        :idPlanificacion ="planificacion.planificacionAcademico[0].id"
                        :cursosAcademico="cursos.misCursos"
                        :planificacionAcademico="!planificacion.planificacionAcademicaEdicion ? 
                            planificacion.planificacionAcademico[0].planificaciones_docencia :
                            planificacion.planificacionAcademicaEdicion[0].planificaciones_docencia"
                        :estadoPlanificacion="planificacion.planificacionAcademico[0].estado"
                        :opcion="planificacion.planificacionAcademicaEdicion ? true : false"
                        :periodo="planificacion.planificacionAcademico[0].anio"
                    />
                </q-carousel-slide>
                <q-carousel-slide name="investigacion" class="">
                    <!-- :investigaciones="planificacion.planificacionAcademico[0].planificaciones_investigacion" -->
                    <Investigacion
                        :idPlanificacion ="planificacion.planificacionAcademico[0].id"
                        :investigaciones="!planificacion.planificacionAcademicaEdicion ? 
                            planificacion.planificacionAcademico[0].planificaciones_investigacion :
                            planificacion.planificacionAcademicaEdicion[0].planificaciones_investigacion"
                        :estadoPlanificacion="planificacion.planificacionAcademico[0].estado"
                        :opcion="planificacion.planificacionAcademicaEdicion ? true : false"
                    />
                </q-carousel-slide>
                <q-carousel-slide name="vinculacion" class="">
                    <!-- :vinculacionCEMedio="planificacion.planificacionAcademico[0].planificaciones_vinculacion" -->
                    <VinculacionCEMedio
                        :idPlanificacion ="planificacion.planificacionAcademico[0].id"
                        :vinculacionCEMedio="!planificacion.planificacionAcademicaEdicion ? 
                            planificacion.planificacionAcademico[0].planificaciones_vinculacion :
                            planificacion.planificacionAcademicaEdicion[0].planificaciones_vinculacion"
                        :estadoPlanificacion="planificacion.planificacionAcademico[0].estado"
                        :opcion="planificacion.planificacionAcademicaEdicion ? true : false"
                    />
                </q-carousel-slide>
                <q-carousel-slide name="gestion" class="">
                    <!-- :gestiones="planificacion.planificacionAcademico[0].planificaciones_gestion"  -->
                    <GestionInstitucional
                        :idPlanificacion ="planificacion.planificacionAcademico[0].id"
                        :gestiones="!planificacion.planificacionAcademicaEdicion ? 
                            planificacion.planificacionAcademico[0].planificaciones_gestion :
                            planificacion.planificacionAcademicaEdicion[0].planificaciones_gestion"
                        :estadoPlanificacion="planificacion.planificacionAcademico[0].estado"
                        :opcion="planificacion.planificacionAcademicaEdicion ? true : false"
                    />
                </q-carousel-slide>
                <q-carousel-slide name="actividades" class="">
                    <!-- :actividadesFormativas="planificacion.planificacionAcademico[0].planificaciones_formacion"  -->
                    <ActividadesFormativas
                        :idPlanificacion ="planificacion.planificacionAcademico[0].id"
                        :actividadesFormativas="!planificacion.planificacionAcademicaEdicion ? 
                            planificacion.planificacionAcademico[0].planificaciones_formacion :
                            planificacion.planificacionAcademicaEdicion[0].planificaciones_formacion"
                        :estadoPlanificacion="planificacion.planificacionAcademico[0].estado"
                        :opcion="planificacion.planificacionAcademicaEdicion ? true : false"
                    />
                </q-carousel-slide>
                <template v-slot:control>
                    <q-carousel-control
                        position="bottom-right"
                        :offset="[15, 15]"
                        class="q-gutter-xs"                        
                    >
                        <q-btn
                            push round dense color="btnContinuar" text-color="white" icon="arrow_upward"
                            @click="$refs.carousel.previous()"
                        />
                        
                        <q-btn
                            v-if="usuario.perfil.planificacionAcademica === 'Académico'"
                            color="btnCancelar"
                            label="Volver al Panel"
                            class="q-ml-sm"
                            @click="planificacion.planificacionAcademicaEdicion &&
                                planificacion.planificacionAcademico[0].estado == 'Pendiente' ? cancelarPlanificacion() : volverPanel()"
                        />
                        <q-btn
                            v-if="usuario.perfil.planificacionAcademica === 'Académico' &&
                                    planificacion.planificacionAcademicaEdicion"
                            color="primary"
                            label="Guardar"
                            class="q-ml-sm"
                            @click="submitPlanificacion"
                        />
                        
                        <q-btn
                            v-if="usuario.perfil.planificacionAcademica === 'Académico' &&
                                    !planificacion.planificacionAcademicaEdicion &&
                                    planificacion.planificacionAcademico[0].estado == 'Pendiente'"
                            color="btnVolver"
                            label="Editar Plan"
                            class="q-ml-sm"
                            @click="submitPlanificacionEdicion"
                        />
                            <q-btn
                            v-if="usuario.perfil.planificacionAcademica === 'Jefe Departamento'"
                            color="btnCancelar"
                            label="Volver al Panel"
                            class="q-ml-sm"
                            @click="volverPanel"
                        />
                        <q-btn
                            v-if="usuario.perfil.planificacionAcademica === 'Jefe Departamento'"
                            color="btnVolver"
                            label="Ingresar observaciones"
                            class="q-ml-sm"
                            @click="rechazarPlanificacion"
                        />  
                        <q-btn
                            push round dense color="btnContinuar" text-color="white" icon="arrow_downward"
                            @click="$refs.carousel.next()"
                        />
                    </q-carousel-control>
                </template>
            </q-carousel>
        </q-card>        
        
    </div>
</template>
<script>    
    import { ref, toRef, computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";
    import PopupCancelarPlanificacion from "src/components/componentesPAA/PopupCancelarPlanificacion.vue";
    import PopUpRechazarPlanificacion from "src/components/componentesPAA/PopUpRechazarPlanificacion.vue";
    import InformacionBasica from "src/components/componentesPAA/InformacionBasica.vue";
    import Docencia from "src/components/componentesPAA//docencia/Docencia.vue";
    import Investigacion from "src/components/componentesPAA//investigacion/Investigacion.vue";
    import GestionInstitucional from "src/components/componentesPAA//gestion/GestionInstitucional.vue";
    import VinculacionCEMedio from "src/components/componentesPAA//vinculacion/VinculacionCEMedio.vue";
    import ActividadesFormativas from "src/components/componentesPAA//formativo/ActividadesFormativas.vue";


    export default defineComponent({
        components:{
            PopupCancelarPlanificacion,
            PopUpRechazarPlanificacion,
            InformacionBasica,
            Docencia,
            Investigacion,
            GestionInstitucional,
            VinculacionCEMedio,
            ActividadesFormativas,
            VinculacionCEMedio
        },
        props: {
            acciones: Array,            
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const cursos = computed(() => store.state.planificacion.asignatura);    
            const planificacion = computed(() => store.state.planificacion.planificacionAcademica);
            const usuario = computed(() => store.state.usuarix.usuario);
            const selected = ref([]);
            const tab = ref("informacionBasica")
            const mostrar = ref("");
            const mostrarPopUpRechazo = ref(false);
            const mostrarPopupCancelar = ref(false);
            const step = ref(1)
            const cambiaTab = (value, event) => {                
                tab.value = value;                
                //innerTab.value = "borrador";
            }

            const volverPanel = () => {
                store.dispatch("planificacion/planificacionAcademica/limpiaEditarPlanficicacion");

                if (usuario.value.perfil.planificacionAcademica == 'Académico'){
                    router.push("panelAcademico");
                }else if (usuario.value.perfil.planificacionAcademica == 'Jefe Departamento') {
                    router.push("panelJefeDepartamento");
                }else if (usuario.value.perfil.planificacionAcademica == 'Dirección/Desarrollo Académica'){
                    console.log("PANEL DIRECCION")
                    //router.push("panelAcademico");
                }
            }
            const submitPlanificacionEdicion = () => {
                store.dispatch("planificacion/planificacionAcademica/editarPlanificacion");
                router.push("planificacionAcademica")
            }
            const submitPlanificacion = () => {
                
                const nuevaPlanificacion = { ...planificacion.value.planificacionAcademicaEdicion[0] };                
                
                const nuevasDocencias = nuevaPlanificacion.planificaciones_docencia.map((docencia) => {                    
                    const nuevaDocencia = { ...docencia };
                    // Verificamos si el tipo es "Pregrado" o "Postgrado" antes de modificar la asignatura
                    nuevaDocencia.cantidad_horas = parseInt(docencia.cantidad_horas, 10);
                    if (docencia.tipo === "Pregrado" || docencia.tipo === "Postgrado" || docencia.tipo == "Programa") {                        
                        nuevaDocencia.asignatura = docencia.asignatura.id;
                    }
                    return nuevaDocencia;
                });

                nuevaPlanificacion.planificaciones_docencia = nuevasDocencias;                
                
                store.dispatch("planificacion/planificacionAcademica/patchPlanificacion", nuevaPlanificacion);
                volverPanel();
            }
            
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            };

            const manejoRechazo = () => {                
                mostrarPopUpRechazo.value = false;
                selected.value = [];
                volverPanel();
            };
            const handlerPopupCancelar = (respuesta) => {
                mostrarPopupCancelar.value = false;
                if (respuesta == "guarda") {
                    submitPlanificacion();
                } else if (respuesta == "sale") {
                    volverPanel();
                } else {
                // se hace nada
                }
            };
            
            return {
                mostrarPopUpRechazo,
                manejoRechazo,
                mostrar,
                mostrarPopupCancelar,
                handlerPopupCancelar,
                slide: ref('infoBasica'),
                cursos,
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                step,
                planificacion,
                submitPlanificacion,
                submitPlanificacionEdicion,
                volverPanel,
                usuario,
                rechazarPlanificacion: () => {
                    mostrarPopUpRechazo.value = true;
                    //router.push("rechazarPlanificacion");
                },
                cancelarPlanificacion: () => {
                    mostrarPopupCancelar.value = true;
                },
            };
        }        
    })
</script>