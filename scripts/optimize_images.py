"""Create responsive WebP siblings for a new image; requires Pillow."""
from pathlib import Path
import argparse
from PIL import Image,ImageOps
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('destination',type=Path);args=p.parse_args()
if args.destination.exists():raise SystemExit('Choose a new destination; this tool does not overwrite existing photographs.')
args.destination.parent.mkdir(parents=True,exist_ok=True)
im=ImageOps.exif_transpose(Image.open(args.source)).convert('RGB');im.thumbnail((1440,1080));im.save(args.destination,'WEBP',quality=79,method=6)
im.thumbnail((600,450));im.save(args.destination.with_name(args.destination.stem+'-600.webp'),'WEBP',quality=76,method=6)
print('Created',args.destination,'and its 600-pixel thumbnail. Add source, artist and license to data/image-attribution.json before rebuilding.')
