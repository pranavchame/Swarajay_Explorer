"""Generate share metadata, structured data, SEO inventory and production sitemap."""
import csv,json,os,re
from html import escape,unescape
from urllib.parse import urljoin,urlsplit

def publish(root,paths,forts,explicit=None):
 config=json.loads((root/'site-config.json').read_text(encoding='utf8'))
 base=explicit or os.getenv('SITE_URL') or config.get('public_url') or os.getenv('CF_PAGES_URL') or os.getenv('GITHUB_PAGES_URL')
 if base:
  u=urlsplit(base)
  if u.scheme!='https' or not u.netloc or u.query or u.fragment or u.username:raise SystemExit('Provide an HTTPS site URL without query, fragment or credentials.')
  base=base.rstrip('/')+'/'
 rows=[];by={f['url']:f for f in forts}
 for path in paths:
  file=root/path;doc=file.read_text(encoding='utf8')
  def meta(name):
   m=re.search(r'<meta (?:name|property)="'+re.escape(name)+r'" content="([^"]*)"',doc);return unescape(m[1]) if m else ''
  title=unescape(re.search(r'<title>(.*?)</title>',doc)[1]);desc=meta('description');keywords=meta('keywords')
  graph=[{'@type':'WebPage','name':title,'description':desc,'inLanguage':'en-IN'}]
  f=by.get(path)
  if f:
   landmark={'@type':'LandmarksOrHistoricalBuildings','name':f['name'],'alternateName':f.get('marathi_name') or f['name'],'description':desc,'address':{'@type':'PostalAddress','addressLocality':f['district'],'addressRegion':'Maharashtra','addressCountry':'IN'}}
   if f.get('latitude') is not None:landmark['geo']={'@type':'GeoCoordinates','latitude':f['latitude'],'longitude':f['longitude']}
   graph.append(landmark)
  if base:
   url=urljoin(base,path);image=meta('og:image');absolute_image=urljoin(url,image)
   graph[0].update({'@id':url+'#webpage','url':url,'isPartOf':{'@id':base+'#website'},'primaryImageOfPage':{'@type':'ImageObject','url':absolute_image}})
   graph.append({'@type':'WebSite','@id':base+'#website','url':base,'name':'Swarajya Explorer','inLanguage':'en-IN'})
   crumbs=[('Home','index.html')]
   if f:crumbs+=[('Explore forts','forts.html'),(f['name'],path)];graph[0]['mainEntity']={'@id':url+'#fort'};graph[1].update({'@id':url+'#fort','url':url,'image':absolute_image})
   elif path!='index.html':crumbs.append((title.split(' | ')[0],path))
   graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':urljoin(base,p)} for i,(name,p) in enumerate(crumbs)]})
   doc=doc.replace('</head>','<link rel="canonical" href="'+escape(url,quote=True)+'"><meta property="og:url" content="'+escape(url,quote=True)+'"></head>')
   for name in ['og:image','twitter:image']:
    doc=re.sub(r'(<meta (?:name|property)="'+name+r'" content=")[^"]*',lambda m:m[1]+escape(absolute_image,quote=True),doc)
  else:url=''
  # Replace the earlier landmark block with a single coherent JSON-LD graph.
  doc=re.sub(r'<script type="application/ld\+json">.*?</script>','',doc,flags=re.S)
  doc=doc.replace('</head>','<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')+'</script></head>')
  file.write_text(doc,encoding='utf8');rows.append({'path':path,'title':title,'description':desc,'keywords':keywords,'canonical_url':url})
 (root/'404.html').write_text((root/'404.html').read_text(encoding='utf8').replace('index,follow,max-image-preview:large','noindex,follow'),encoding='utf8')
 (root/'reports/seo-inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
 with (root/'reports/seo-inventory.csv').open('w',encoding='utf-8-sig',newline='') as out:
  writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 locs=paths+['assets/documents/MH-Leaflet-Forts-Slides.pdf']
 (root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+(''.join('<url><loc>'+escape(urljoin(base,p))+'</loc></url>' for p in locs) if base else '')+'</urlset>',encoding='utf8')
 (root/'robots.txt').write_text('User-agent: *\nAllow: /\n'+('Sitemap: '+base+'sitemap.xml\n' if base else '# Set SITE_URL or site-config.json public_url and rebuild to generate the production sitemap.\n'),encoding='utf8')
 (root/'reports/seo-status.json').write_text(json.dumps({'pages':len(rows),'fort_pages':len(forts),'production_url':base,'canonical_and_sitemap_ready':bool(base),'note':'Google ignores meta keywords. Titles, descriptions and useful visible content help describe pages; rankings are not guaranteed.'},indent=2),encoding='utf8')
