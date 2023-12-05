import { api } from "boot/axios";
import { Cookies } from "quasar";

export function resumenActividades(context, periodo) {
    api
        .get("api/planificacionesAcademicas/resumenActividades/" + periodo + "/")
        .then((response) => {
            context.commit("setResumenHoras", response.data);            
        })
        .catch(() => {
            console.log("error req acciones unidad resp");
        });
}

export function resumenActividadesAcademico(context, idPlanificacion) {
    api
        .get("api/planificacionesAcademicas/resumenActividadesAcademico/" + idPlanificacion + "/")
        .then((response) => {
            context.commit("setResumenHoras", response.data);            
        })
        .catch(() => {
            console.log("error req. resumenActividadesAcademico");
        });
}

export async function editarPlanificacion(context){
    context.commit("setPlanificacionAEditar")
    //context.commit("setModoEdicion")
}

export async function limpiaEditarPlanficicacion(context){
    context.commit("limpiaPlanificacionAEditar")
    //context.commit("setModoEdicion")
}

export function planificacionAcademicx(context, idPlanificacion) {
    api
        .get("api/planificacionesAcademicas/planificacionAcademicx/" + idPlanificacion + "/")
        .then((response) => {
            context.commit("setPlanificacionAcademicx", response.data.planificacion);
        })
        .catch(() => {
            console.log("error req acciones unidad resp");
        });
}

export function planificacionesDepartamento(context, periodo) {
    api
        .get("api/planificacionesAcademicas/planificacionesDepartamento/" + periodo + '/Enviado_jefe_dpto')
        .then((response) => {
            context.commit("setPlanificacionesDepartamento", response.data.datos);            
        })
        .catch(() => {
            console.log("error req planificaciones unidad resp");
        });
}

export function getAcademicos(context) {
    const django_token = Cookies.get("django_token");
    api
        .get("usuarios_departamento/", {
            headers: {
            "X-CSRFTOKEN": django_token,
            },
        })
        .then((response) => {
            console.log("Response getAcademicos ", response.data)
            context.commit("setAcademicxsDepartamento", response.data);
        })
        .catch(() => {
            console.log("error obteniendo academicos del departamento");
        });
}


export function getMisPlanificaciones(context) {
    api
        .get("api/planificacionesAcademicas/misPlanificaciones/" + 2023 + "/")
        .then((response) => {            
            context.commit("misPlanificaciones", response.data.planificacion);            
        })
        .catch(() => {
            console.log("error req misPlanificaciones");
        });
}

export function getMisObservaciones(context) {
    api
        .get("api/observacionesPlanificacionAcademica/observacionesASubsanar/" + 2023 + "/")
        .then((response) => {            
            context.commit("misObservaciones", response.data.observaciones);            
        })
        .catch(() => {
            console.log("error req getMisObservaciones");
        });
}

export function vincularCompromisos(context, compromiso) {
    const django_token = Cookies.get("django_token");
    api
    .post("/planificacionVinculacionCompromisos/", compromiso, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
        })
    .then((response) => {
        console.log("Response vincularCompromisos", response)
        //context.commit("setWorkflow", "RechazadoPorLider");
    })
    .catch(() => {
        console.log("error planificacion/vincularCompromisos");
    });
}


// ======================== Información Básica ============================
export function actualizarInformacionBasicaPlanificacion (context, nuevaInformacionBasica) {
    context.commit("actualizarInformacionBasica",nuevaInformacionBasica );
}
// ======================== Información Básica ============================

// ======================== Docencia ======================================
//Manejo datos asignaturas "Planificación Docencia"
export function actualizarArregloAsignaturas(context, nuevaAsignatura) {
    context.commit("actualizarAsignatura",nuevaAsignatura );
}

export function eliminarAsignatura(context, asignaturaId) {
    context.commit("quitarAsignatura",asignaturaId );
}

//Manejo datos programas "Planificación Docencia"
export function actualizarArregloProgramas(context, nuevoPrograma) {
    context.commit("actualizarArregloProgramas",nuevoPrograma );
}

export function eliminarPrograma(context, programaId) {
    context.commit("eliminarPrograma",programaId );
}

//Manejo datos actividades "Planificación Docencia"
export function actualizarArregloActividadesDocencia(context, nuevaActividad) {
    context.commit("actualizarArregloActividadesDocencia",nuevaActividad );
}

export function eliminarActividadDocencia(context, actividadId) {
    context.commit("quitarActividadDocencia",actividadId );
}
// ======================== Docencia ======================================


// ======================== Investigación ======================================
//Manejo datos publicaciones "Planificación Investigacion"
export function actualizarArregloInvestigaciones(context, nuevaInvestigacion) {
    context.commit("actualizarPlanificacionInvestigacion", nuevaInvestigacion );
}

export function eliminarInvestigacion(context, publicacionId) {
    context.commit("quitarInvestigacion", publicacionId );
}
//Manejo datos proyectos "Planificación Investigacion"
export function actualizarArregloProyectos(context, nuevoProyecto) {
    context.commit("actualizarAsignatura", nuevoProyecto );
}

export function eliminarProyecto(context, proyectoId) {
    context.commit("quitarAsignatura",proyectoId );
}
//Manejo datos eventos "Planificación Investigacion"
export function actualizarArregloEventos(context, nuevoEvento) {
    context.commit("actualizarAsignatura", nuevoEvento );
}

export function eliminarEvento(context, eventoId) {
    context.commit("quitarAsignatura",eventoId );
}
// ======================== Investigación ======================================

// ======================== Gestion =======================================
//Manejo datos gestión "Planificación Gestión Institucional"
export function actualizarArregloGestion(context, nuevaGestion) {
    context.commit("actualizarActividadGestion", nuevaGestion );
}

export function eliminarGestion(context, gestionId) {
    context.commit("quitarActividadGestion",gestionId );
}
// ======================== Gestion =======================================

// ======================== Vinculación ===================================
//Manejo datos gestión "Planificación Gestión Institucional"
export function actualizarArregloVinculacion(context, nuevaActividad) {
    context.commit("actualizarActividadVinculacion", nuevaActividad);
}

export function eliminarActividadVinculacion(context, vinculacionId) {
    context.commit("quitarActividadVinculacion",vinculacionId );
}
// ======================== Vinculación ===================================

// ======================== Formativas ====================================
//Manejo datos formacion "Planificación Actividades Formativas"
export function actualizarArregloFormacion(context, nuevaActividad) {
    context.commit("actualizarActividadesFormativas", nuevaActividad );
}

export function eliminarActividadFormativa(context, actividadId) {
    context.commit("quitarActividadFormativa",actividadId );
}
// ======================== Formativas ====================================

export function patchPlanificacion(context, nuevaPlanificacion) {
    const django_token = Cookies.get("django_token");
    api
    .patch("/api/planificacionesAcademicas/" + nuevaPlanificacion.id + "/", nuevaPlanificacion, {
        headers: {
            "X-CSRFTOKEN": django_token,
        },
    })
    .then((response) => {
        console.log("respuesta patch", response.status);
        //context.commit("setNuevoProducto", response.data);
    })
    .catch(() => {
        console.log("error planificacion/patchPlanificacion");
    });
}