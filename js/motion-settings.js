'use strict';
window.SWMotion = (() => {
 const media=matchMedia('(prefers-reduced-motion: reduce)');
 let paused=false;
 try {paused=localStorage.getItem('swarajya-motion')==='off';} catch {}
 const allowed=()=>!paused&&!media.matches;
 function sync(){
  document.documentElement.classList.toggle('motion-paused',!allowed());
  document.querySelectorAll('[data-motion-toggle]').forEach(button=>{
   button.textContent=media.matches?'Motion: Reduced':paused?'Motion: Off':'Motion: On';
   button.setAttribute('aria-pressed',String(!allowed()));
   button.setAttribute('aria-label',media.matches?'Decorative animations reduced by device preference':paused?'Enable decorative animations':'Reduce decorative animations');
   button.disabled=media.matches;
   button.title=media.matches?'Your device requests reduced motion.':'Turn decorative animations on or off';
  });
  document.dispatchEvent(new Event('sw:motionchange'));
 }
 function toggle(){paused=!paused;try{localStorage.setItem('swarajya-motion',paused?'off':'on');}catch{}sync();}
 media.addEventListener('change',sync);
 document.addEventListener('DOMContentLoaded',()=>{document.querySelectorAll('[data-motion-toggle]').forEach(b=>b.addEventListener('click',toggle));sync();});
 document.documentElement.classList.toggle('motion-paused',!allowed());
 return {allowed};
})();
