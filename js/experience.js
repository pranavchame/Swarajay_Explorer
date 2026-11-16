'use strict';
(() => {
 const motion=()=>window.SWMotion?.allowed()!==false;
 const progress=document.createElement('div');progress.className='reading-progress';progress.setAttribute('aria-hidden','true');document.body.append(progress);
 const topButton=document.createElement('button');topButton.className='back-to-top';topButton.type='button';topButton.setAttribute('aria-label','Back to top');topButton.innerHTML='<span aria-hidden="true">↑</span>';topButton.hidden=true;document.body.append(topButton);
 topButton.addEventListener('click',()=>{window.scrollTo({top:0,behavior:motion()?'smooth':'instant'});document.querySelector('.skip')?.focus({preventScroll:true});});
 const hero=document.querySelector('.cinema-photo');
 const sections=[...document.querySelectorAll('.detail-jump a')].map(a=>({a,section:document.querySelector(a.getAttribute('href'))})).filter(x=>x.section);
 let frame=0;
 function paint(){frame=0;const y=window.scrollY,max=document.documentElement.scrollHeight-innerHeight;progress.style.transform=`scaleX(${max>0?Math.min(1,Math.max(0,y/max)):0})`;topButton.hidden=y<600;
  if(hero)hero.style.setProperty('--scroll-y',motion()?Math.min(y*.13,100)+'px':'0px');
  if(sections.length){let current=sections[0];for(const item of sections)if(item.section.getBoundingClientRect().top<innerHeight*.36)current=item;for(const {a} of sections){if(a===current.a)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');}}
 }
 const schedule=()=>{if(!frame)frame=requestAnimationFrame(paint);};addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule);document.addEventListener('sw:motionchange',schedule);paint();
 if('ResizeObserver' in window)new ResizeObserver(schedule).observe(document.querySelector('main')||document.body);
 // Stagger cards as they enter the viewport; opacity never depends on JavaScript succeeding.
 const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(!entry.isIntersecting)return;const el=entry.target;observer.unobserve(el);if(motion())el.animate([{opacity:.35,translate:'0 22px'},{opacity:1,translate:'0 0'}],{duration:430,delay:Number(el.dataset.motionOrder||0)*45,easing:'cubic-bezier(.2,.7,.2,1)'});}),{threshold:.08});
 document.querySelectorAll('.fort-card,.journal-tile,.heritage-stop').forEach((el,i)=>{el.dataset.motionOrder=i%3;observer.observe(el);});
 document.querySelectorAll('details').forEach(details=>{
  const summary=details.querySelector('summary');if(!summary)return;
  let running=null,closing=false;
  summary.addEventListener('click',event=>{
   if(!motion())return;
   event.preventDefault();const start=details.getBoundingClientRect().height;
   const wantOpen=running?closing:!details.open;
   running?.cancel();running=null;
   if(wantOpen){details.open=true;details.style.height='auto';}
   const end=wantOpen?details.getBoundingClientRect().height:summary.getBoundingClientRect().height+parseFloat(getComputedStyle(details).paddingTop)+parseFloat(getComputedStyle(details).paddingBottom)+2;
   closing=!wantOpen;details.style.overflow='hidden';running=details.animate({height:[start+'px',end+'px']},{duration:250,easing:'ease-out'});
   running.onfinish=()=>{details.open=wantOpen;details.style.overflow='';details.style.height='';running=null;schedule();};
  });
  document.addEventListener('sw:motionchange',()=>{if(!motion()&&running){running.cancel();details.open=!closing;running=null;details.style.overflow='';details.style.height='';}});
 });
 const viewer=document.querySelector('#lightbox'),photo=viewer?.querySelector(':scope > img');
 if(photo){let animation;const reveal=()=>{if(!viewer.open||!motion())return;animation?.cancel();animation=photo.animate([{opacity:.15,translate:'16px 0'},{opacity:1,translate:'0 0'}],{duration:260,easing:'ease-out'});};photo.addEventListener('load',reveal);new MutationObserver(()=>{if(photo.complete)reveal();}).observe(photo,{attributes:true,attributeFilter:['src']});}
 document.querySelectorAll('[data-save]').forEach(button=>button.addEventListener('click',()=>{if(motion())button.animate([{scale:1},{scale:1.06},{scale:1}],{duration:300,easing:'ease-out'});}));
 document.addEventListener('sw:motionchange',()=>{if(!motion()){document.getAnimations().forEach(a=>a.cancel());document.querySelectorAll('[data-tilt],[data-magnetic],[data-parallax]').forEach(el=>{el.style.transform='';el.style.setProperty('--px','0px');el.style.setProperty('--py','0px');});}});
})();
