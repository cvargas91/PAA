import { api } from "boot/axios";
import { Cookies } from "quasar";

export function getCursos(context) {
    const django_token = Cookies.get("django_token");
    api
        .get("obtener_cursos/", {
            headers: {
            "X-CSRFTOKEN": django_token,
            },
        })
        .then((response) => {
            console.log("Response cursos ucampus", response.status)
            //context.commit("setNuevoProducto", response.data);
        })
        .catch(() => {
            console.log("error obteniendo cursos");
        });
}

export function getMisCursos(context) {
    const django_token = Cookies.get("django_token");
    api
        .get("mis_cursos/", {
            headers: {
            "X-CSRFTOKEN": django_token,
            },
        })
        .then((response) => {
            context.commit("setMisCursos", response.data);
        })
        .catch(() => {
            console.log("error obteniendo mis cursos");
        });
}

export function getCursosAcademicx(context, data) {
    api
        .get("api/asignaturasPlanificacionAcademica/cursos_academicxs/" + data.nombre + '/' + data.apellido + '/' + data.anio + '/')
        .then((response) => {
            context.commit("setCursosAcademicx", response.data);
        })
        .catch(() => {
            console.log("error obteniendo cursos del académic@");
        });
}

export function limpiaCursosAcademicx(context) {
    context.commit("limpiaCursosAcademicx");
}

export function getCursosPorDepartamento(context) {
    const django_token = Cookies.get("django_token");
    api
        .get("api/asignaturasPlanificacionAcademica/asignaturasDepartamento/", {
            headers: {
            "X-CSRFTOKEN": django_token,
            },
        })
        .then((response) => {
            context.commit("setCursosDepartamento", response.data.data);
        })
        .catch(() => {
            console.log("error obteniendo mis cursos");
        });
}