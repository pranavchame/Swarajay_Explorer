'use strict';
(() => {
 const reduced = {get matches(){return !window.SWMotion.allowed();},addEventListener:(_,fn)=>document.addEventListener('sw:motionchange',fn)};
 let navigating = false;
 const reset = () => { navigating = false; document.documentElement.classList.remove('page-leaving'); };
 addEventListener('pageshow', reset);
 reduced.addEventListener('change', () => { if (reduced.matches) reset(); });
 document.addEventListener('click', event => {
  if (reduced.matches || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  const control = event.target.closest('a,button');
  if (!control || control.disabled) return;
  // A fixed, non-interactive ring never changes control layout or captures input.
  if (event.detail > 0) {
   const ring = document.createElement('span');
   ring.className = 'click-ring'; ring.setAttribute('aria-hidden', 'true');
   ring.style.left = event.clientX + 'px'; ring.style.top = event.clientY + 'px';
   (document.querySelector('dialog[open]') || document.body).append(ring);
   ring.addEventListener('animationend', () => ring.remove(), {once:true});
   setTimeout(() => ring.remove(), 650);
  }
  const anchor = control.closest('a[href]');
  if (!anchor || anchor.hasAttribute('download') || (anchor.target && anchor.target !== '_self')) return;
  let target;
  try { target = new URL(anchor.href); } catch { return; }
  if (target.origin !== location.origin || !['http:','https:'].includes(target.protocol)) return;
  // In-page navigation keeps the native focus, scrolling and browser history behavior.
  if (target.pathname === location.pathname && target.search === location.search) return;
  if (!target.pathname.endsWith('.html') && !target.pathname.endsWith('/')) return;
  if (navigating) { event.preventDefault(); return; }
  navigating = true;
  event.preventDefault();
  document.documentElement.classList.add('page-leaving');
  setTimeout(() => location.assign(target.href), 130);
  // Restore the page if a browser/extension prevents navigation.
  setTimeout(reset, 1600);
 });
})();
