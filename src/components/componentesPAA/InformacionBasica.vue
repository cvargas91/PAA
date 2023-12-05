<template>
    <q-card  style="max-width: 1900px; margin: 0 auto;" class="text-textoAzul">
        <q-card-section class="q-pa-xs" v-if="opcion!= 'jefe'">
          <h2 class="text-h5">Formulario de Datos Académicos</h2>
        </q-card-section>        
        <q-card-section>
          <q-form @input="informChanges">
            <q-item style="max-height: 40px;">
              <q-item-section>
                <q-item-label><b>Nombre:</b></q-item-label>
              </q-item-section>
              <q-item-section class="tarjetaAmarilla">        
                <q-input
                  v-model="infoBasica.nombreCompleto"
                  id="nombreCompleto"                  
                  style="width: 100%;"
                  borderless
                  readonly
                />
              </q-item-section>
            </q-item>
            <!-- <q-separator/> -->
            <q-item style="max-height: 40px;">
              <q-item-section>
                <q-item-label><b>RUT:</b></q-item-label>
              </q-item-section>
              <q-item-section class="tarjetaAmarilla">        
                <q-input
                  v-model="infoBasica.rut"
                  id="rut"                  
                  required
                  style="width: 100%;"
                  borderless
                  :readonly="opcion == 'vista' || opcion =='jefe'? true : false"
                /> 
              </q-item-section>
            </q-item>

            <q-item style="max-height: 80px;">
              <q-item-section top class="col-6 gt-sm">
                <q-item-label class="q-mt-sm"><b>Categoría Académica:</b></q-item-label>
              </q-item-section>
            
              <q-item-section top class="tarjetaAmarilla q-gutter-xs">
                <q-item-label lines="1" class="q-gutter-sm">
                  <div class="row justify-evenly">
                    <div class="col-4">
                      <q-radio 
                        dense 
                        v-model="selectedCategoria" 
                        val="ordinaria" 
                        label="Categoría Académica Ordinaria" 
                        :disable="opcion == 'vista' || opcion =='jefe'? true : false"
                        @update:model-value="subcategoriasOptions"
                      />
                    </div>
                    <div class="col-4">
                      <q-radio 
                        dense 
                        v-model="selectedCategoria" 
                        val="adjunta" 
                        label="Categoría Académica Adjunta" 
                        :disable="opcion == 'vista' || opcion =='jefe'? true : false"
                        @update:model-value="subcategoriasOptions"
                      />
                    </div>
                  </div>
                  
                  
                </q-item-label>
            
                <q-item-section class="col-6 col-md-4 q-mt-sm"> <!-- Se ajustó el margen inferior -->
                  <q-select 
                  v-model="infoBasica.categoriaAcademica"
                  label="Seleccione una subcategoría"
                  id="categoriaAcademica"                  
                  required
                  :options="opcionesSubcategoria"
                  @update:model-value="informChanges"
                  style="width: 100%;"
                  dense
                  borderless
                  :readonly="opcion == 'vista' || opcion =='jefe'? true : false"
                  :disable="selectedCategoria"
                  />
                </q-item-section>
              </q-item-section>

            </q-item>

            <q-item style="max-height: 40px;">
              <q-item-section>
                <q-item-label><b>Departamento:</b></q-item-label>
              </q-item-section>
              <q-item-section class="tarjetaAmarilla">        
                <q-input
                  v-model="infoBasica.departamento"
                  id="departamento"                  
                  required
                  style="width: 100%;"
                  dense
                  borderless
                />
              </q-item-section>
            </q-item>

            <q-item style="max-height: 40px;">
              <q-item-section>
                <q-item-label><b>Fecha de Ingreso a la Universidad:</b></q-item-label>
              </q-item-section>
              <q-item-section class="tarjetaAmarilla">        
                <q-input  
                  v-model="infoBasica.fechaIngreso" 
                  mask="date" 
                  :rules="['date']"
                  @update:model-value="informChanges"
                  dense 
                  hide-bottom-space
                >                
                  <template v-slot:prepend >
                    <q-icon name="event" class="cursor-pointer" >
                      <q-popup-proxy 
                        cover transition-show="scale" 
                        transition-hide="scale" 
                        v-if="!(opcion == 'vista' || opcion =='jefe'? true : false)"
                        >
                        <q-date 
                          v-model="infoBasica.fechaIngreso" 
                          @update:model-value="informChanges"
                        >
                          <div class="row items-center justify-end">
                            <q-btn 
                              v-close-popup 
                              label="Ok!" 
                              color="possitive" 
                              flat
                              @click="informChanges"
                              />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </q-item-section>
            </q-item>
            <q-item style="max-height: 44px;">
              <q-item-section>
                <q-item-label><b>Jornada (en horas):</b></q-item-label>
              </q-item-section>
              <q-item-section class="tarjetaAmarilla">        
                <q-select
                  v-model="infoBasica.jornada"
                  id="jornada"
                  @update:model-value="informChanges"
                  :options="jornadaOptions"
                  style="width: 100%;"
                  dense
                  borderless
                  :readonly="opcion == 'vista' || opcion =='jefe'? true : false"
                >
                </q-select>
              </q-item-section>
            </q-item>

          </q-form>

        </q-card-section>        
      </q-card>
</template>
<script>    
    import { ref, toRef,computed, onMounted, defineComponent } from "vue";
    import { useRouter } from "vue-router";
    import { useStore } from "vuex";    
    

    export default defineComponent({
        methods: {
          informChanges() {
            if(this.opcion == "jefe" || this.opcion == 'vista'){
              console.log("Aca no hacer nada")
            }else{
              let nuevaInformacion = {
                "rut_academicx" : this.infoBasica.rut,
                "categoria": this.infoBasica.categoriaAcademica,
                "departamento": this.infoBasica.departamento,
                "fecha_ingreso": this.infoBasica.fechaIngreso ? this.infoBasica.fechaIngreso.replace(/\//g, '-') : null,
                "jornada": this.infoBasica.jornada,
              }
              this.$store.dispatch("planificacion/planificacionAcademica/actualizarInformacionBasicaPlanificacion", nuevaInformacion);
            }            
          }
        },
        props: {
            planificacionAcademico: Array,
            estadoPlanificacion: String,
            opcion: String,
            usuario: Object,
        },
        setup(props) {
            const router = useRouter();
            const store = useStore();
            const detalleAccion = computed(() => store.state.accion);
            const selected = ref([]);
            const tab = ref("informacionBasica");
            const infoBasica = ref({
              nombreCompleto    : props.usuario.nombre + " " + props.usuario.apellido,
              rut               : props.planificacionAcademico.rut_academicx,
              categoriaAcademica: props.planificacionAcademico.categoria,
              departamento      : props.usuario.perfil? props.usuario.perfil.actor_nombre : props.planificacionAcademico.departamento,
              fechaIngreso      : props.planificacionAcademico.fecha_ingreso,
              jornada           : props.planificacionAcademico.jornada,
            });
            
            const opcionesSubcategoria = ref([]);
            const categoriaAcademicaOptions =             
            ['Categoría y Carrera Académica Ordinaria',
            'Categoría Académica Adjunta'];
            function generateOptions() {
              return Array.from({ length: 44 }, (_, index) => String(index + 1));
            }
            const jornadaOptions = ref(generateOptions());
            
            const subcategorias = {
                  ordinaria: ['Instructor', 'Profesor Asistente', 'Profesor Asociado', 'Profesor Titular'],
                  adjunta: ['Instructor Adjunto', 'Profesor Adjunto', 'Investigador Adjunto']
            };

            const subcategoriasOptions = (value) => {
              opcionesSubcategoria.value = subcategorias[value];
            };

            
            const cambiaTab = (value, event) => {                
                tab.value = value;
                //innerTab.value = "borrador";
            }   
            const seleccionaFila = async (detalles) => {
                window.scroll({ top: 0, left: 0, behavior: "smooth" });
            }
            
            const opciones = [
                {
                    name: "asignatura",
                    label: "Asignatura",
                    field: (row) => (row.nombre ? row.nombre : "Otro"),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "codigo",
                    label: "Codigo",
                    field: (row) => (row.codigo ? row.codigo : "Cpd"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "semestre",
                    label: "Semestre",
                    field: (row) => (row.semestre ? row.semestre : "Sem"),
                    align: "left",
                    style: "white-space: normal",
                },
                {
                    name: "estado",
                    label: "Estado Asignatura",
                    field: (row) => (row.estado ? row.estado : "Sin"),
                    align: "left",
                    style: "white-space: normal",
                },   
            ]
            return {
                infoBasica,
                categoriaAcademicaOptions,
                jornadaOptions,
                opciones,
                detalleAccion,
                selected,
                seleccionaFila: seleccionaFila,
                cambiaTab,
                tab,
                opcionesSubcategoria,
                subcategoriasOptions,
                planificacionAcademica: toRef(props,"planificacionAcademico"),
                opcion: toRef(props,"opcion"),
                disable: ref(false),
                categoria: ref('ordinaria'),
                selectedCategoria: ref(''),
                selectedSubcategoria: '',
                selectedIndex: -1,
            };
          }        
    })
</script>