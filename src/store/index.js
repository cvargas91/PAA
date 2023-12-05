import { store } from "quasar/wrappers";
import { createStore } from "vuex";
import accion from "./accion";
import usuarix from "./usuarix";
import entrega from "./entrega";
import verificador from "./verificador";
import producto from "./producto";
import poador from "./poador";
import estrategia from "./estrategia";
import actor from "./actor";
import reporte from "./reporte";
import asignatura from "./planificacion/asignatura";
import observaciones from "./planificacion/observaciones";
import planificacionAcademica from "./planificacion/planificacionAcademica";

export default store(function (/* { ssrContext } */) {
  const Store = createStore({
    modules: {
      accion,
      usuarix,
      entrega,
      verificador,
      producto,
      poador,
      estrategia,
      actor,
      reporte,
      //Manejo "store" Planificación Anual Académica
      planificacion: {
        namespaced: true,
        modules: {
          asignatura,
          observaciones,
          planificacionAcademica,
        }
      },      
    },

    // enable strict mode (adds overhead!)
    // for dev mode and --debug builds only
    strict: process.env.DEBUGGING,
  });

  return Store;
});
