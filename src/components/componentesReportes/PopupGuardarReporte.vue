<template>
  <q-dialog v-model="mostrar">
    <q-card>
      <q-card-section>
        <div class="text-h6 text-textoAzul">Guardar Reporte</div>
        <q-separator spaced />
      </q-card-section>
      <q-list class="text-textoAzul">        

        <q-item clickable @click="handleClick('guardaFinalizado')" v-ripple>
          <q-item-section avatar>
            <q-icon color="positive" name="sticky_note_2" />
          </q-item-section>

          <q-item-section>
            <q-item-label>
              <b> Guardar como Finalizado </b>
            </q-item-label>
            <q-item-label caption>
              Sale y almacena el avance del Reporte como "Finalizado". Reporte listo para descargar
              en <b>Finalizados</b>
            </q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable @click="handleClick('guardaBorrador')" v-ripple>
          <q-item-section avatar>
            <q-icon color="negative" name="sticky_note_2" />
          </q-item-section>

          <q-item-section>
            <q-item-label>
              <b> Guardar Borrador </b>
            </q-item-label>
            <q-item-label caption>
              Sale y almacena el avance del Reporte como "borrador". Se
              puede editar en apartado <b>Borradores</b>
            </q-item-label>
          </q-item-section>
        </q-item>        

        <q-item clickable @click="handleClick('cancelar')" v-ripple>
          <q-item-section avatar>
            <q-icon color="primary" name="edit" />
          </q-item-section>

          <q-item-section>
            <q-item-label>
              <b> No </b>
            </q-item-label>
            <q-item-label caption>
              No guardar. Quiero seguir editando.
              </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-card>
  </q-dialog>
</template>

<script>
import { computed } from "vue";

export default {
  props: {
    mostrar: Boolean,
  },
  setup(props, { emit }) {
    const handleClick = (respuesta) => {
      emit("respuestaPopup", respuesta);
    };
    const mostrar = computed({
      get: () => props.mostrar,
      set: (value) => emit("update:mostrar", value),
    });
    return {
      handleClick,
      mostrar,
    };
  },
};
</script>
