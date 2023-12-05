<template>
    <q-dialog 
      v-model="mostrar" 
      persistent 
      transition-show="slide-up"
      transition-hide="slide-down"
      @before-show="limpiarFormulario"      
    > 
    
        <q-card style="width: 1000px; max-width: 80vw;">
            <q-card-section>
                <div class="text-h6 text-textoAzul">Ingresa una nueva asignatura a la Planificación Académica</div>                
            </q-card-section>
            
            <q-separator />
            <q-card-section>              
              <q-form @submit="handleClick('guardar')" class="text-textoAzul">
                  <!-- <q-item>
                    Tipos de asignaturas disponibles:
                  </q-item> -->
                  <q-item>                    
                    <q-option-group
                        inline
                        :options="opcionesCursos"
                        :model-value="tab"
                        @update:model-value="cambiaTab"
                    />
                  </q-item>

                  <q-item v-if="tab">                    
                    <q-item-section>                      
                      <q-item-label><b>Asignaturas {{ etiquetaAsignaturas }}</b>:</q-item-label>
                    </q-item-section>
                    <q-item-section>                      
                      <q-select
                        v-model="form.asignatura"
                        :options="opcionesAsignaturaUsuario"
                        style="width: 100%;"
                        option-value="id"
                        option-label="nombre"
                      >
                        <template v-slot:option="scope">
                          <q-item v-bind="scope.itemProps">
                            <q-item-section>
                              <q-item-label>{{ scope.opt.nombre }}</q-item-label>
                              <q-item-label caption>{{ scope.opt.codigo }}</q-item-label>
                            </q-item-section>
                          </q-item>
                        </template>
                      </q-select>
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
                      <q-item-label><b>Semestre:</b></q-item-label>
                    </q-item-section>
                    <q-item-section>        
                      <q-select
                        v-model="form.semestre"
                        :options="opcionesSemestre"
                        style="width: 100%;"
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
                        style="width: 100%;"
                        mask="######"
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
                      />
                    </div>
                  </q-card-section>   
              </q-form>                
            </q-card-section>      
        </q-card>
    </q-dialog>
</template>

<script>
  import { ref, computed, toRef ,onMounted} from "vue";
  import { useStore } from "vuex";

  export default {
    methods: {
      limpiarFormulario() {        
        this.form.asignatura = "";
        this.form.rol = "";
        this.form.semestre = "";
        this.form.horas = "";
      },
    },
    computed: {
      etiquetaAsignaturas (){         
        if (this.tab == "asignaturas_dpto_usuario"){
          return Object.keys(this.asignaturas.cursosPorDepartamento[this.tab])[0]
        }else{
          if(this.tab == "pregrado"){
            return Object.keys(this.asignaturas.cursosPorDepartamento['asignaturas_direccion'])[1]
          }else{
            return Object.keys(this.asignaturas.cursosPorDepartamento['asignaturas_direccion'])[0]
          }                    
        }        
      },
      opcionesAsignaturaUsuario(){          
          if (this.tab == "asignaturas_dpto_usuario"){
            return this.asignaturas.cursosPorDepartamento.asignaturas_dpto_usuario[Object.keys(this.asignaturas.cursosPorDepartamento.asignaturas_dpto_usuario)[0]];
          }else{
            if(this.tab == "pregrado"){              
              return this.asignaturas.cursosPorDepartamento['asignaturas_direccion'][Object.keys(this.asignaturas.cursosPorDepartamento['asignaturas_direccion'])[1]]
            }else{
              return this.asignaturas.cursosPorDepartamento['asignaturas_direccion'][Object.keys(this.asignaturas.cursosPorDepartamento['asignaturas_direccion'])[0]]
          }                    
        }      
          //return this.asignaturas.cursosPorDepartamento.asignaturas_dpto_usuario[Object.keys(this.asignaturas.cursosPorDepartamento.asignaturas_dpto_usuario)[0]];
          
      },
      opcionesCursos(){
        const etiquetas = [];
        for (const clavePrincipal in this.asignaturas.cursosPorDepartamento) {
          if (clavePrincipal !== 'asignaturas_otro_dpto') {
            const clavesSecundarias = Object.keys(this.asignaturas.cursosPorDepartamento[clavePrincipal]);

            for (const claveSecundaria of clavesSecundarias) {
              let valorDescriptivo = '';
              if (clavePrincipal === 'asignaturas_dpto_usuario') {
                valorDescriptivo = 'asignaturas_dpto_usuario';
              } else if (clavePrincipal === 'asignaturas_direccion') {
                if (claveSecundaria === 'Dirección de Postgrado y Educación Continua') {
                  valorDescriptivo = claveSecundaria;
                } else if (claveSecundaria === 'Dirección de Pregrado') {
                  valorDescriptivo = 'pregrado';
                }
              }
              etiquetas.push({ label: claveSecundaria, value: valorDescriptivo });
            }
          }
        }

        if (etiquetas.length > 0){
          this.etiqueta = etiquetas[0].value;
        }
        return etiquetas;
      },  
    },
    props: {
        cursos: Array,
        mostrar: Boolean,        
    },
    setup(props, { emit }) {
        const store = useStore();
        const modelRol = ref("");
        const modelAsignatura = ref("");
        const modelSemestre = ref("");
        const ModelHoras = ref("");
        const miPlanificacion = computed(() => store.state.planificacion.planificacionAcademica);
        const asignaturas = computed (() => store.state.planificacion.asignatura);
        const etiqueta = ref(null);
        const tab = ref(etiqueta);
        const cambiaTab = (value, event) => {          
          tab.value = value;
        }
        const form = ref({
          asignatura : "",
          rol : "",
          semestre: "",
          horas: ""
        });
        onMounted(() => {
            form.value.asignatura = "";
            form.value.semestre = "";
            form.value.rol = "";            
            form.value.horas = "";
        });
        
        const handleClick = (opcion) => {
            let nuevaAsignatura = {
              ...form.value.asignatura,
              horas: form.value.horas,
              semestre: form.value.semestre.label,
              rol: form.value.rol.label,
            };
            let respuesta = {
              opcion : opcion,
              data: nuevaAsignatura,
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
            modelRol,
            modelAsignatura,
            modelSemestre,
            ModelHoras,
            asignaturas,
            asignatura: null,
            semestre: null,
            rol: null,
            horasEstimadas: null,
            opcionesAsignatura: toRef(props, "cursos"),            
            opcionesSemestre: [              
              { label: "Primer semestre", value: 1 },
              { label: "Segundo semestre", value: 2 },
            ],
            opcionesRol: [              
              { label: "Responsable del curso", value: "Responsable del curso" },
              { label: "Co-responsable", value: "Co-responsable" },
              { label: "Parte del equipo", value: "Parte del equipo" },
              { label: "Coordinador/a equipo docente", value: "Coordinador/a equipo docente" },              
            ],
            etiqueta,
            tab,
            cambiaTab,
        };
    },
  };
</script>