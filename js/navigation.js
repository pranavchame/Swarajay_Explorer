'use strict';
(() => {
 const nav=document.querySelector('#main-nav'),toggle=document.querySelector('.menu-toggle');if(!nav||!toggle)return;
 const links=[...nav.querySelectorAll('a')],indicator=nav.querySelector('.nav-indicator'),desktop=matchMedia('(min-width:1024px)');
 const active=()=>nav.querySelector('[aria-current="page"]');
 function point(link){if(!desktop.matches)return;indicator.style.opacity=link?'1':'0';links.forEach(x=>x.classList.toggle('indicator-target',x===link));if(!link)return;const a=link.getBoundingClientRect(),b=nav.getBoundingClientRect();indicator.style.width=a.width+'px';indicator.style.transform=`translateX(${a.left-b.left}px)`;}
 function close(focus=false){nav.classList.remove('open');document.body.classList.remove('nav-open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Open navigation');document.querySelectorAll('main,.site-footer').forEach(x=>x.inert=false);if(focus)toggle.focus();}
 toggle.addEventListener('click',()=>{if(nav.classList.contains('open'))return close();nav.classList.add('open');document.body.classList.add('nav-open');toggle.setAttribute('aria-expanded','true');toggle.setAttribute('aria-label','Close navigation');document.querySelectorAll('main,.site-footer').forEach(x=>x.inert=true);});
 document.querySelector('.nav-backdrop')?.addEventListener('click',()=>close(true));
 document.addEventListener('keydown',event=>{if(!nav.classList.contains('open'))return;if(event.key==='Escape'){event.preventDefault();close(true);}if(event.key==='Tab'){const last=links.at(-1);if(event.shiftKey&&document.activeElement===toggle){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();toggle.focus();}}});
 links.forEach(a=>a.addEventListener('click',()=>close()));
 nav.addEventListener('pointerover',event=>{const link=event.target.closest('a');if(link)point(link);});nav.addEventListener('pointerleave',()=>point(active()));
 nav.addEventListener('focusin',event=>point(event.target.closest('a')));nav.addEventListener('focusout',()=>requestAnimationFrame(()=>point(nav.contains(document.activeElement)?document.activeElement:active())));
 new ResizeObserver(()=>point(active())).observe(nav);desktop.addEventListener('change',()=>{close();point(active());});document.fonts?.ready.then(()=>point(active()));point(active());
})();
