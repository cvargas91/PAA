<template>
  <div v-if="entregas">    
    <div class="text-h6 q-mb-md" v-if="mantencionPOA2023">
      En Mantención según POA 2023.
    </div>    
    <div v-if="entregaSeleccionada.length" class="tarjetaAmarilla">
      <div class="text-subtitle1">
        {{ entregaSeleccionada[0].descripcion }}
        <div v-if="adjuntos" class="text-h6 q-mb-md text-textoAzul">
          Acción <b> Sin archivos adjuntos</b>.
        </div>
      </div>
      <div
        v-if="entregaSeleccionada.length"
        class="row justify-end q-gutter-sm q-ma-md"
      >
        <q-btn
          color="btnCancelar"
          label="   Cancelar   "
          @click="entregaSeleccionada = []"
        />
        <BotonSecundarioEntregas
          :usuario="usuario"
          :entrega="entregaSeleccionada[0]"
          :tipoEntrega="tipoEntrega"
          @mantencion="manejoMantencion"
        />
        <BotonEdicionEntregas
          :usuario="usuario"
          :entrega="entregaSeleccionada[0]"
          :tipoEntrega="tipoEntrega"
          @mantencion="manejoMantencion"
        />
        <BotonPrincipalEntregas
          :usuario="usuario"
          :entrega="entregaSeleccionada[0]"
          :tipoEntrega="tipoEntrega"
          @ajuntosEntregas="getAdjuntos"
          @mantencion="manejoMantencion"
        />
      </div>
    </div>    
    <q-table
      flat
      class="tablaAcciones"
      :rows="entregas"
      :columns="
        tipoEntrega == 'verificador' ? columnasVerificador : columnasProducto
      "
      row-key="id"
      selection="single"
      v-model:selected="entregaSeleccionada"
      :filter="filter"
      :filter-method="customFilter"
      no-data-label="No hay verificadores para el filtro aplicado"
    >
      <!-- apartado Adjuntos -->
      <template v-slot:body-cell-adjuntos="props">        
        <q-td :props="props">
          <div v-if="props.value">
            <ul class="q-pa-sm">
              <li
                          v-for="item in props.value.slice(0, 5)"
                          :key="item.id"
                        >
                          <a target="_blank" :href="item.url">{{
                            item.name
                          }}</a>
                        </li>
              <div v-if="props.value.length > 5">...</div>
            </ul>
          </div>
        </q-td>
      </template>
      <!-- Apartado Titulo de la Accion -->
      <template v-slot:body-cell-accion="props">        
        <q-td :props="props">
          <div v-if="props.value">
            {{ props.value.id_uaysen }}
            <q-tooltip class="text-body1">{{ props.value.titulo }}</q-tooltip>
          </div>
        </q-td>
      </template>

      <template v-slot:top>
        <div class="row q-lg" style="width: 100%;">           
          <div class="col-8">
            <div class="q-gutter-md row">
              <q-select
                label="Periodo"            
                :options="optionsAnio"
                outlined 
                v-model="filter.anio"     
                @filter="AniofilterFn"
                style="width: 16%"
              />
              <q-select
                label="Accion"            
                :options="optionsAccion"
                outlined 
                v-model="filter.accion"     
                @filter="AccionfilterFn"
                style="width: 15%"
              />
              <q-select
                label="Unidad"            
                :options="optionsUnidad"
                outlined 
                v-model="filter.unidad"     
                @filter="UnidadfilterFn"              
                style="width: 15%"
              />
              <q-select
                label="Rol"            
                :options="optionsRol"
                outlined 
                v-model="filter.rol"     
                @filter="RolfilterFn"              
                style="width: 13%"
              />
            </div>
          </div>
          <div class="col-4" style="display: flex; justify-content: flex-end;">
            <div class="q-gutter-md row">              
              <q-input
                rounded
                autogrow
                outlined v-model="filter.search"
                placeholder="Buscar"
              >
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
          </div>
        </div>
      </template>      
    </q-table>
  </div>
</template>
<script>
import { ref, toRef, defineComponent } from "vue";
import BotonPrincipalEntregas from "src/components/BotonPrincipalEntregas.vue";
import BotonSecundarioEntregas from "src/components/BotonSecundarioEntregas.vue";
import BotonEdicionEntregas from "src/components/BotonEdicionEntregas.vue";

export default defineComponent({
  components: {
    BotonPrincipalEntregas,
    BotonSecundarioEntregas,
    BotonEdicionEntregas,
  },
  props: {
    entregas: Array,
    usuario: Object,
    tipoEntrega: String,
  },
  watch: {
    filterAnio(newFilterAnio) {      
      //this.customFilter;
    },
  },
  methods: {
    lowerCase(cadena){
      return cadena.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    },
    filteredAccion(rows, accion){    
      return rows.filter((row) => {        
        if (row.indicador.funcion.accion.id_uaysen == accion){
          return row
        }
      });
    },
    filteredRol(rows, rol){
      return rows.filter((row) => {        
        if (row.rol.tipo == rol){
          return row
        }
      });
    },
    filteredUnidad(rows, unidad){      
      return rows.filter((row) => {        
        if (row.rol.actor.id_uaysen == unidad){
          return row
        }
      });
    },
    filterPeriodo (rows, anio){
      return rows.filter((row) => {        
        if (row.indicador.funcion.accion.anio == anio){
          return row
        }
      });
    },
    filterBusquedaObjetos(objeto, busqueda){
      let rowValues = Object.values(objeto);
      let rowValuesLower = rowValues.map(elemento => {
          if(elemento){            
          //Control para arreglo de archivos adjuntos
            if(!Array.isArray(elemento)) {
              // Código a ejecutar si elemento NO es un arreglo
              return this.lowerCase(elemento.toString());
            }else{
              return "";  
            }
          }else{
            return "";
          }
      });

      for (let val=0; val < rowValuesLower.length; val++){          
          if (rowValuesLower[val].includes(busqueda)){            
            return true;
          }
      }
      return false;
    },
    filterBusquedaAdjuntos(objeto, busqueda){      
      for (let val=0 ; val < objeto.length; val++){
        if(this.filterBusquedaObjetos(objeto[val], busqueda)){
          return true;
        }
      }
      return false;                  
    },
    filterBusqueda (rows, busqueda){
      return rows.filter((row) => {
        let rowValues = Object.values(row);
        let foundMatch = false; // Variable de control para indicar si se encontró una coincidencia
        
      //let rowValuesLower = rowValues.map(elemento => {
        let rowValuesLower = rowValues.map(elemento => {
          if(elemento){            
            //Control para arreglo de archivos adjuntos
            if(Array.isArray(elemento)){              
              if(this.filterBusquedaAdjuntos(elemento, busqueda)){
                foundMatch = true
              }else{
                return "";
              }
              
            }

            if(typeof elemento === "object"){
              if(this.filterBusquedaObjetos(elemento, busqueda)){
                foundMatch = true
              }else{
                return "";
              }
            }else{
              return this.lowerCase(elemento.toString());
            }            
          }else{
            return "";
          }
        });
        
        if(foundMatch){
          return row;
        }

        for (let val=0; val < rowValuesLower.length; val++){                    
          if (rowValuesLower[val].includes(busqueda)){            
            return row;
          }else{
          }
        }
      });
    },
    customFilter(rows, terms){    
      this.entregaSeleccionada = [];
      let busqueda = this.filter.search ? this.lowerCase(this.filter.search) : ""
      let filterAnio = this.filter.anio;
      let filterAccion = this.filter.accion;
      let filterRol = this.filter.rol;
      let filterUnidad = this.filter.unidad;
      
      let filteredRows = rows;

      if (filterAnio){      
        if (filterAnio !== "Todos"){
          filteredRows = this.filterPeriodo(filteredRows, filterAnio);
        }else{
          filteredRows = filteredRows;
        }        
      }
      
      if (filterAccion) {
        if (filterAccion !== "Todos"){
          filteredRows = this.filteredAccion(filteredRows, filterAccion);
        }else{
          filteredRows = filteredRows;
        }        
      }

      if (filterRol) {
        if(filterRol !== "Todos"){
          filteredRows = this.filteredRol(filteredRows, filterRol);
        }else{
          filteredRows = filteredRows;
        }        
      }

      if (filterUnidad) {
        if(filterUnidad !== "Todos"){
          filteredRows = this.filteredUnidad(filteredRows, filterUnidad);
        }else{
          filteredRows = filteredRows;
        }        
      }

      if (busqueda != ""){
        filteredRows = this.filterBusqueda(filteredRows, busqueda);        
      }
      
      return filteredRows               
    },
    manejoMantencion(mantencion){
      this.mantencionPOA2023 = mantencion
    },
  },
  setup(props) {
    const adjuntos = ref(false);
    const mantencionPOA2023 = ref(false);
    const getAdjuntos = (adjunto) => {
      adjuntos.value = adjunto;
    };
    const optionsAnio = ref([]);
    const optionsAccion = ref([]);
    const optionsRol    = ref([]);
    const optionsUnidad = ref([]);
    
    const filterAnio   = ref(null);
    const filterAccion = ref(null);
    const filterRol    = ref(null);
    const filterUnidad = ref(null);
    
    return {
      optionsAccion,
      optionsRol,   
      optionsUnidad,
      optionsAnio,
      filterAnio,
      filterAccion,
      filterRol,
      filterUnidad,
      // filter: ref(""),
      filter: ref({
        anio: null,
        search: "",
        accion: null,
        rol: null,
        unidad: null,
      }),
      mantencionPOA2023,
      getAdjuntos,
      adjuntos,
      entregas: toRef(props, "entregas"),
      tipoEntrega: toRef(props, "tipoEntrega"),
      entregaSeleccionada: ref([]),
      columnasProducto: [
        {
          name: "descripcion",
          label: "Descripción",
          field: "descripcion",
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "colaborador",
          label: "Colaborador",
          field: (row) => row.usuario.first_name + " " + row.usuario.last_name,
          align: "left",
        },
        {
          name: "mdv",
          label: "Medio de Verificación",
          field: (row) => row.mdv ? row.mdv.nombre : row.hitos[0].nombre,
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "accion",
          label: "Acción",
          field: (row) => row.mdv ? row.mdv.accion : row.hitos[0].accion,
          align: "left",
        },
        {
          name: "accionTipo",
          label: "Tipo acción",
          field: (row) => row.mdv ? row.mdv.accion.tipo : row.hitos[0].accion.origen,
          align: "left",
          sortable: true,
        },
        {
          name: "adjuntos",
          label: "Adjuntos",
          field: "adjuntos",
          align: "left",
        },
        {
          name: "estado",
          label: "Estado",
          field: "estado",
          align: "left",
          sortable: true,
        },
        {
          name: "fecha",
          label: "Fecha",
          field: "fecha_creacion",
          align: "left",
          sortable: true,
        },
      ],
      columnasVerificador: [
        {
          name: "descripcion",
          label: "Descripción",
          field: "descripcion",
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "colaborador",
          label: "Colaborador",
          field: (row) => row.usuario.first_name + " " + row.usuario.last_name,
          align: "left",
        },
        {
          name: "indicador",
          label: "Indicador",
          field: (row) => row.indicador.nombre,
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "funcion",
          label: "Función",
          field: (row) => row.indicador.funcion.nombre,
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "accion",
          label: "Acción",
          field: (row) => row.indicador.funcion.accion,
          align: "left",
          style: "white-space: normal",
        },
        {
          name: "adjuntos",
          label: "Adjuntos",
          field: "adjuntos",
          align: "left",
        },
        {
          name: "estado",
          label: "Estado",
          field: "estado",
          align: "left",
          sortable: true,
        },
        {
          name: "fecha",
          label: "Fecha",
          field: "fecha_creacion",
          align: "left",
          sortable: true,
        },
      ],
      AniofilterFn (val, update, abort) {
          if (Array.isArray(optionsAnio.value) && optionsAnio.value.length > 0) {
              // already loaded
              update()
              return
          }
              
          update(() => {                        
            optionsAnio.value = props.tipoEntrega === "verificador" ? Array.from(new Set(props.entregas.map(entrega => entrega.indicador.funcion.accion.anio))) :
            Array.from(new Set(props.entregas.map(entrega => entrega.hitos[0].accion.anio)));
            optionsAnio.value.unshift("Todos");
          })                
      },
      AccionfilterFn (val, update, abort) {
          if (Array.isArray(optionsAccion.value) && optionsAccion.value.length > 0) {
              // already loaded
              update()
              return
          }
              
          update(() => {               
            optionsAccion.value = props.tipoEntrega === "verificador" ? Array.from(new Set(props.entregas.map(entrega => entrega.indicador.funcion.accion.id_uaysen))) : 
              Array.from(new Set(props.entregas.map(entrega => entrega.hitos[0].accion.id_uaysen)));
            optionsAccion.value.unshift("Todos");
          })                
      },
      UnidadfilterFn (val, update, abort) {
          if (Array.isArray(optionsUnidad.value) && optionsUnidad.value.length > 0) {
              // already loaded
              update()
              return
          }
              
          update(() => {            
            optionsUnidad.value = Array.from(new Set(props.entregas.map(entrega => entrega.rol.actor.id_uaysen)));
            optionsUnidad.value.unshift("Todos");
          })                
      },
      RolfilterFn (val, update, abort) {
          if (Array.isArray(optionsRol.value) && optionsRol.value.length > 0) {
              // already loaded
              update()
              return
          }
              
          update(() => {            
            optionsRol.value = Array.from(new Set(props.entregas.map(entrega => entrega.rol.tipo)));
            optionsRol.value.unshift("Todos");
          })                
      },
    };
  },
});
</script>
