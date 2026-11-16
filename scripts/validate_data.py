"""Validate catalogue integrity; this does not independently authenticate historical claims."""
from pathlib import Path
from collections import Counter
import json, math, re, sys
from urllib.parse import urlparse,parse_qs
ROOT=Path(__file__).resolve().parents[1]
forts=json.loads((ROOT/'data/forts.json').read_text(encoding='utf-8'))
required=['id','slug','name','aliases','district','region','type','latitude','longitude','coordinate_source','elevation','history','history_excerpt','significance','events','rulers','shivaji_connection','architecture','attractions','difficulty','duration','best_season','nearest_settlement','how_to_reach','safety','image','image_kind','references','directions_url']
errors=[]
def check(ok,message):
 if not ok:errors.append(message)
check(bool(forts),'No published forts')
gallery=json.loads((ROOT/'data/gallery-attribution.json').read_text(encoding='utf8'))
for key in ['id','slug','name']:
 duplicates=[k for k,v in Counter(f[key].casefold() for f in forts).items() if v>1]
 check(not duplicates,'Duplicate '+key+': '+str(duplicates))
coords=[];refs=[]
for f in forts:
 n=f['name'];check(bool(gallery.get(f['slug'])) and f['image_kind']=='photograph',n+': published fort lacks photography');check(all(k in f for k in required),n+': required schema fields missing')
 check(bool(re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',f['slug'])),n+': invalid slug')
 check(bool(f['history'] or f['history_excerpt']),n+': no historical text')
 check(bool(f['references']),n+': no references')
 for r in f['references']:check(r['url'].startswith('https://'),n+': invalid reference URL')
 refs.append(f['references'][0]['url'])
 check((ROOT/f['url']).is_file(),n+': missing generated page')
 check((ROOT/f['image']).is_file(),n+': missing image')
 check((ROOT/f['thumbnail']).is_file(),n+': missing thumbnail')
 if f['image_kind']=='photograph':
  check(bool(f['image_credit']),n+': missing image license')
  check(bool(f['image_credit']['source'] and f['image_credit']['license']),n+': incomplete image provenance')
 else:check(f['image_kind']=='illustration',n+': unknown media type')
 if f['latitude'] is not None:
  lat,lng=f['latitude'],f['longitude'];check(all(isinstance(v,(int,float)) and math.isfinite(v) for v in [lat,lng]),n+': coordinates not finite numbers')
  check(15.6<lat<22.1 and 72.5<lng<80.9,n+': outside regional coordinate bounds')
  check(f['coordinate_source'].startswith('https://'),n+': missing coordinate source')
  coords.append((lat,lng))
  q=parse_qs(urlparse(f['directions_url']).query);check(q.get('destination')==[str(lat)+','+str(lng)] and q.get('api')==['1'],n+': incorrect directions')
 else:check(f['longitude'] is None and f['directions_url'] is None,n+': unverified directions must not be published')
check(len(coords)==len(set(coords)),'Duplicate map coordinates')
check(len(refs)==len(set(refs)),'Duplicate source article: possible alias counted twice')
report={'status':'PASS' if not errors else 'FAIL','unique_forts':len(forts),'source_referenced_coordinates':len(coords),'independently_surveyed_coordinates':0,'districts':len({f['district'] for f in forts}),'photographs_in_use':sum(f['image_kind']=='photograph' for f in forts),'illustrations_unique':len({f['image'] for f in forts if f['image_kind']=='illustration'}),'overview_histories':sum(bool(f['history']) for f in forts),'source_note_histories':sum(not f['history'] for f in forts),'documented_trek_grades':sum(bool(f['difficulty']) for f in forts),'documented_durations':sum(bool(f['duration']) for f in forts),'documented_seasons':sum(bool(f['best_season']) for f in forts),'errors':errors,'scope':'Schema, uniqueness, source provenance, paths, broad coordinate bounds and directions. This is not an independent historical or geospatial verification.'}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/data-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2));sys.exit(bool(errors))
