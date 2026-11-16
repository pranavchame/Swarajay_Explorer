"""Build for Cloudflare Pages or GitHub Pages; no third-party Python packages required."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
for script in ['generate_pages.py','validate_data.py','check_links.py']:
 subprocess.run([sys.executable,str(root/'scripts'/script)],check=True)
