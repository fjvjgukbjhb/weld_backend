(self.webpackChunkant_design_pro=self.webpackChunkant_design_pro||[]).push([[9483],{87615:function(g,s,e){"use strict";e.r(s),e.d(s,{default:function(){return te}});var n=e(66456),d=e(15711),m=e(58024),f=e(91894),U=e(13062),K=e(71230),r=e(57663),E=e(71577),Z=e(89032),t=e(15746),c=e(9715),P=e(55843),z=e(47673),R=e(4107),O=e(34792),I=e(48086),D=e(32059),o=e(11849),x=e(2824),ce=e(14965),G=e(91774),me=e(43358),k=e(34041),S=e(67294),X=e(61128),j=e(39428),F=e(3182),H=e(21010);function V(T){return N.apply(this,arguments)}function N(){return N=(0,F.Z)((0,j.Z)().mark(function T(C){return(0,j.Z)().wrap(function(u){for(;;)switch(u.prev=u.next){case 0:return u.abrupt("return",(0,H.WY)("/api/user_action/query_by",{method:"POST",data:C}));case 1:case"end":return u.stop()}},T)})),N.apply(this,arguments)}function _(T){return B.apply(this,arguments)}function B(){return B=(0,F.Z)((0,j.Z)().mark(function T(C){return(0,j.Z)().wrap(function(u){for(;;)switch(u.prev=u.next){case 0:return u.abrupt("return",(0,H.WY)("/api/user_action/query_all",{method:"GET",params:C}));case 1:case"end":return u.stop()}},T)})),B.apply(this,arguments)}var a=e(85893),ve=k.Z.Option,q=G.Z.RangePicker,fe=[{id:"1",username:"John ",actionTime:"2022-3-1 19:00:00",actionName:"\u4E0B\u8F7D\u62A5\u544A",content:"\u4E0B\u8F7D\u4E86\u4E00\u4EFD\u62A5\u544A",pageName:"\u901A\u98CE\u673A\u9875\u9762",pageUrl:"www.example.com/poster.html",element:"\u76F8\u4F3C\u8BBE\u8BA1"},{id:"2",username:"John ",actionTime:"2022-3-1 19:00:00",actionName:"\u4E0B\u8F7D\u62A5\u544A",content:"\u4E0B\u8F7D\u4E86\u4E00\u4EFD\u62A5\u544A",pageName:"\u901A\u98CE\u673A\u9875\u9762",pageUrl:"www.example.com/poster.html",element:"\u76F8\u4F3C\u8BBE\u8BA1"},{id:"3",username:"John ",actionTime:"2022-3-1 19:00:00",actionName:"\u4E0B\u8F7D\u62A5\u544A",content:"\u4E0B\u8F7D\u4E86\u4E00\u4EFD\u62A5\u544A",pageName:"\u901A\u98CE\u673A\u9875\u9762",pageUrl:"www.example.com/poster.html",element:"\u76F8\u4F3C\u8BBE\u8BA1"}],ee=function(C){var v=10,u=(0,S.useState)(1),$=(0,x.Z)(u,2),Y=$[0],ne=$[1],ae=(0,S.useState)([]),w=(0,x.Z)(ae,2),re=w[0],L=w[1],oe=(0,S.useState)({}),J=(0,x.Z)(oe,2),W=J[0],se=J[1],le=function(l){var p,h=Object.keys(l).filter(function(i){return l[i]!==null&&l[i]!==void 0}).reduce(function(i,M){return(0,o.Z)((0,o.Z)({},i),{},(0,D.Z)({},M,l[M]))},{}),A={};if(((p=l.actionTime)===null||p===void 0?void 0:p.length)>0){var Q=l.actionTime;A=(0,o.Z)((0,o.Z)({},h),{},{beginTime:Q[0].format("YYYY-MM-DD HH:mm:ss"),endTime:Q[1].format("YYYY-MM-DD HH:mm:ss")})}else A=(0,o.Z)({},h);se(A);var de=(0,o.Z)((0,o.Z)({},A),{},{pageNo:Y,pageSize:v});V(de).then(function(i){var M,b;console.log("@@",i==null||(M=i.data)===null||M===void 0?void 0:M.data),L(i==null||(b=i.data)===null||b===void 0?void 0:b.data)}).catch(function(i){I.default.error("\u8BF7\u6C42\u5931\u8D25\uFF01")})};console.log("#####",W),(0,S.useEffect)(function(){_({pageNo:Y,pageSize:v}).then(function(y){L(y==null?void 0:y.data)}).catch(function(y){I.default.error("\u8BF7\u6C42\u5931\u8D25\uFF01")})},[]);var ie=function(l){ne(l);var p={};Object.keys(W).length>0?p=(0,o.Z)((0,o.Z)({},W),{},{page:l,pageSize:v}):p={page:l,pageSize:v},_(p).then(function(h){L(h==null?void 0:h.data)}).catch(function(h){I.default.error("\u8BF7\u6C42\u5931\u8D25\uFF01")})},ue=[{title:"\u5E8F\u53F7",dataIndex:"id",key:"id",render:function(l){return"".concat(v*(Y-1)+parseInt(l)+1)}},{title:"\u4E8B\u4EF6\u540D\u79F0",dataIndex:"actionName",key:"actionName"},{title:"\u4E8B\u4EF6\u5185\u5BB9",dataIndex:"content",key:"content"},{title:"\u9875\u9762\u540D\u79F0",dataIndex:"pageName",key:"pageName"},{title:"\u9875\u9762\u94FE\u63A5",dataIndex:"pageUrl",key:"pageUrl"},{title:"\u9875\u9762\u533A\u57DF",dataIndex:"element",key:"element"},{title:"\u4E8B\u4EF6\u7528\u6237",dataIndex:"username",key:"username"},{title:"\u4E8B\u4EF6\u65F6\u95F4",dataIndex:"actionTime",key:"actionTime"}];return(0,a.jsx)("div",{children:(0,a.jsxs)(X.ZP,{children:[(0,a.jsx)(f.Z,{children:(0,a.jsx)(P.Z,{layout:"horizontal",onFinish:le,children:(0,a.jsxs)(K.Z,{gutter:24,children:[(0,a.jsx)(t.Z,{span:6,children:(0,a.jsx)(P.Z.Item,{label:"\u4E8B\u4EF6\u7528\u6237",name:"username",children:(0,a.jsx)(R.Z,{})})}),(0,a.jsx)(t.Z,{span:10,children:(0,a.jsx)(P.Z.Item,{label:"\u4E8B\u4EF6\u65F6\u95F4",name:"actionTime",children:(0,a.jsx)(q,{showTime:!0,format:"YYYY-MM-DD HH:mm:ss"})})}),(0,a.jsx)(t.Z,{span:4,children:(0,a.jsx)(P.Z.Item,{wrapperCol:{xs:{span:24,offset:0},sm:{span:16,offset:8}},children:(0,a.jsx)(E.Z,{type:"primary",htmlType:"submit",children:"\u67E5\u8BE2"})})})]})})}),(0,a.jsx)(d.Z,{columns:ue,dataSource:re,pagination:{defaultPageSize:v,onChange:ie,total:3,simple:!0}})]})})},te=ee},34952:function(g,s,e){"use strict";var n=e(22122),d=e(15105),m=e(67294),f=function(r,E){var Z={};for(var t in r)Object.prototype.hasOwnProperty.call(r,t)&&E.indexOf(t)<0&&(Z[t]=r[t]);if(r!=null&&typeof Object.getOwnPropertySymbols=="function")for(var c=0,t=Object.getOwnPropertySymbols(r);c<t.length;c++)E.indexOf(t[c])<0&&Object.prototype.propertyIsEnumerable.call(r,t[c])&&(Z[t[c]]=r[t[c]]);return Z},U={border:0,background:"transparent",padding:0,lineHeight:"inherit",display:"inline-block"},K=m.forwardRef(function(r,E){var Z=function(D){var o=D.keyCode;o===d.Z.ENTER&&D.preventDefault()},t=function(D){var o=D.keyCode,x=r.onClick;o===d.Z.ENTER&&x&&x()},c=r.style,P=r.noStyle,z=r.disabled,R=f(r,["style","noStyle","disabled"]),O={};return P||(O=(0,n.Z)({},U)),z&&(O.pointerEvents="none"),O=(0,n.Z)((0,n.Z)({},O),c),m.createElement("div",(0,n.Z)({role:"button",tabIndex:0,ref:E},R,{onKeyDown:Z,onKeyUp:t,style:O}))});s.Z=K},15746:function(g,s,e){"use strict";var n=e(21584);s.Z=n.Z},89032:function(g,s,e){"use strict";var n=e(38663),d=e.n(n),m=e(6999)},71230:function(g,s,e){"use strict";var n=e(92820);s.Z=n.Z},13062:function(g,s,e){"use strict";var n=e(38663),d=e.n(n),m=e(6999)},97435:function(g,s){"use strict";function e(n,d){for(var m=Object.assign({},n),f=0;f<d.length;f+=1){var U=d[f];delete m[U]}return m}s.Z=e}}]);
