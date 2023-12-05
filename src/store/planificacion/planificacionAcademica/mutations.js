export function setModoEdicion(state) {
  state.edicion = true;
}

export function setAcademicxsDepartamento (state, academicxs){
  state.academicxs = academicxs;
}

export function setPlanificacionAEditar(state) {
  //state.planificacionAcademicaEdicion = state.planificacionAcademico;
  state.planificacionAcademicaEdicion = [...state.planificacionAcademico];

}
export function limpiaPlanificacionAEditar(state) {
  state.planificacionAcademicaEdicion = null;
}

export function setResumenHoras(state, resumenHoras) {
  state.resumenHoras = resumenHoras;
}

export function setPlanificacionesDepartamento(state, planificaciones) {
  state.planificacionesDepartamento = planificaciones;
}

export function setPlanificacionAcademicx(state, planificacion) {
  state.planificacionAcademico = planificacion;
}

export function misPlanificaciones(state, planificacion) {  
  state.planificacionAcademico = planificacion;
}

export function ultimoIDPlanificacion(planificacion){
  const ultimoID = planificacion.reduce((maxID, item) => {
    return item.id > maxID ? item.id : maxID;
  }, 0);
  return ultimoID;
}

// ======================== Información Básica ============================
export function actualizarInformacionBasica (state, nuevaInformacionBasica) {
  state.planificacionAcademicaEdicion[0].rut_academicx = nuevaInformacionBasica.rut_academicx;
  state.planificacionAcademicaEdicion[0].categoria     = nuevaInformacionBasica.categoria;
  state.planificacionAcademicaEdicion[0].departamento  = nuevaInformacionBasica.departamento;
  state.planificacionAcademicaEdicion[0].fecha_ingreso = nuevaInformacionBasica.fecha_ingreso;
  state.planificacionAcademicaEdicion[0].jornada       = nuevaInformacionBasica.jornada;
}

// ======================== Información Básica ============================
// ======================== Docencia ======================================
//Manejo datos asignaturas "Planificación Docencia"
export function actualizarAsignatura(state, nuevaAsignatura) {  
  let index = -1;
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_docencia) {
    index = state.planificacionAcademicaEdicion[0].planificaciones_docencia.findIndex(
      //(item) => item.asignatura && item.asignatura.id === nuevaAsignatura.id
      (item) => item.id === nuevaAsignatura.idPlanificacion
    );
  }
  

  if (index !== -1 && state.planificacionAcademicaEdicion[0].planificaciones_docencia[index]) {
    state.planificacionAcademicaEdicion[0].planificaciones_docencia[index].cantidad_horas = nuevaAsignatura.horas;
    state.planificacionAcademicaEdicion[0].planificaciones_docencia[index].rol = nuevaAsignatura.rol;
  } else {
    const ultimoID = ultimoIDPlanificacion(state.planificacionAcademicaEdicion[0].planificaciones_docencia);    
    nuevaAsignatura.id = ultimoID + 1;
    state.planificacionAcademicaEdicion[0].planificaciones_docencia.push(nuevaAsignatura);
  }
}

export function quitarAsignatura (state, asignaturaId) {
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_docencia) {
    const index = state.planificacionAcademicaEdicion[0].planificaciones_docencia.findIndex(
      // (item) => item.asignatura && item.asignatura.id === asignaturaId
      (item) => item.id === asignaturaId
    );

    if (index !== -1) {
      state.planificacionAcademicaEdicion[0].planificaciones_docencia.splice(index, 1);      
    }
  }
}

//Manejo datos programas "Planificación Docencia"
export function actualizarArregloProgramas(state, nuevaPrograma) {
  let index = -1;
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_docencia) {
    index = state.planificacionAcademicaEdicion[0].planificaciones_docencia.findIndex(
      // (item) => item.asignatura && item.asignatura.id === nuevaPrograma.asignatura.id
      (item) => item.id === nuevaPrograma.id
    );
  }
  

  if (index !== -1 && state.planificacionAcademicaEdicion[0].planificaciones_docencia[index]) {  
    state.planificacionAcademicaEdicion[0].planificaciones_docencia[index] = nuevaPrograma;    
  } else {    
    const ultimoID = ultimoIDPlanificacion(state.planificacionAcademicaEdicion[0].planificaciones_docencia);
    nuevaPrograma.id = ultimoID + 1;
    state.planificacionAcademicaEdicion[0].planificaciones_docencia.push(nuevaPrograma);
  }
}

export function eliminarPrograma (state, programaId) {
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_docencia) {
    const index = state.planificacionAcademicaEdicion[0].planificaciones_docencia.findIndex(
      (item) => item.id === programaId
    );

    if (index !== -1) {
      state.planificacionAcademicaEdicion[0].planificaciones_docencia.splice(index, 1);      
    }
  }
}
//Manejo datos actividades "Planificación Docencia"
export function actualizarArregloActividadesDocencia(state, nuevaActividad) {
  let index = -1;
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_docencia) {
    index = state.planificacionAcademicaEdicion[0].planificaciones_docencia.findIndex(
      (item) => item.id === nuevaActividad.id
    );
  }
  

  if (index !== -1 && state.planificacionAcademicaEdicion[0].planificaciones_docencia[index]) {
    state.planificacionAcademicaEdicion[0].planificaciones_docencia[index] = nuevaActividad;
  } else {
    const ultimoID = ultimoIDPlanificacion(state.planificacionAcademicaEdicion[0].planificaciones_docencia);
    nuevaActividad.id = ultimoID + 1;
    state.planificacionAcademicaEdicion[0].planificaciones_docencia.push(nuevaActividad);
  }
}

export function quitarActividadDocencia (state, actividadId) {
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_docencia) {
    const index = state.planificacionAcademicaEdicion[0].planificaciones_docencia.findIndex(
      (item) => item.id === actividadId
    );

    if (index !== -1) {
      state.planificacionAcademicaEdicion[0].planificaciones_docencia.splice(index, 1);      
    }
  }
}
// ======================== Docencia ======================================

// ======================== Investigación==================================
//Manejo datos publicaciones "Planificación Investigacion"
export function actualizarPlanificacionInvestigacion(state, nuevaInvestigacion) {
  let index = -1;
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_investigacion) {
    index = state.planificacionAcademicaEdicion[0].planificaciones_investigacion.findIndex(
      (item) => item.id === nuevaInvestigacion.id
    );
  }
  

  if (index !== -1 && state.planificacionAcademicaEdicion[0].planificaciones_investigacion[index]) {
    state.planificacionAcademicaEdicion[0].planificaciones_investigacion[index] = nuevaInvestigacion;
  } else {
    const ultimoID = ultimoIDPlanificacion(state.planificacionAcademicaEdicion[0].planificaciones_investigacion);
    nuevaInvestigacion.id = ultimoID + 1;
    state.planificacionAcademicaEdicion[0].planificaciones_investigacion.push(nuevaInvestigacion);
  }
}

export function quitarInvestigacion (state, investigacionId) {
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_investigacion) {
    const index = state.planificacionAcademicaEdicion[0].planificaciones_investigacion.findIndex(
      (item) => item.id === investigacionId
    );

    if (index !== -1) {
      state.planificacionAcademicaEdicion[0].planificaciones_investigacion.splice(index, 1);      
    }
  }
}
// ======================== Investigación==================================

// ======================== Gestion =======================================
//Manejo datos de actividades de Gestión Institucional
export function actualizarActividadGestion(state, nuevaGestion) {
  let index = -1;
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_gestion) {
    index = state.planificacionAcademicaEdicion[0].planificaciones_gestion.findIndex(
      (item) => item.id === nuevaGestion.id
    );
  }
  

  if (index !== -1 && state.planificacionAcademicaEdicion[0].planificaciones_gestion[index]) {
    state.planificacionAcademicaEdicion[0].planificaciones_gestion[index] = nuevaGestion;
  } else {
    const ultimoID = ultimoIDPlanificacion(state.planificacionAcademicaEdicion[0].planificaciones_gestion);
    nuevaGestion.id = ultimoID + 1;
    state.planificacionAcademicaEdicion[0].planificaciones_gestion.push(nuevaGestion);
  }
}

export function quitarActividadGestion (state, gestionId) {
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_gestion) {
    const index = state.planificacionAcademicaEdicion[0].planificaciones_gestion.findIndex(
      (item) => item.id === gestionId
    );

    if (index !== -1) {
      state.planificacionAcademicaEdicion[0].planificaciones_gestion.splice(index, 1);      
    }
  }
}
// ======================== Gestion =======================================

// ======================== Vinculación ===================================
export function actualizarActividadVinculacion(state, nuevaActividad) {
  let index = -1;
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_vinculacion) {
    index = state.planificacionAcademicaEdicion[0].planificaciones_vinculacion.findIndex(
      (item) => item.id === nuevaActividad.id
    );
  }
  

  if (index !== -1 && state.planificacionAcademicaEdicion[0].planificaciones_vinculacion[index]) {
    state.planificacionAcademicaEdicion[0].planificaciones_vinculacion[index] = nuevaActividad;
  } else {
    const ultimoID = ultimoIDPlanificacion(state.planificacionAcademicaEdicion[0].planificaciones_vinculacion);
    nuevaActividad.id = ultimoID + 1;
    state.planificacionAcademicaEdicion[0].planificaciones_vinculacion.push(nuevaActividad);
  }
}

export function quitarActividadVinculacion (state, vinculacionId) {
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_vinculacion) {
    const index = state.planificacionAcademicaEdicion[0].planificaciones_vinculacion.findIndex(
      (item) => item.id === vinculacionId
    );

    if (index !== -1) {
      state.planificacionAcademicaEdicion[0].planificaciones_vinculacion.splice(index, 1);      
    }
  }
}
// ======================== Vinculación ===================================

// ======================== Formativas ====================================
export function actualizarActividadesFormativas(state, nuevaActividad) {
  let index = -1;
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_formacion) {
    index = state.planificacionAcademicaEdicion[0].planificaciones_formacion.findIndex(
      (item) => item.id === nuevaActividad.id
    );
  }
  

  if (index !== -1 && state.planificacionAcademicaEdicion[0].planificaciones_formacion[index]) {
    state.planificacionAcademicaEdicion[0].planificaciones_formacion[index] = nuevaActividad;
  } else {
    const ultimoID = ultimoIDPlanificacion(state.planificacionAcademicaEdicion[0].planificaciones_formacion);
    nuevaActividad.id = ultimoID + 1;
    state.planificacionAcademicaEdicion[0].planificaciones_formacion.push(nuevaActividad);
  }
}

export function quitarActividadFormativa (state, actividadId) {
  
  if (state.planificacionAcademicaEdicion[0].planificaciones_formacion) {
    const index = state.planificacionAcademicaEdicion[0].planificaciones_formacion.findIndex(
      (item) => item.id === actividadId
    );

    if (index !== -1) {
      state.planificacionAcademicaEdicion[0].planificaciones_formacion.splice(index, 1);      
    }
  }
}
// ======================== Formativas ====================================

