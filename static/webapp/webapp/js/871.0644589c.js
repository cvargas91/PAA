"use strict";(self["webpackChunkspci"]=self["webpackChunkspci"]||[]).push([[871],{15871:(e,a,l)=>{l.r(a),l.d(a,{default:()=>ue});var i=l(83673),o=l(62323);const r={class:"q-pa-md"},t={key:0},n=(0,i._)("div",{class:"text-h6"},"¡Felicitaciones!",-1),s=(0,i._)("p",null,"Se ha enviado el nuevo borrador al líder del equipo",-1),c={key:1},d=(0,i._)("div",{class:"text-h6 text-textoAzul"},"¡Felicitaciones!",-1),u=(0,i._)("p",null,"Se ha guardado el nuevo verificador como borrador",-1),p=(0,i._)("div",{class:"text-h6 text-textoAzul"}," ¿Está listo tu nuevo verificador para ser revisado por el líder del equipo? ",-1),m={key:2},v={class:"text-h6"},f={class:"text-subtitle1"},g={class:"text-subtitle2"},w={class:"col"},b={class:"text-body1"},_={key:0,class:"column"},q={key:1,class:"bg-accent"},k={class:"row"},h={class:"col q-ma-sm"},W={class:"text-h6"},y=(0,i._)("div",{class:"text-weight-bold"},"Fórmula",-1),C=(0,i._)("div",{class:"text-weight-bold"},"Meta",-1),j=(0,i._)("div",{class:"text-weight-bold"},"Verificador",-1),V={class:"col q-ma-sm"},x=(0,i._)("div",{class:"text-h6"},"Indique el avance del indicador",-1),D=(0,i._)("div",{class:"text-h6"},"Adjuntar el verificador",-1),A=(0,i._)("p",null," Adjunta documentos que necesites para demostrar el avance del indicador. Éstos quedarán almacenados en Google Drive y serán revisados por tu jefatura y el equipo de UPCI ",-1),S={key:0,class:"q-pa-md",style:{"max-width":"400px"}},Z=(0,i._)("div",{class:"text-weight-bold"}," Documentos subidos a Google Drive: ",-1),E={class:"row justify-end"},P={key:3},Q=(0,i._)("p",null," Esto es muy extraño. Si lees esto, probablemente es un error del sistema ",-1),z=[Q];function U(e,a,l,Q,U,N){const F=(0,i.up)("PopupCancelarNuevaEntrega"),I=(0,i.up)("q-btn"),H=(0,i.up)("q-card-section"),L=(0,i.up)("q-btn-toggle"),G=(0,i.up)("q-card-actions"),K=(0,i.up)("q-card"),R=(0,i.up)("q-step"),Y=(0,i.up)("q-separator"),$=(0,i.up)("q-input"),B=(0,i.up)("q-form"),O=(0,i.up)("Picker"),M=(0,i.up)("q-item-label"),T=(0,i.up)("q-item-section"),J=(0,i.up)("q-icon"),X=(0,i.up)("q-item"),ee=(0,i.up)("q-list"),ae=(0,i.up)("q-stepper-navigation"),le=(0,i.up)("q-stepper"),ie=(0,i.Q2)("ripple");return(0,i.wg)(),(0,i.iD)("div",r,[(0,i.Wm)(F,{mostrar:Q.mostrarPopupCancelar,"onUpdate:mostrar":a[0]||(a[0]=e=>Q.mostrarPopupCancelar=e),onRespuestaPopup:Q.handlerPopupCancelar},null,8,["mostrar","onRespuestaPopup"]),"EnviadoAlLider"==Q.entrega.estadoWorkflow?((0,i.wg)(),(0,i.iD)("div",t,[n,s,(0,i.Wm)(I,{label:"OK. Ir a la bandeja de entregas",class:"q-ma-sm",to:"bandejaEntregas",color:"primary"})])):Q.verificador.nuevoVerificador?((0,i.wg)(),(0,i.iD)("div",c,[d,u,p,(0,i._)("div",null,[(0,i.Wm)(I,{label:"No no no, déjalo como borrador. Lo enviaré más tarde",class:"q-ma-sm",to:"bandejaEntregas",color:"primary"}),(0,i.Wm)(I,{class:"q-ma-sm",label:"Sí, envíalo al líder",onClick:Q.enviaAlLider,color:"secondary"},null,8,["onClick"])])])):Q.entrega.nuevaEntrega?((0,i.wg)(),(0,i.iD)("div",m,[(0,i.Wm)(le,{modelValue:Q.step,"onUpdate:modelValue":a[7]||(a[7]=e=>Q.step=e),ref:"stepper",color:"blue",animated:"","header-class":"tablaAcciones"},{navigation:(0,i.w5)((()=>[(0,i.Wm)(ae,{class:"tarjetaAmarilla"},{default:(0,i.w5)((()=>[(0,i._)("div",E,[(0,i.Wm)(I,{color:"btnCancelar",label:"  Cancelar  ",class:"q-ml-sm",onClick:Q.clicCancelar},null,8,["onClick"]),Q.step>1?((0,i.wg)(),(0,i.j4)(I,{key:0,color:"btnVolver",onClick:a[4]||(a[4]=a=>e.$refs.stepper.previous()),label:"   Volver   ",class:"q-ml-sm"})):(0,i.kq)("",!0),1==Q.step?((0,i.wg)(),(0,i.j4)(I,{key:1,onClick:a[5]||(a[5]=a=>e.$refs.stepper.next()),color:"btnContinuar",label:"  Continuar ",class:"q-ml-sm",disable:!Q.indicadorSeleccionado},null,8,["disable"])):(0,i.kq)("",!0),2==Q.step?((0,i.wg)(),(0,i.j4)(I,{key:2,onClick:a[6]||(a[6]=a=>e.$refs.stepper.next()),color:"btnContinuar",label:"  Continuar ",class:"q-ml-sm",disable:!Q.verificadorValor||!Q.verificadorDescripcion},null,8,["disable"])):(0,i.kq)("",!0),3==Q.step?((0,i.wg)(),(0,i.j4)(I,{key:3,onClick:Q.submitVerificador,color:"primary",label:"  Finalizar ",class:"q-ml-sm",disable:!Q.entrega.adjuntosNuevaEntrega},null,8,["onClick","disable"])):(0,i.kq)("",!0)])])),_:1})])),default:(0,i.w5)((()=>[(0,i.Wm)(R,{name:1,title:"Indicador",icon:"settings",done:Q.step>1,class:"tarjetaAmarilla"},{default:(0,i.w5)((()=>[(0,i._)("div",v," Seleccione un verificador de las siguientes funciones de "+(0,o.zw)(Q.entrega.nuevaEntrega.id_uaysen),1),(0,i._)("div",f,(0,o.zw)(Q.entrega.nuevaEntrega.titulo),1),(0,i._)("div",g," Objetivo: "+(0,o.zw)(Q.entrega.nuevaEntrega.objetivo),1),((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(Q.accion.funciones,(e=>((0,i.wg)(),(0,i.iD)("div",{class:"row",key:e.id},[(0,i._)("div",w,[(0,i.Wm)(K,{class:"tarjetaAmarilla"},{default:(0,i.w5)((()=>[(0,i.Wm)(H,{class:"q-pa-sm"},{default:(0,i.w5)((()=>[(0,i._)("div",b,(0,o.zw)(e.nombre),1)])),_:2},1024),(0,i.Wm)(G,{vertical:""},{default:(0,i.w5)((()=>[e.indicador_set.length?((0,i.wg)(),(0,i.iD)("div",_,[((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(e.indicador_set,(e=>((0,i.wg)(),(0,i.j4)(L,{"no-caps":"",align:"left",class:"col",key:e.id,modelValue:Q.indicadorSeleccionado,"onUpdate:modelValue":a[1]||(a[1]=e=>Q.indicadorSeleccionado=e),"toggle-color":"primary",options:[{label:e.nombre,value:e}]},null,8,["modelValue","options"])))),128))])):((0,i.wg)(),(0,i.iD)("div",q," No hay indicadores definidos para esta función. Por favor, notificar este incidente a UPCI para ser revisado. Gracias "))])),_:2},1024)])),_:2},1024)])])))),128))])),_:1},8,["done"]),(0,i.Wm)(R,{name:2,title:"Detalles",icon:"assignment",done:Q.step>2,class:"tarjetaAmarilla"},{default:(0,i.w5)((()=>[(0,i._)("div",k,[(0,i._)("div",h,[(0,i.Wm)(K,{flat:"",class:"tarjetaAmarilla"},{default:(0,i.w5)((()=>[(0,i.Wm)(H,null,{default:(0,i.w5)((()=>[(0,i._)("div",W,(0,o.zw)(Q.indicadorSeleccionado.nombre),1)])),_:1}),(0,i.Wm)(Y,{inset:""}),(0,i.Wm)(H,{class:"q-pt-none"},{default:(0,i.w5)((()=>[y,(0,i.Uk)(" "+(0,o.zw)(Q.indicadorSeleccionado.formula),1)])),_:1}),(0,i.Wm)(H,{class:"q-pt-none"},{default:(0,i.w5)((()=>[C,(0,i.Uk)(" "+(0,o.zw)(Q.indicadorSeleccionado.meta),1)])),_:1}),(0,i.Wm)(H,{class:"q-pt-none"},{default:(0,i.w5)((()=>[j,(0,i.Uk)(" "+(0,o.zw)(Q.indicadorSeleccionado.nombreVerificador),1)])),_:1})])),_:1})]),(0,i._)("div",V,[(0,i.Wm)(K,{flat:"",class:"tarjetaAmarilla"},{default:(0,i.w5)((()=>[(0,i.Wm)(H,null,{default:(0,i.w5)((()=>[x])),_:1}),(0,i.Wm)(Y,{inset:""}),(0,i.Wm)(B,{class:"q-gutter-md"},{default:(0,i.w5)((()=>[(0,i.Wm)(H,{class:"q-pt-none"},{default:(0,i.w5)((()=>[(0,i.Wm)($,{filled:"",modelValue:Q.verificadorValor,"onUpdate:modelValue":a[2]||(a[2]=e=>Q.verificadorValor=e),label:Q.indicadorSeleccionado.formula,hint:"Valor del indicador al día de hoy","lazy-rules":"",rules:[e=>e&&e.length>0||"Debe ingresar un valor"]},null,8,["modelValue","label","rules"])])),_:1}),(0,i.Wm)(H,{class:"q-pt-none"},{default:(0,i.w5)((()=>[(0,i.Wm)($,{type:"textarea",filled:"",modelValue:Q.verificadorDescripcion,"onUpdate:modelValue":a[3]||(a[3]=e=>Q.verificadorDescripcion=e),label:"Descripción o comentarios sobre valor indicado","lazy-rules":"",rules:[e=>e&&e.length>0||"Debe ingresar una descripción o comentario"]},null,8,["modelValue","rules"])])),_:1})])),_:1})])),_:1})])]),(0,i.Wm)(Y,{inset:""})])),_:1},8,["done"]),(0,i.Wm)(R,{name:3,title:"Adjunta",icon:"create_new_folder",class:"tarjetaAmarilla"},{default:(0,i.w5)((()=>[D,A,(0,i.Wm)(O,{baseDir:Q.indicadorSeleccionado.dirGoogle},null,8,["baseDir"]),Q.entrega.adjuntosNuevaEntrega?((0,i.wg)(),(0,i.iD)("div",S,[Z,((0,i.wg)(!0),(0,i.iD)(i.HY,null,(0,i.Ko)(Q.entrega.adjuntosNuevaEntrega,(e=>((0,i.wg)(),(0,i.j4)(ee,{bordered:"",key:e.id},{default:(0,i.w5)((()=>[(0,i.wy)(((0,i.wg)(),(0,i.j4)(X,{clickable:"",onClick:a=>Q.clickAdjunto(e)},{default:(0,i.w5)((()=>[(0,i.Wm)(T,null,{default:(0,i.w5)((()=>[(0,i.Wm)(M,{caption:""},{default:(0,i.w5)((()=>[(0,i.Uk)((0,o.zw)(e.name),1)])),_:2},1024),(0,i.Wm)(M,{caption:""},{default:(0,i.w5)((()=>[(0,i.Uk)((0,o.zw)(e.type),1)])),_:2},1024)])),_:2},1024),(0,i.Wm)(T,{avatar:""},{default:(0,i.w5)((()=>[(0,i.Wm)(J,{color:"primary",name:"file_download"})])),_:1})])),_:2},1032,["onClick"])),[[ie]])])),_:2},1024)))),128))])):(0,i.kq)("",!0)])),_:1})])),_:1},8,["modelValue"])])):((0,i.wg)(),(0,i.iD)("div",P,z))])}var N=l(61959),F=l(93617),I=l(28339),H=l(52556),L=l(76731);const G={components:{Picker:H.Z,PopupCancelarNuevaEntrega:L.Z},setup(){const e=(0,F.oR)(),a=(0,I.tv)(),l=(0,i.Fl)((()=>e.state.entrega)),o=(0,i.Fl)((()=>e.state.verificador)),r=(0,i.Fl)((()=>e.state.accion)),t=(0,i.Fl)((()=>e.state.usuarix)),n=(0,N.iH)(null),s=(0,N.iH)(null),c=(0,N.iH)(null),d=(0,N.iH)(!1),u=(0,N.iH)(""),p=e=>{window.open(e.url)},m=()=>{const a={usuario:t.value.usuario.id,indicador:n.value.id,valor:s.value,descripcion:c.value,adjuntos:l.value.adjuntosNuevaEntrega};e.dispatch("verificador/postVerificador",a)};return(0,i.bv)((()=>{l.value.nuevaEntrega&&e.dispatch("accion/reqFuncionesPorAccion",l.value.nuevaEntrega.id)})),(0,i.Ah)((()=>{e.dispatch("verificador/limpiaNuevoVerificador"),e.dispatch("producto/limpiaNuevoProducto"),e.dispatch("entrega/limpiaAdjuntos")})),{clickAdjunto:p,verificador:o,entrega:l,accion:r,indicadorSeleccionado:n,verificadorValor:s,verificadorDescripcion:c,mostrarPopupCancelar:d,respuestaPopupCancelar:u,handlerPopupCancelar:e=>{d.value=!1,"guarda"==e?(m(),a.push("acciones")):"sale"==e&&a.push("acciones")},submitVerificador:m,enviaAlLider:()=>{e.dispatch("entrega/workflowEnviaAlLider",{entrega_id:o.value.nuevoVerificador.id,entrega_tipo:"verificador"})},step:(0,N.iH)(1),clicCancelar:()=>{c.value?d.value=!0:a.push("acciones")}}}};var K=l(74260),R=l(48240),Y=l(83518),$=l(96552),B=l(10151),O=l(25589),M=l(99367),T=l(38761),J=l(65869),X=l(68689),ee=l(34842),ae=l(27011),le=l(83414),ie=l(52035),oe=l(2350),re=l(24554),te=l(90118),ne=l(46489),se=l(7518),ce=l.n(se);const de=(0,K.Z)(G,[["render",U]]),ue=de;ce()(G,"components",{QBtn:R.Z,QStepper:Y.Z,QStep:$.Z,QCard:B.Z,QCardSection:O.Z,QCardActions:M.Z,QBtnToggle:T.Z,QSeparator:J.Z,QForm:X.Z,QInput:ee.Z,QList:ae.Z,QItem:le.Z,QItemSection:ie.Z,QItemLabel:oe.Z,QIcon:re.Z,QStepperNavigation:te.Z}),ce()(G,"directives",{Ripple:ne.Z})}}]);