"use strict";(self.modernJsonp=self.modernJsonp||[]).push([[6881],{25690:(e,t,n)=>{n.d(t,{default:()=>r});var i=n(718222);let a=`pulsing {
  0% {
    opacity: 1;
  }

  50% {
    opacity: 0.4;
  }

  100% {
    opacity: 1;
  }
}`,r={css:(0,i.Ll)([a]),animation:"pulsing 2s infinite"}},718222:(e,t,n)=>{n.d(t,{CC:()=>a,Ll:()=>o,XF:()=>r});let i=(e,t,n)=>({x:Math.floor(e*Math.cos(n)),y:Math.floor(t*Math.sin(n))}),a=(e,t)=>i(t/2,e/2,2*Math.random()*Math.PI),r=(e,t)=>Math.floor(Math.random()*(t-e+1))+e,o=e=>["@-webkit-keyframes","@keyframes"].map(t=>e.map(e=>t+" "+e).join(`
`)).join(`
`)},633569:(e,t,n)=>{n.r(t),n.d(t,{default:()=>S});var i=n(667294),a=n(883119),r=n(19963),o=n(756064);function l(e,t,n){var i;return(t="symbol"==typeof(i=function(e,t){if("object"!=typeof e||!e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var i=n.call(e,t||"default");if("object"!=typeof i)return i;throw TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(t,"string"))?i:i+"")in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}let s={},u=e=>{let t=e.__id||e.id;return"string"==typeof t&&t||null};class m{constructor(){l(this,"idMap",new Map),l(this,"objMap",new WeakMap)}get(e){let t=u(e);return this.objMap.get(e)??(t?this.idMap.get(t):void 0)}has(e){let t=u(e);return this.objMap.has(e)??(!!t&&this.idMap.has(t))}set(e,t){let n=u(e);n&&this.idMap.set(n,t),this.objMap.set(e,t)}reset(){this.idMap=new Map,this.objMap=new WeakMap}}function p(e,t){return"number"==typeof e?e:"_lg1"===t?e[t]??e.lg??1:e[t]??1}var d=n(399083),c=n(824834),h=n(876594),g=n(25690),f=n(970601),y=n(785893);let{css:x,animation:b}=g.default,_={backgroundColor:h._VP,animation:b,borderRadius:h.Ev2};function w({data:e}){let{height:t}=e;return(0,y.jsxs)(i.Fragment,{children:[(0,y.jsx)(f.Z,{unsafeCSS:x}),(0,y.jsx)(a.xu,{dangerouslySetInlineStyle:{__style:_},"data-test-id":"skeleton-pin",children:(0,y.jsx)(a.xu,{height:t})})]})}var v=n(56063),M=n(967312),C=n(174646),k=n(538645),$=n(992114),j=n(438596);function S(e){let{align:t,cacheKey:n,id:l,isFetching:u,isGridCentered:h=!0,items:g,layout:x,loadItems:b,masonryRef:_,optOutFluidGridExperiment:S=!1,renderItem:R,scrollContainerRef:W,virtualize:A=!0,_getColumnSpanConfig:I,_getResponsiveModuleConfigForSecondItem:F,_dynamicHeights:G,isLoadingStateEnabled:E,initialLoadingStatePinCount:P,isLoadingAccessibilityLabel:O,isLoadedAccessibilityLabel:H}=e,N=(0,k.ZP)(),{isAuthenticated:T,isRTL:X}=(0,C.B)(),{logContextEvent:B}=(0,r.v)(),Z=(0,M.F)(),z="desktop"===N,Q=(0,j.MM)(),J=((0,i.useRef)(g.map(()=>({fetchTimestamp:Date.now(),measureTimestamp:Date.now(),hasRendered:!1,pageCount:0}))),z&&!S),{experimentalColumnWidth:L,experimentalGutter:V}=(0,d.Z)(J),q=e.serverRender??!!z,D="flexible"===x||"uniformRowFlexible"===x||"desktop"!==N||J,K=(D&&x?.startsWith("uniformRow")?"uniformRowFlexible":void 0)??(q?"serverRenderedFlexible":"flexible"),U=e.columnWidth??L??v.yF;D&&(U=Math.floor(U));let Y=e.gutterWidth??V??(z?v.oX:1),ee=e.minCols??v.yc,et=(0,i.useRef)(0),en=U+Y,ei=function(e){if(null==e)return;let t=function(e){let t=s[e];return t&&t.screenWidth===window.innerWidth||(s[e]={screenWidth:window.innerWidth}),s[e]}(e);return t.measurementCache||(t.measurementCache=new m),t.measurementCache}(n),ea=(0,i.useCallback)(()=>W?.current||window,[W]),er=(0,i.useRef)(!0),eo=(e,t)=>{let n={itemsBatchSize:5,whitespaceThreshold:0,iterationsLimit:15e3};return t>3&&(n.whitespaceThreshold=Y*t),e>=7&&(n.itemsBatchSize=7),n},{anyEnabled:el,group:es}=Z.checkExperiment("web_masonry_enable_dynamic_heights_for_all"),{anyEnabled:eu}=Z.checkExperiment("web_masonry_pin_overlap_calculation_and_logging"),em=h&&er.current?"centered":"",{className:ep,styles:ed}=function(e){let t=`m_${Object.keys(e).sort().reduce((t,n)=>{let i=e[n];return null==i||"object"==typeof i||"function"==typeof i?t:"boolean"==typeof i?t+(i?"t":"f"):t+i},"").replace(/\:/g,"\\:")}`,{flexible:n,gutterWidth:i,isRTL:a,itemWidth:r,maxColumns:o,minColumns:l,items:s,_getColumnSpanConfig:u,_getResponsiveModuleConfigForSecondItem:m}=e,d=u?s.map((e,t)=>({index:t,columnSpanConfig:u(e)??1})).filter(e=>1!==e.columnSpanConfig):[],c=r+i,h=Array.from({length:o+1-l},(e,t)=>t+l).map(e=>{let h,g,f=e===l?0:e*c,y=e===o?null:(e+1)*c-.01;u&&m&&s.length>1&&(h=u(s[0]),g=m(s[1]));let{styles:x,numberOfVisibleItems:b}=d.reduce((a,o)=>{let{columnSpanConfig:l}=o,u=Math.min(function({columnCount:e,columnSpanConfig:t,firstItemColumnSpanConfig:n,isFlexibleWidthItem:i,secondItemResponsiveModuleConfig:a}){let r=e<=2?"sm":e<=4?"md":e<=6?"_lg1":e<=8?"lg":"xl",o=p(t,r);if(i){let t=p(n,r);o="number"==typeof a?a:a?Math.max(a.min,Math.min(a.max,e-t)):1}return o}({columnCount:e,columnSpanConfig:l,isFlexibleWidthItem:!!g&&o===s[1],firstItemColumnSpanConfig:h??1,secondItemResponsiveModuleConfig:g??1}),e),m=null!=o.index&&a.numberOfVisibleItems>=u+o.index,d=n?100/e*u:r*u+i*(u-1),{numberOfVisibleItems:c}=a;return m?c-=u-1:o.index<c&&(c+=1),{styles:a.styles.concat(function({className:e,index:t,columnSpanConfig:n,visible:i,width:a,flexible:r}){let o="number"==typeof n?n:btoa(JSON.stringify(n));return r?`
      .${e} .static[data-column-span="${o}"]:nth-child(${t+1}) {
        visibility: ${i?"visible":"hidden"} !important;
        position: ${i?"inherit":"absolute"} !important;
        width: ${a}% !important;
      }`:`
      .${e} .static[data-column-span="${o}"]:nth-child(${t+1}) {
        visibility: ${i?"visible":"hidden"} !important;
        position: ${i?"inherit":"absolute"} !important;
        width: ${a}px !important;
      }`}({className:t,index:o.index,columnSpanConfig:l,visible:m,width:d,flexible:n})),numberOfVisibleItems:c}},{styles:"",numberOfVisibleItems:e}),_=n?`
      .${t} .static {
        box-sizing: border-box;
        width: calc(100% / ${e}) !important;
      }
    `:`
      .${t} {
        max-width: ${e*c}px;
      }

      .${t} .static {
        width: ${r}px !important;
      }
    `;return{minWidth:f,maxWidth:y,styles:`
      .${t} .static:nth-child(-n+${b}) {
        position: static !important;
        visibility: visible !important;
        float: ${a?"right":"left"};
        display: block;
      }

      .${t} .static {
        padding: 0 ${i/2}px;
      }

      ${_}

      ${x}
    `}}),g=h.map(({minWidth:e,maxWidth:t,styles:n})=>`
    @container (min-width: ${e}px) ${t?`and (max-width: ${t}px)`:""} {
      ${n}
    }
  `),f=h.map(({minWidth:e,maxWidth:t,styles:n})=>`
    @media (min-width: ${e}px) ${t?`and (max-width: ${t}px)`:""} {
      ${n}
    }
  `),y=`
    ${g.join("")}
    @supports not (container-type: inline-size) {
      ${f.join("")}
    }
  `;return{className:t,styles:`
    .masonryContainer:has(.${t}) {
      container-type: inline-size;
    }

    .masonryContainer > .centered {
      margin-left: auto;
      margin-right: auto;
    }

    .${t} .static {
      position: absolute !important;
      visibility: hidden !important;
    }

    ${y}
  `}}({gutterWidth:Y,flexible:D,items:g,isRTL:X,itemWidth:U,maxColumns:e.maxColumns??Math.max(g.length,v.g5),minColumns:ee,_getColumnSpanConfig:I,_getResponsiveModuleConfigForSecondItem:F}),ec=`${em} ${ep}`.trim(),{anyEnabled:eh,expName:eg,group:ef,isMeasureAllEnabled:ey}=(0,c.Z)(),ex=((0,i.useRef)(void 0),(0,i.useRef)(g.length)),eb=(0,i.useRef)(0),e_=(0,i.useRef)(null);(0,i.useEffect)(()=>{ex.current=g.length,eb.current+=1},[g]),(0,i.useEffect)(()=>{er.current&&(er.current=!1)},[]),(0,i.useEffect)(()=>()=>{},[]);let ew=(0,i.useCallback)(e=>{let t=e.reduce((e,t)=>e+t),n=t/e.length;(0,$.S0)("webapp.masonry.multiColumnWhitespace.average",n,{sampleRate:1,tags:{experimentalMasonryGroup:ef||"unknown",handlerId:Q,isAuthenticated:T,multiColumnItemSpan:e.length}}),(0,$.S0)("webapp.masonry.twoColWhitespace",n,{sampleRate:1,tags:{columnWidth:U,minCols:ee}}),B({event_type:15878,component:14468,aux_data:{total_whitespace_px:t}}),B({event_type:16062,component:14468,aux_data:{average_whitespace_px:n}}),B({event_type:16063,component:14468,aux_data:{max_whitespace_px:Math.max(...e)}}),e.forEach(t=>{t>=50&&((0,$.nP)("webapp.masonry.multiColumnWhitespace.over50",{sampleRate:1,tags:{experimentalMasonryGroup:ef||"unknown",handlerId:Q,isAuthenticated:T,multiColumnItemSpan:e.length}}),B({event_type:16261,component:14468})),t>=100&&((0,$.nP)("webapp.masonry.multiColumnWhitespace.over100",{sampleRate:1,tags:{experimentalMasonryGroup:ef||"unknown",handlerId:Q,isAuthenticated:T,multiColumnItemSpan:e.length}}),B({event_type:16262,component:14468}))}),(0,$.nP)("webapp.masonry.multiColumnWhitespace.count",{sampleRate:1,tags:{experimentalMasonryGroup:ef||"unknown",handlerId:Q,isAuthenticated:T,multiColumnItemSpan:e.length}})},[U,B,ee,T,Q,ef]),{_items:ev,_renderItem:eM}=function({initialLoadingStatePinCount:e=50,infiniteScrollPinCount:t=10,isFetching:n,items:a=[],renderItem:r,isLoadingStateEnabled:o}){let l=+(a.filter(e=>"object"==typeof e&&null!==e&&"type"in e&&"closeup_module"===e.type).length>0),s=o&&n,u=(0,i.useMemo)(()=>Array.from({length:a.length>l?t:e}).reduce((e,t,n)=>[...e,{height:n%2==0?356:236,key:`skeleton-pin-${n}`,isSkeleton:!0}],[]),[a.length,l,t,e]);return{_items:(0,i.useMemo)(()=>s?[...a,...u]:a,[s,a,u]),_renderItem:(0,i.useMemo)(()=>o?e=>{let{itemIdx:t,data:n}=e;return t>=a.length&&n&&"object"==typeof n&&"key"in n&&"height"in n?(0,y.jsx)(w,{data:n},n.key):r(e)}:r,[o,r,a.length])}}({isLoadingStateEnabled:E,items:g,renderItem:(0,i.useCallback)(e=>(0,y.jsx)(o.Z,{name:"MasonryItem",children:R(e)}),[R]),isFetching:u,initialLoadingStatePinCount:P}),eC=E&&u,ek=(0,i.useRef)(new Set);return(0,i.useEffect)(()=>{if(!eu)return;let e=setTimeout(()=>{requestAnimationFrame(()=>{let e=Array.from(e_.current?.querySelectorAll("[data-grid-item-idx]")??[]);if(0===e.length)return;let t=e.map(e=>{let t=e.getAttribute("data-grid-item-idx");return{rect:e.getBoundingClientRect(),itemIdx:t}}),n=0,i=0,a=0,r=0,o=0,l=0;for(let e=0;e<t.length;e+=1){let s=t[e]?.rect,u=t[e]?.itemIdx;for(let m=e+1;m<t.length;m+=1){let e=t[m]?.rect,p=t[m]?.itemIdx;if(s&&e&&u&&p){let t=[u,p].sort().join("|");if(!ek.current.has(t)&&s.right>=e.left&&s.left<=e.right&&s.bottom>=e.top&&s.top<=e.bottom&&s.height>0&&e.height>0){ek.current.add(t),n+=1;let u=Math.max(0,Math.min(s.right,e.right)-Math.max(s.left,e.left))*Math.max(0,Math.min(s.bottom,e.bottom)-Math.max(s.top,e.top));u>8e4?l+=1:u>4e4?o+=1:u>1e4?r+=1:u>5e3?a+=1:u>2500&&(i+=1)}}}}n>0&&(0,$.QX)("webapp.masonry.pinOverlapHits",n,{tags:{isAuthenticated:T,isDesktop:z,handlerId:Q,experimentalMasonryGroup:ef||"unknown",dynamicHeightsForAllGroup:es||"unknown"}}),i>0&&(0,$.QX)("webapp.masonry.pinOverlap.AreaPx.over2500",i,{tags:{isAuthenticated:T,isDesktop:z,handlerId:Q,experimentalMasonryGroup:ef||"unknown",dynamicHeightsForAllGroup:es||"unknown"}}),a>0&&(0,$.QX)("webapp.masonry.pinOverlap.AreaPx.over5000",a,{tags:{isAuthenticated:T,isDesktop:z,handlerId:Q,experimentalMasonryGroup:ef||"unknown",dynamicHeightsForAllGroup:es||"unknown"}}),r>0&&(0,$.QX)("webapp.masonry.pinOverlap.AreaPx.over10000",r,{tags:{isAuthenticated:T,isDesktop:z,handlerId:Q,experimentalMasonryGroup:ef||"unknown",dynamicHeightsForAllGroup:es||"unknown"}}),o>0&&(0,$.QX)("webapp.masonry.pinOverlap.AreaPx.over40000",o,{tags:{isAuthenticated:T,isDesktop:z,handlerId:Q,experimentalMasonryGroup:ef||"unknown",dynamicHeightsForAllGroup:es||"unknown"}}),l>0&&(0,$.QX)("webapp.masonry.pinOverlap.AreaPx.over80000",l,{tags:{isAuthenticated:T,isDesktop:z,handlerId:Q,experimentalMasonryGroup:ef||"unknown",dynamicHeightsForAllGroup:es||"unknown"}})})},1e3);return()=>{clearTimeout(e)}},[U,ef,T,z,eu,g,Q,es]),(0,y.jsxs)(i.Fragment,{children:[E&&!er.current&&(0,y.jsx)(a.xu,{"aria-live":"polite",display:"visuallyHidden",children:eC?O:H}),(0,y.jsx)("div",{ref:e_,"aria-busy":E?!!eC:void 0,className:"masonryContainer","data-test-id":"masonry-container",id:l,style:J?{padding:`0 ${Y/2}px`}:void 0,children:(0,y.jsxs)("div",{className:ec,children:[q&&er.current?(0,y.jsx)(f.Z,{"data-test-id":"masonry-ssr-styles",unsafeCSS:ed}):null,(0,y.jsx)(a.xu,{"data-test-id":"max-width-container",marginBottom:0,marginEnd:"auto",marginStart:"auto",marginTop:0,maxWidth:e.maxColumns?en*e.maxColumns:void 0,children:eh?(0,y.jsx)(a.GX,{ref:e=>{_&&(_.current=e)},_dynamicHeights:el||G,_getColumnSpanConfig:I,_getModulePositioningConfig:eo,_getResponsiveModuleConfigForSecondItem:F,_logTwoColWhitespace:ew,_measureAll:ey,align:t,columnWidth:U,gutterWidth:Y,items:ev,layout:D?K:x??"basic",loadItems:b,measurementStore:ei,minCols:ee,renderItem:eM,scrollContainer:ea,virtualBufferFactor:.3,virtualize:A}):(0,y.jsx)(a.Rk,{ref:e=>{_&&(_.current=e)},_dynamicHeights:el||G,_getColumnSpanConfig:I,_getModulePositioningConfig:eo,_getResponsiveModuleConfigForSecondItem:F,_logTwoColWhitespace:ew,align:t,columnWidth:U,gutterWidth:Y,items:ev,layout:D?K:x??"basic",loadItems:b,measurementStore:ei,minCols:ee,renderItem:eM,scrollContainer:ea,virtualBufferFactor:.3,virtualize:A})})]})})]})}},399083:(e,t,n)=>{n.d(t,{Z:()=>i});function i(e=!0){let t=e?16:void 0,n=t?Math.floor(t/4):void 0;return{experimentalColumnWidth:e?221:void 0,experimentalGutter:t,experimentalGutterBoints:n}}},824834:(e,t,n)=>{n.d(t,{Z:()=>o});var i=n(967312),a=n(174646),r=n(438596);function o(e){let{isAuthenticated:t}=(0,a.B)(),{expName:n,anyEnabled:o,group:l}=function({experimentsClient:e,handlerId:t,isAuthenticated:n,skipActivation:i}){let{checkExperiment:a}=e,r=a(n?"web_masonry_v2_auth":"web_masonry_v2_unauth",{dangerouslySkipActivation:i});return r.group?{expName:n?"web_masonry_v2_auth":"web_masonry_v2_unauth",...r}:"www/[username]/[slug].js"!==t||n?"www/pin/[id].js"!==t||n?{expName:"",anyEnabled:!1,group:""}:{expName:"web_masonry_v2_unauth_pin",...a("web_masonry_v2_unauth_pin",{dangerouslySkipActivation:i})}:{expName:"web_masonry_v2_unauth_board",...a("web_masonry_v2_unauth_board",{dangerouslySkipActivation:i})}}({experimentsClient:(0,i.F)(),handlerId:(0,r.MM)(),isAuthenticated:t,skipActivation:e?.skipActivation??!1});return{expName:n,anyEnabled:o,group:l,isMeasureAllEnabled:"enabled_measure_all"===l||"enabled_measure_all_impression_fix"===l,isImpressionFixEnabled:"control_impression_fix"===l||"enabled_impression_fix"===l||"enabled_measure_all_impression_fix"===l}}}}]);
//# sourceMappingURL=https://sm.pinimg.com/webapp/6881-95cdd0a45065b95b.mjs.map