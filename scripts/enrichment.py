from html import escape as e
import re
def stars(f):
 n=f.get('difficulty_rating')
 return f'<span class="difficulty level-{n or 0}"><span aria-hidden="true">'+('★'*n+'☆'*(5-n) if n else '—')+'</span> '+e(f.get('difficulty') or 'Difficulty Not Yet Verified')+'</span>'
def recommend(f):return '<span class="recommendation">'+e(f['recommendation'])+'</span>'
def event_html(ev,pre=''):
 return '<article class="timeline-event" id="'+e(ev['id'])+'"><p class="eyebrow">'+e(ev['date'])+'</p><h3>'+e(ev['title'])+'</h3><p>'+e(ev['significance'])+'</p><details><summary>Read more · full event account</summary><ol class="event-summary">'+''.join('<li>'+e(s)+'</li>' for s in ev['summary'])+'</ol>'+''.join('<p>'+e(p)+'</p>' for p in ev['full'])+'<p class="small">Sources: '+', '.join('<a href="'+e(r['url'])+'">'+e(r['title'])+'</a>' for r in ev['references'])+'</p></details></article>'
def detail(f,body,gallery,events):
 rating='<section id="assessment" class="detail-section"><p class="eyebrow">PLAN A VISIT THAT SUITS YOU</p><h2>Difficulty & visit recommendation</h2><div class="assessment">'+stars(f)+recommend(f)+'</div><h3>Why visit?</h3><p>'+e(f['recommendation_reason'])+'</p><h3>Why this difficulty?</h3><ul>'+''.join('<li>'+e(x)+'</li>' for x in f['difficulty_reasons'])+'</ul><p class="small">Route assessed: '+e(f['route_assessed'])+'. '+e(f['difficulty_confidence'])+'. Source review: '+e(f['reviewed'])+'. Stars describe effort and obstacles; the visit badge is a separate editorial assessment. No community review average is displayed.</p></section>'
 city=e(f.get('nearest_city') or 'Not yet verified')+(f' · {f["city_distance_km"]} km straight line' if f.get('city_distance_km') is not None else '')
 essentials='<div class="essential-info"><p><b>Base / nearby village:</b> '+e(f.get('nearest_settlement') or 'Not yet verified')+'</p><p><b>Nearby major city:</b> '+city+'</p><p class="small">'+e(f['city_method'])+'</p>'+stars(f)+' '+recommend(f)+'</div>'
 body=body.replace('<div class="fort-actions">',essentials+'<div class="fort-actions">')
 body=body.replace('</h1><p class="lead">','</h1>'+('<p class="marathi-name" lang="mr">'+e(f['marathi_name'])+'</p>' if f.get('marathi_name') else '')+'<p class="lead">',1)
 jump='<nav class="detail-jump" aria-label="On this fort page"><a href="#assessment">Visit guide</a><a href="#fort-history">History</a><a href="#fort-gallery">Photos</a><a href="#fort-layout">Layout</a><a href="#references">Sources</a></nav>'
 body=body.replace('<div class="wrap detail-layout">','<div class="wrap">'+jump+'</div><div class="wrap detail-layout">')
 body=body.replace('<article><section class="detail-section">','<article>'+rating+'<section id="fort-history" class="detail-section">',1)
 important='<section class="detail-section"><h2>Historical importance</h2><p>'+e(f['significance'])+'</p><h3>Rulers & periods</h3>'
 if f.get('ruler_periods'):important+='<ul>'+''.join('<li>'+e(str(x))+'</li>' for x in f['ruler_periods'])+'</ul>'
 else:important+='<p>'+e(', '.join(f['rulers']) or 'Individual ruling powers are not established in this entry.')+'</p><p class="small">Exact possession periods and durations have not been verified. A sovereign’s reign does not establish uninterrupted control of this fort.</p>'
 important+='</section>'
 related=[ev for ev in events if f['slug'] in ev['fort_slugs']]
 if related:important+='<section class="detail-section"><h2>Events that shaped Swarajya</h2>'+''.join(event_html(ev,'../../') for ev in related)+'</section>'
 body=body.replace('<section class="detail-section"><p class="eyebrow">READING THE LANDSCAPE',important+'<section class="detail-section"><p class="eyebrow">READING THE LANDSCAPE')
 photos=gallery.get(f['slug'],[])
 galleryhtml='<section id="fort-gallery" class="detail-section"><p class="eyebrow">DOCUMENTARY PHOTOGRAPHY</p><h2>'+str(len(photos))+' photographs of '+e(f['name'])+'</h2><p class="small">Open a photograph for swipe, zoom and fullscreen controls. Each image links to its author and reuse licence.</p><div class="photo-grid">'
 for i,p in enumerate(photos):
  caption=f['name']+' · '+p['title'].removeprefix('File:')+' · '+p['artist']+' · '+p['license']
  galleryhtml+='<figure><button class="gallery-open" data-image="../../'+e(p['file'])+'" data-caption="'+e(caption)+'" aria-label="Open photograph '+str(i+1)+'"><img loading="lazy" decoding="async" src="../../'+e(p['thumbnail'])+'" width="600" height="450" alt="'+e(p.get('description') or p['title'])+'"></button><figcaption>'+e(p['artist'])+' · <a href="'+e(p['source'])+'">Source</a> · <a href="'+e(p.get('license_url') or p['source'])+'">'+e(p['license'])+'</a></figcaption></figure>'
 if not photos:galleryhtml+='<p>Verified licensed photographs are not yet available for this entry.</p>'
 galleryhtml+='</div></section>'
 body=re.sub(r'<section class="detail-section"><h2>(?:A closer look|About this illustration)</h2>.*?</section>',lambda _:galleryhtml,body,flags=re.S)
 # A selectable feature inventory avoids inventing the precise locations of structures.
 layout='<section id="fort-layout" class="detail-section"><h2>Explore fort features</h2><p>This is a feature guide, not a surveyed top-down layout. Precise structural locations are not yet verified.</p><div class="layout-features">'+''.join('<details><summary>'+e(a)+'</summary><p>'+e(a)+' is mentioned in the linked source account for '+e(f['name'])+'. Confirm its condition and access locally.</p></details>' for a in f['architecture'])+'</div></section>'
 body=body.replace('<section id="references"',layout+'<section id="references"')
 return body
