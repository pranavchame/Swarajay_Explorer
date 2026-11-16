"""Check local HTML links, fragments, source assets, image sets and CSS resources."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
class Document(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0;self.title=False;self.viewport=False;self.noindex=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='viewport':self.viewport=True
  if tag=='meta' and a.get('name')=='robots' and 'noindex' in a.get('content',''):self.noindex=True
  for key in ['href','src','data-image']:
   if a.get(key):self.links.append(a[key])
  if a.get('srcset'):self.links.extend(v.strip().split()[0] for v in a['srcset'].split(','))
docs={};errors=[];count=0;directory_names={}
for p in ROOT.rglob('*.html'):
 content=p.read_text(encoding='utf-8')
 # Google's exact ownership token is not a visitor-facing HTML page.
 if p.parent==ROOT and re.fullmatch(r'google[0-9a-f]+\.html',p.name) and content.strip()=='google-site-verification: '+p.name:continue
 d=Document();d.feed(content);docs[p.resolve()]=d
 if not d.noindex and d.h1!=1:errors.append(f'{p.relative_to(ROOT)}: expected one h1, got {d.h1}')
 if not d.title or not d.viewport:errors.append(f'{p.relative_to(ROOT)}: missing title or viewport')
def validate(source,link):
 global count
 parsed=urlparse(link)
 if parsed.scheme or parsed.netloc or link.startswith('//'):return
 count+=1;target=(source.parent/unquote(parsed.path)).resolve() if parsed.path else source.resolve()
 if target.is_dir():target=target/'index.html'
 if not target.is_file():errors.append(f'{source.relative_to(ROOT)} -> missing {link}');return
 if not target.is_relative_to(ROOT):errors.append(f'{source.relative_to(ROOT)} -> escaped site root: {link}')
 if parsed.fragment and target in docs and unquote(parsed.fragment) not in docs[target].ids:errors.append(f'{source.relative_to(ROOT)} -> missing fragment {link}')
 # Ensure case matches the actual filename for case-sensitive hosts.
 if target.parent not in directory_names:directory_names[target.parent]={p.name for p in target.parent.iterdir()}
 if parsed.path and target.name not in directory_names[target.parent]:errors.append(f'{source.relative_to(ROOT)} -> wrong path case {link}')
for p,d in docs.items():
 for link in d.links:validate(p,link)
for p in ROOT.rglob('*.css'):
 for link in re.findall(r'url\([\'\"]?([^\)\'\"]+)',p.read_text(encoding='utf-8')):
  if not link.startswith('data:'):validate(p,link)
report={'status':'PASS' if not errors else 'FAIL','html_pages':len(docs),'local_references_checked':count,'errors':errors,'scope':'All local HTML links, fragments, src/srcset assets, CSS url resources, page titles, h1 counts and viewport metadata. External websites are not continuously availability-tested.'}
(ROOT/'reports').mkdir(exist_ok=True);(ROOT/'reports/link-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2));sys.exit(bool(errors))
