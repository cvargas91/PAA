export function setMisCursos(state, misCursos) {
  state.misCursos = misCursos;
}

export function setCursosAcademicx(state, cursos) {
  state.cursosAcademicx = cursos;
}

export function limpiaCursosAcademicx(state) {
  state.cursosAcademicx = null;
}

export function setCursosDepartamento(state, cursos) {
  state.cursosPorDepartamento = cursos;
}

export function setProductos(state, productos) {
  state.productos = productos;
}

export function setProductosUPCI(state, productos) {
  state.productosUPCI = productos;
}

export function setTotalHitosReporte(state, arrayTotalHitos) {
  state.totalHitos = arrayTotalHitos;
}