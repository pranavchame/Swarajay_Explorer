'use strict';
(() => {
  const directory=document.querySelector('[data-directory]');if(!directory)return;
  const form=document.querySelector('#filters');
  const fixed=directory.dataset.fixedDistrict;
  const results=document.querySelector('#results');
  const cards=new Map([...results.children].map(card=>[card.dataset.fort,card]));
  const count=document.querySelector('#results-count');
  const empty=document.querySelector('#no-results');
  const more=document.querySelector('#load-more');
  let limit=18;let matched=[];
  SW.initializeFilters(form,fixed);
  function paint(){
    const visible=new Set(matched.slice(0,limit).map(f=>f.slug));
    for(const [id,card] of cards)card.hidden=!visible.has(id);
    const fragment=document.createDocumentFragment();
    for(const fort of matched)if(cards.has(fort.slug))fragment.append(cards.get(fort.slug));
    results.append(fragment);
    count.textContent=`${matched.length} ${matched.length===1?'fort':'forts'} found${matched.length>limit?` · showing ${limit}`:''}`;
    empty.hidden=matched.length!==0;more.hidden=matched.length<=limit;
    more.textContent=`Show more forts (${Math.max(0,matched.length-limit)} remaining)`;
  }
  function filter(sync=true){const values=SW.formValues(form);if(fixed)values.district=fixed;matched=SW.query(values);limit=18;paint();if(sync)SW.syncQuery(values);const mapLink=directory.querySelector('.results-bar a');const mapUrl=new URL(SW.url('maps.html'));for(const key of ['q','district','region','type','difficulty'])if(values[key])mapUrl.searchParams.set(key,values[key]);if(values.saved)mapUrl.searchParams.set('saved','1');mapLink.href=mapUrl.href;}
  form.addEventListener('submit',event=>{event.preventDefault();filter();});
  form.addEventListener('input',()=>filter());
  form.addEventListener('change',()=>filter());
  form.addEventListener('reset',()=>setTimeout(()=>{if(fixed)form.elements.district.value=fixed;filter();},0));
  document.querySelector('#empty-clear').addEventListener('click',()=>form.reset());
  more.addEventListener('click',()=>{limit+=18;paint();});
  window.addEventListener('popstate',()=>{SW.initializeFilters(form,fixed);filter(false);});
  filter(false);
})();
