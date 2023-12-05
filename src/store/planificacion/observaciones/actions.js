import { api } from "boot/axios";
import { Cookies } from "quasar";

export function getMisObservaciones(context) {
    api
        .get("api/observacionesPlanificacionAcademica/observacionesASubsanar/" + 2023 + "/")
        .then((response) => {
            context.commit("setObservacionesASubsanar", response.data.datos);            
        })
        .catch(() => {
            console.log("error req getMisObservaciones");
        });
}//Consulta por las observaciones ingresadas por el usuario tipo Jefe Dpto o Dirección.
export function getObservacionesUsuario(context) {
    api
        .get("api/observacionesPlanificacionAcademica/misObservaciones/")
        .then((response) => {
            context.commit("setObservacionesASubsanar", response.data.datos);            
        })
        .catch(() => {
            console.log("error req getMisObservaciones");
        });
}

//################################### Flujo cambios de estado Planificación ################################
export function workflowJefeDptoRechaza(context, observacion) {
    const django_token = Cookies.get("django_token");
    api
    .post("/planificacionJefeDptoRechaza/", observacion, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
        })
    .then((response) => {
        console.log("Response workflowJefeDptoRechaza", response)
        //context.commit("setWorkflow", "RechazadoPorLider");
    })
    .catch(() => {
        console.log("error entrega/workflowJefeDptoRechaza");
    });
}

export function workflowDireccionRechaza(context, observacion) {
    const django_token = Cookies.get("django_token");
    api
    .post("/planificacionDireccionRechaza/", observacion, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
        })
    .then((response) => {
        console.log("Response workflowDireccionRechaza", response)
        //context.commit("setWorkflow", "RechazadoPorLider");
    })
    .catch(() => {
        console.log("error entrega/workflowDireccionRechaza");
    });
}

export function workflowEnvioAJefeDpto(context, observacion) {
    const django_token = Cookies.get("django_token");
    api
    .post("/planificacionEnvioAJefeDpto/", observacion, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
        })
    .then((response) => {
        console.log("Response workflowEnvioAJefeDpto", response)
        //context.commit("setWorkflow", "RechazadoPorLider");
    })
    .catch(() => {
        console.log("error entrega/workflowEnvioAJefeDpto");
    });
}

export function workflowEnvioADireccion(context, observacion) {
    const django_token = Cookies.get("django_token");
    api
    .post("/planificacionJefeDptoAcepta/", observacion, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
        })
    .then((response) => {
        console.log("Response workflowEnvioADireccion", response)
        //context.commit("setWorkflow", "RechazadoPorLider");
    })
    .catch(() => {
        console.log("error entrega/workflowEnvioADireccion");
    });
}

export function workflowDireccionAcepta(context, observacion) {
    const django_token = Cookies.get("django_token");
    api
    .post("/planificacionDireccionAcepta/", observacion, {
            headers: {
                "X-CSRFTOKEN": django_token,
            },
        })
    .then((response) => {
        console.log("Response workflowDireccionAcepta", response)
        //context.commit("setWorkflow", "RechazadoPorLider");
    })
    .catch(() => {
        console.log("error entrega/workflowDireccionAcepta");
    });
}


//################################### Flujo cambios de estado Planificación ################################