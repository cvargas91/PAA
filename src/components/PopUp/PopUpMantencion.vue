<template>
    <q-dialog v-model="mostrar">
        <q-card class="col-xxl-5" style="width: 250%">        
            <q-card-section class="text-textoAzul" >
                    <!-- <q-card-section align="right" class="text-weight-medium">
                        <b>Descripción</b>
                    </q-card-section> -->
                <q-separator color="indigo-10" />

                <!-- <div>Acción Seleccionada:</div> -->
                <div class="text-h6 text-textoAzul">
                    <b>{{mensaje}}</b>
                </div>    
                <q-separator color="indigo-10" />            
            </q-card-section>
            
            <q-card-actions align="center">
                <q-btn label="ACEPTAR" color="secondary" text-color="white" v-close-popup class="Full-width"/>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
    import { computed } from "vue";
    import { useStore } from "vuex";
  
    export default {
        props: {
            mostrar: Boolean,
        },
        setup(props, { emit }) {
            const store = useStore();
            const mostrar = computed({
                get: () => props.mostrar,
                set: (value) => emit("update:mostrar", value),
            });
            const mensaje = "Plazo cerrado para carga de Medios de Verificación. En proceso de construcción de Reporte."
            return {
                mostrar,
                mensaje,
            };
    },
};
</script>