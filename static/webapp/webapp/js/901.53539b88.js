"use strict";(self["webpackChunkspci"]=self["webpackChunkspci"]||[]).push([[901],{86901:(e,a,o)=>{o.r(a),o.d(a,{default:()=>E});var t=o(83673);const r={class:"q-pa-md"},l=(0,t._)("b",null,"Generar Reporte",-1),s=(0,t._)("b",null,"Borrador Reportes",-1),i=(0,t._)("b",null,"Reportes Finalizados",-1),c=(0,t._)("div",{class:"text-h4 q-mb-md"},[(0,t._)("b",null,"Generar Reporte")],-1),n=(0,t._)("div",{class:"text-h4 q-mb-md"},[(0,t._)("b",null,"Borrador Reportes")],-1),d=(0,t._)("div",{class:"text-h4 q-mb-md"},[(0,t._)("b",null,"Reportes Finalizados")],-1);function p(e,a,o,p,u,m){const b=(0,t.up)("q-avatar"),f=(0,t.up)("q-tab"),h=(0,t.up)("q-tabs"),v=(0,t.up)("BandejaUnidades"),q=(0,t.up)("q-tab-panel"),w=(0,t.up)("BandejaReportes"),_=(0,t.up)("q-tab-panels"),R=(0,t.up)("q-splitter"),g=(0,t.up)("q-card");return(0,t.wg)(),(0,t.iD)("div",r,[(0,t.Wm)(g,{class:"my-card"},{default:(0,t.w5)((()=>[(0,t.Wm)(R,{modelValue:p.splitterModel,"onUpdate:modelValue":a[2]||(a[2]=e=>p.splitterModel=e),style:{height:"650px"}},{before:(0,t.w5)((()=>[(0,t.Wm)(h,{modelValue:p.tab,"onUpdate:modelValue":a[0]||(a[0]=e=>p.tab=e),vertical:"",class:"text-teal"},{default:(0,t.w5)((()=>[(0,t.Wm)(f,{name:"reporte"},{default:(0,t.w5)((()=>[(0,t.Wm)(b,{icon:"description",size:"md",color:"light-blue-10","text-color":"white"}),l])),_:1}),(0,t.Wm)(f,{name:"borradores"},{default:(0,t.w5)((()=>[(0,t.Wm)(b,{icon:"edit_note",size:"md",color:"light-blue-10","text-color":"white"}),s])),_:1}),(0,t.Wm)(f,{name:"finalizados"},{default:(0,t.w5)((()=>[(0,t.Wm)(b,{icon:"task",size:"md",color:"light-blue-10","text-color":"white"}),i])),_:1})])),_:1},8,["modelValue"])])),after:(0,t.w5)((()=>[(0,t.Wm)(_,{class:"text-textoAzul",modelValue:p.tab,"onUpdate:modelValue":a[1]||(a[1]=e=>p.tab=e),animated:"",swipeable:"",vertical:"","transition-prev":"jump-up","transition-next":"jump-up"},{default:(0,t.w5)((()=>[(0,t.Wm)(q,{name:"reporte"},{default:(0,t.w5)((()=>[c,(0,t.Wm)(v)])),_:1}),(0,t.Wm)(q,{name:"borradores"},{default:(0,t.w5)((()=>[n,(0,t.Wm)(w,{reportes:p.reportes.borrador.borradores},null,8,["reportes"])])),_:1}),(0,t.Wm)(q,{name:"finalizados"},{default:(0,t.w5)((()=>[d,(0,t.Wm)(w,{reportes:p.reportes.finalizado.finalizados},null,8,["reportes"])])),_:1})])),_:1},8,["modelValue"])])),_:1},8,["modelValue"])])),_:1})])}var u=o(61959),m=o(93617),b=o(26920);const f={class:"q-px-sm"},h={key:0,class:"q-pa-md"},v={class:"row justify-end q-gutter-sm q-ma-md"};function q(e,a,o,r,l,s){const i=(0,t.up)("q-table"),c=(0,t.up)("q-btn");return(0,t.wg)(),(0,t.iD)("div",f,[(0,t.Wm)(i,{rows:e.reportes,columns:e.opciones,selection:"single","row-key":"id",selected:e.accionesSeleccionadas,"onUpdate:selected":a[0]||(a[0]=a=>e.accionesSeleccionadas=a),"no-data-label":"No hay acciones para el filtro aplicado"},null,8,["rows","columns","selected"]),e.accionesSeleccionadas.length?((0,t.wg)(),(0,t.iD)("div",h,[(0,t._)("div",v,[(0,t.Wm)(c,{class:"q-ma-sm",color:"btnCancelar",label:"   Cancelar   ",onClick:a[1]||(a[1]=a=>e.accionesSeleccionadas=[])}),e.seRenderea?(0,t.kq)("",!0):((0,t.wg)(),(0,t.j4)(c,{key:0,class:"q-ma-sm",color:"positive",label:"   Editar    ",onClick:e.accionBotonEdicion},null,8,["onClick"])),e.seRenderea?((0,t.wg)(),(0,t.j4)(c,{key:1,class:"q-ma-sm",label:"   Descargar    ",color:"light-blue-10",onClick:e.accionBotonGeneracion},null,8,["onClick"])):(0,t.kq)("",!0)])])):(0,t.kq)("",!0)])}var w=o(79582);const _=(0,t.aZ)({props:{reportes:Array},setup(e){const a=(0,m.oR)(),o=(0,w.tv)(),r=(0,u.iH)([]),l=(0,t.Fl)((()=>a.state.actor.actores)),s=(0,u.iH)(!1),i=(0,u.iH)(e.reportes);e.reportes.length&&"Finalizado"===e.reportes[0].estado&&(s.value=!0);const c=e=>{let a=l.value.filter((a=>a.id===e)).map((e=>e.id_uaysen));return a};return{getValor:c,actores:l,accionesSeleccionadas:r,reportes:i,seRenderea:s,opciones:[{name:"reporte",label:"N° Reporte",field:"id",align:"left"},{name:"unidad",label:"Unidad",field:e=>c(e.actor),align:"left",sortable:!0},{name:"creado",label:"Creado",field:"creado",align:"left",sortable:!0},{name:"creado",label:"Modificado",field:"modificado",align:"left",sortable:!0}],accionBotonEdicion:async()=>{await a.dispatch("accion/reqDetalleAccion",r.value[0].reporte_acciones[0].accion),a.dispatch("accion/reqFuncionesPorAccion",r.value[0].reporte_acciones[0].accion),a.dispatch("accion/reqMdvFuncionesEHitosPorAccion",r.value[0].reporte_acciones[0].accion),a.dispatch("producto/reqHitosReporte",r.value[0].reporte_acciones[0].accion),a.dispatch("reporte/setReporteAEditar",r.value[0]),o.push("reporteUpciEdicion")},accionBotonGeneracion:async()=>{let e=c(r.value[0].actor);e.push(r.value[0].modificado.substring(0,10)),e.push(r.value[0].id),await a.dispatch("reporte/generaReporte",e),r.value=[],a.dispatch("reporte/reqReportesBorradores"),a.dispatch("reporte/reqReportesUpci"),o.push("panelReportesUpci")}}}});var R=o(74260),g=o(82138),W=o(48240),k=o(7518),B=o.n(k);const x=(0,R.Z)(_,[["render",q]]),y=x;B()(_,"components",{QTable:g.Z,QBtn:W.Z});const Z={components:{BandejaUnidades:b["default"],BandejaReportes:y},setup(){const e=(0,m.oR)(),a=(0,t.Fl)((()=>e.state.reporte)),o=(0,t.Fl)((()=>e.state.reporte.reporte));(0,t.Fl)((()=>e.state.reporte.reporte.borradores));return(0,t.bv)((()=>{e.dispatch("reporte/reqReportesBorradores"),e.dispatch("reporte/reqReportesUpci"),e.dispatch("reporte/limpiaReporteAEditar"),e.dispatch("accion/limpiaAccionAReportar"),e.dispatch("reporte/limpiaReporteAccion")})),{reportes:a,reportes2:o,tab:(0,u.iH)("reporte"),splitterModel:(0,u.iH)(20)}}};var z=o(10151),A=o(80218),C=o(57547),U=o(3269),V=o(75096),j=o(5906),F=o(86602);const Q=(0,R.Z)(Z,[["render",p]]),E=Q;B()(Z,"components",{QCard:z.Z,QSplitter:A.Z,QTabs:C.Z,QTab:U.Z,QAvatar:V.Z,QTabPanels:j.Z,QTabPanel:F.Z})}}]);