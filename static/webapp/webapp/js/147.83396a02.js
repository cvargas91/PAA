"use strict";(self["webpackChunkspci"]=self["webpackChunkspci"]||[]).push([[147],{16147:(e,a,o)=>{o.r(a),o.d(a,{default:()=>w});var t=o(83673);const i=(0,t._)("div",{class:"q-pa-md"},[(0,t._)("div",{class:"text-h6 text-textoAzul"},[(0,t._)("b",null,"Retroalimentación de productos y verificadores")])],-1),l={key:0,class:"q-pa-md"},n={key:1,class:"q-pa-md"};function r(e,a,o,r,c,s){const d=(0,t.up)("q-table"),m=(0,t.up)("q-page");return(0,t.wg)(),(0,t.j4)(m,null,{default:(0,t.w5)((()=>[i,e.retroalimentacion_productos?((0,t.wg)(),(0,t.iD)("div",l,[(0,t.Wm)(d,{title:"Productos",rows:e.retroalimentacion_productos,columns:e.columnasTablas,"row-key":"name"},null,8,["rows","columns"])])):(0,t.kq)("",!0),e.retroalimentacion_verificadores?((0,t.wg)(),(0,t.iD)("div",n,[(0,t.Wm)(d,{title:"Verificadores",rows:e.retroalimentacion_verificadores,columns:e.columnasTablas,"row-key":"name"},null,8,["rows","columns"])])):(0,t.kq)("",!0)])),_:1})}var c=o(93617);const s=(0,t.aZ)({setup(){const e=(0,c.oR)(),a=[{name:"retroalimentacion",label:"Detalle de la retroalimentación",align:"left",style:"white-space: normal",field:e=>e.retroalimentacion},{name:"modificado",label:"Fecha última modificación",align:"left",field:e=>e.modificado},{name:"creado",label:"Fecha creación",align:"left",field:e=>e.creado}];return(0,t.bv)((()=>{e.dispatch("entrega/setRetroalimentaciones")})),{columnasTablas:a,retroalimentacion_productos:(0,t.Fl)((()=>e.state.entrega.retroalimentacion_productos)),retroalimentacion_verificadores:(0,t.Fl)((()=>e.state.entrega.retroalimentacion_verificadores))}}});var d=o(74260),m=o(24379),u=o(82138),f=o(7518),p=o.n(f);const v=(0,d.Z)(s,[["render",r]]),w=v;p()(s,"components",{QPage:m.Z,QTable:u.Z})}}]);