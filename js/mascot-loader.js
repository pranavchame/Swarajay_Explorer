'use strict';
(() => {
 const src=document.currentScript.dataset.mascotSrc,desktop=matchMedia('(min-width:1024px)');let loaded=false;
 function load(){if(!loaded&&desktop.matches){loaded=true;const script=document.createElement('script');script.src=src;script.defer=true;document.head.append(script);}}
 desktop.addEventListener('change',load);load();
})();
