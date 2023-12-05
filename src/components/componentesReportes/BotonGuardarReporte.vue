<template>
    <PopupGuardarReporte
        :mostrar="mostrarPopupCancelar"
        @update:mostrar="mostrarPopupCancelar = $event"
        @respuestaPopup="handlerPopupCancelar"
    />
    <q-btn
        class="q-ml-sm"
        color="btnAdjuntar"
        label="   Guardar Reporte   "
        @click="cancelarReporte"
    />
    
</template>
<script>
    import { ref,toRef,watch, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";
    import PopupGuardarReporte from "src/components/componentesReportes/PopupGuardarReporte.vue";

    export default defineComponent({
    components: { 
        PopupGuardarReporte 
    },
    props: {
        opcion: String,
    },
    emits:["guardarAvance","guardarFinalizado"],
    setup(props, { emit }) {
        const store = useStore();
        const router = useRouter();
        const mostrar = ref("");
        const mostrarPopupCancelar = ref(false);
        const reporte = computed(() => store.state.reporte);
        const handlerPopupCancelar = (respuesta) => {
                mostrarPopupCancelar.value = false;
                if (respuesta == "guardaBorrador") {
                    emit("guardarAvance");
                } else if (respuesta == "guardaFinalizado") {                    
                    emit("guardarFinalizado");
                } else {
                // se hace nada
                }
        };

        return {
            reporte,
            handlerPopupCancelar,
            cancelarReporte: () => {
                mostrarPopupCancelar.value = true;
                //store.dispatch("accion/limpiaAccionAReportar");
                //store.dispatch("reporte/limpiaReporteFunciones");
                //store.dispatch("reporte/limpiaReporteHitos");
                //router.push("panelReportesUpci");
            },
            mostrar,
            mostrarPopupCancelar,
        };
    },
})
</script>