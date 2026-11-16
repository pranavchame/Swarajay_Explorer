"""Brochure content and per-page search metadata; standard-library only."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
BROCHURE=json.loads((ROOT/'data/tourism-brochure.json').read_text(encoding='utf8'))
ENTRIES={x['slug']:x for x in BROCHURE['entries']}
def e(s):return escape(str(s),quote=True)
def section(f,pre='../../'):
 x=ENTRIES.get(f['slug'])
 if not x:return ''
 pages=', '.join(map(str,x['pages']));pdf=pre+BROCHURE['file']+'#page='+str(x['pages'][0])
 out=f'<section id="tourism-guide" class="wrap section brochure-guide"><p class="eyebrow">MAHARASHTRA TOURISM · BROCHURE GUIDE</p><h2>{e(f["name"])}: heritage &amp; nearby places</h2><p class="lead">{e(x["summary"])}</p><div class="brochure-columns">'
 for label,key in [('Landmarks to look for','landmarks'),('Places in the wider area','nearby')]:
  if x[key]:out+='<div><h3>'+label+'</h3><ul>'+''.join('<li>'+e(a)+'</li>' for a in x[key])+'</ul></div>'
 out+='</div>'
 if x['activities']:out+='<p><strong>Brochure activity ideas:</strong> '+e(x['activities'])+'</p>'
 out+='<details><summary>Travel distances from the brochure <span aria-hidden="true">＋</span></summary><p>'+e(BROCHURE['distance_policy'])+'</p><dl class="travel-facts">'+''.join('<div><dt>By '+k+'</dt><dd>'+e(v)+'</dd></div>' for k,v in x['transport'].items())+'</dl></details>'
 if x['note']:out+='<p class="small brochure-note"><strong>Source clarification:</strong> '+e(x['note'])+'</p>'
 return out+f'<p class="small">Adapted from Maharashtra Tourism, <cite>{e(BROCHURE["title"])}</cite>, PDF pages {pages}. <a href="{e(pdf)}">Read the original PDF ↗</a> · <a href="{pre}tourism-brochure.html">Explore all brochure forts ↗</a></p></section>'
def brochure_page(forts):
 by={f['slug']:f for f in forts};out='<section class="page-intro wrap"><p class="eyebrow">MAHARASHTRA TOURISM · READING ROOM</p><h1>Guardians of <em>History.</em></h1><p class="lead">Explore the 20 forts featured in the Maharashtra Tourism leaflet, with 14 detailed guides and six further recommendations.</p><p><a class="button" href="'+BROCHURE['file']+'" download>Download the original PDF · 7.7 MB ↓</a></p></section><section class="wrap prose"><h2>About this source</h2><p>This 12-page leaflet is published by Maharashtra Tourism and supplied by the website owner. Its historical descriptions are paraphrased with attribution. Travel figures remain source quotations, not live route measurements. Some claims require clarification, noted on the relevant fort pages. Publication date is not shown. The original document retains its publisher’s rights and contact details.</p></section><section class="wrap section"><h2>Fourteen fort guides</h2><div class="district-grid">'
 for x in BROCHURE['entries']:
  f=by[x['slug']];out+='<a class="district-tile" href="'+f['url']+'#tourism-guide"><h3>'+e(f['name'])+'</h3><p>'+e(f['district'])+' · PDF '+', '.join(map(str,x['pages']))+' ↗</p></a>'
 out+='</div><h2>Six more forts named in the leaflet</h2><p>The leaflet names these forts on page 12 without individual historical or travel descriptions. Follow their existing guides for sourced information.</p><div class="district-grid">'
 for slug in BROCHURE['named_only']:
  f=by[slug];out+='<a class="district-tile" href="'+f['url']+'"><h3>'+e(f['name'])+'</h3><p>'+e(f['district'])+' ↗</p></a>'
 return out+'</div></section>'
def fort_meta(f):
 name=f['name'];label=name if 'fort' in name.lower() else name+' Fort'
 title=f'{label}, {f["district"]}: History & Visitor Guide'
 desc=f'Explore {label} in {f["district"]}, Maharashtra: history, authentic photos, landmarks, trek information and sourced visitor guidance.'
 keywords=[label,name+' history',name+' photos',f['district']+' forts','Maharashtra forts',f['type'],name+' visitor guide']
 if f.get('marathi_name'):keywords.append(f['marathi_name'])
 return title,desc,', '.join(dict.fromkeys(keywords))
def general_keywords(title):return ', '.join(dict.fromkeys([re.sub('<[^>]+>','',title),'Maharashtra forts','Swarajya Explorer','Maratha history']))
