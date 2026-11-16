'use strict';
window.SW = (() => {
  const root = new URL('../', document.currentScript.src);
  const forts = window.FORTS || [];
  const url = path => new URL(path, root).href;
  const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const normalize = value => String(value ?? '').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const readSaved = () => { try { const saved=JSON.parse(localStorage.getItem('swarajya-saved') || '[]'); return Array.isArray(saved)?saved.filter(s=>typeof s==='string'):[]; } catch { return []; } };
  const query = values => {
    const needle=normalize(values.q).trim();
    const saved=readSaved();
    return forts.filter(f => (!needle || normalize([f.name,f.marathi_name,...f.aliases,f.district,f.region,f.type,f.nearest_city].join(' ')).includes(needle)) &&
      (!values.district || f.district===values.district) && (!values.region || f.region===values.region) &&
      (!values.type || f.type===values.type) && (!values.difficulty || (values.difficulty==='unknown' ? !f.difficulty : f.difficulty===values.difficulty)) &&
      (!values.recommendation || f.recommendation===values.recommendation) && (!values.saved || saved.includes(f.slug))).sort((a,b)=>values.sort==='district' ? a.district.localeCompare(b.district)||a.name.localeCompare(b.name) : a.name.localeCompare(b.name));
  };
  const formValues = form => ({q:form.elements.q.value,district:form.elements.district.value,region:form.elements.region.value,type:form.elements.type.value,difficulty:form.elements.difficulty.value,sort:form.elements.sort.value,recommendation:form.elements.recommendation?.value||'',saved:form.querySelector('#saved-only').checked});
  const initializeFilters = (form,fixedDistrict='') => {
    const params=new URLSearchParams(location.search);
    for (const key of ['q','district','region','type','difficulty','sort','recommendation']) if (form.elements[key]) form.elements[key].value=params.get(key) || (key==='sort'?'name':'');
    if (fixedDistrict) {form.elements.district.value=fixedDistrict;form.elements.district.disabled=true;}
    form.querySelector('#saved-only').checked=params.get('saved')==='1';
  };
  const syncQuery = values => {
    const params=new URLSearchParams(location.search);
    for(const key of ['q','district','region','type','difficulty','sort','recommendation']) {
      if(values[key] && !(key==='sort'&&values[key]==='name')) params.set(key,values[key]); else params.delete(key);
    }
    if(values.saved)params.set('saved','1');else params.delete('saved');
    const next=location.pathname+(params.size?'?'+params.toString():'')+location.hash;
    try {history.replaceState(null,'',next);} catch { /* file previews may not permit History API updates */ }
  };
  return {root,forts,url,escape,normalize,readSaved,query,formValues,initializeFilters,syncQuery};
})();
document.querySelectorAll('[data-save]').forEach(button=>{
  const refresh=()=>{const saved=SW.readSaved().includes(button.dataset.save);button.setAttribute('aria-pressed',String(saved));button.textContent=saved?'♥ Saved fort':'♡ Save fort';};
  refresh();
  button.addEventListener('click',()=>{
    const saved=new Set(SW.readSaved());const id=button.dataset.save;saved.has(id)?saved.delete(id):saved.add(id);
    try {localStorage.setItem('swarajya-saved',JSON.stringify([...saved]));refresh();}
    catch {button.textContent='Saving unavailable in this browser';}
  });
});
document.querySelector('.share-button')?.addEventListener('click',async()=>{
  const status=document.querySelector('#share-status');
  try {await navigator.clipboard.writeText(location.href);status.textContent='Fort link copied.';}
  catch {status.textContent='Copy this address: '+location.href;}
});
const lightbox=document.querySelector('#lightbox');
let lightboxTrigger=null;
const photos=[...document.querySelectorAll('.gallery-open')];let photoIndex=0;
function showPhoto(index){photoIndex=(index+photos.length)%photos.length;const button=photos[photoIndex];const img=lightbox.querySelector('img');img.classList.remove('zoomed');img.src=button.dataset.image;img.alt=button.dataset.caption;lightbox.querySelector('p').textContent=`${photoIndex+1} / ${photos.length} · ${button.dataset.caption}`;}
photos.forEach((button,index)=>button.addEventListener('click',()=>{lightboxTrigger=button;showPhoto(index);lightbox.showModal();}));
lightbox?.querySelector('.lightbox-close').addEventListener('click',()=>lightbox.close());
lightbox?.querySelector('.photo-prev').addEventListener('click',()=>showPhoto(photoIndex-1));
lightbox?.querySelector('.photo-next').addEventListener('click',()=>showPhoto(photoIndex+1));
lightbox?.querySelector('.photo-zoom').addEventListener('click',()=>lightbox.querySelector('img').classList.toggle('zoomed'));
lightbox?.querySelector('.photo-fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await lightbox.requestFullscreen();}catch{lightbox.querySelector('p').textContent+=' · Fullscreen is unavailable in this browser.';}});
lightbox?.addEventListener('click',event=>{if(event.target===lightbox)lightbox.close();});
lightbox?.addEventListener('close',()=>{lightboxTrigger?.focus();if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});});
lightbox?.addEventListener('keydown',event=>{if(event.key==='ArrowRight'){event.preventDefault();showPhoto(photoIndex+1);}if(event.key==='ArrowLeft'){event.preventDefault();showPhoto(photoIndex-1);}});
let touchStart=null;lightbox?.addEventListener('touchstart',e=>{touchStart=e.changedTouches[0].clientX;},{passive:true});lightbox?.addEventListener('touchend',e=>{if(touchStart!==null&&Math.abs(e.changedTouches[0].clientX-touchStart)>55)showPhoto(photoIndex+(e.changedTouches[0].clientX<touchStart?1:-1));touchStart=null;},{passive:true});
// A local, labelled illustration replaces an unavailable image, never an unrelated fort photograph.
document.querySelectorAll('img:not(.hero-art)').forEach(img=>img.addEventListener('error',()=>{
  if(img.dataset.fallback)return;img.dataset.fallback='true';img.removeAttribute('srcset');img.src=SW.url('assets/images/illustrations/sahyadri-600.webp');img.alt='Generic Sahyadri illustration; original photograph unavailable';
  const label=img.closest('.card-image,.fort-hero-photo')?.querySelector('.photo-label');if(label)label.textContent='Illustration · photo unavailable';
},{once:true}));
