<template>
    <q-dialog v-model="mostrar">
        <q-card>
            <q-card-section>
                <div class="text-h6 text-textoAzul">¿Segur@ que quieres cancelar?</div>
                <q-separator spaced />
            </q-card-section>
            <q-list class="text-textoAzul">
                <q-item clickable @click="handleClick('cancelar')" v-ripple>
                    <q-item-section avatar>
                        <q-icon color="primary" name="edit" />
                    </q-item-section>

                    <q-item-section>
                        <q-item-label>
                            <b> No </b>
                        </q-item-label>
                        <q-item-label caption>
                            No quiero salir. Quiero seguir editando la planificación.
                        </q-item-label>
                    </q-item-section>
                </q-item>
                
                <q-item clickable @click="handleClick('guarda')" v-ripple>
                    <q-item-section avatar>
                        <q-icon color="negative" name="sticky_note_2" />
                    </q-item-section>
                    <q-item-section>
                        <q-item-label>
                            <b> Sí, ¡pero guarda mis avances! </b>
                        </q-item-label>
                        <q-item-label caption>
                            Vuelve al panel y almacena el avance de la planificación sin enviar al Jefe de Departamento. Se
                            puede editar nuevamente en pestaña <b>"Planificaciones".</b>
                        </q-item-label>
                    </q-item-section>
                </q-item>

                <q-item clickable @click="handleClick('sale')" v-ripple>
                    <q-item-section avatar>
                        <q-icon color="secondary" name="delete_forever" />
                    </q-item-section>

                    <q-item-section>
                        <q-item-label>
                            <b> Sí </b>
                        </q-item-label>
                        <q-item-label caption>
                            Volver al panel y descartar avances.
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
  