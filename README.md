# Swarajya Explorer

A static Maharashtra fort and Maratha heritage website created by Pranav Vinod Chame, inspired by Tanshiq and Karan.

- 234 photographed fort profiles across 27 districts
- 1,487 credited photographs and 61 history chapters
- 179 source-referenced map locations
- Maharashtra Tourism PDF, 14 attributed fort supplements and a 20-fort brochure directory
- Responsive navigation, interactive galleries, motion controls and a desktop Mavala companion
- Unique metadata for 270 indexable pages

## Run locally

From this repository folder, run `python -m http.server 8000`, then open http://localhost:8000/.

## Build and deploy

Run `python scripts/build_site.py`. Python standard library only; no npm dependencies required. Set `SITE_URL` to your actual preferred HTTPS production address. The build creates canonical URLs and a 271-entry sitemap when a production URL is configured.

Cloudflare Pages: framework None, build command `python scripts/build_site.py`, output directory `.`. Connect this repository to Pages and set `SITE_URL`.

GitHub Pages: choose GitHub Actions under repository Settings > Pages. The optional template `docs/workflow-templates/pages.yml.example` can be installed as `.github/workflows/pages.yml` by an account authorized to manage workflows. Keep this disabled when Cloudflare is the primary host to avoid duplicate public deployments. It automatically detects the GitHub Pages URL if no preferred address is configured.

Read [deployment and SEO settings](DEPLOYMENT-SEO.md) and the [complete publishing guide](docs/PUBLISHING-GUIDE.md).

## Project structure

| Path | Contents |
| --- | --- |
| `assets/` | Photographs, source PDF, icons and bundled map SDK |
| `data/` | Fort facts, galleries, history and brochure source data |
| `scripts/` | Standard-library page generator, SEO and validation |
| `css/`, `js/` | Website design and interactions |
| `forts/`, `districts/` | Generated public guides |
| `reports/` | Current validation and SEO inventory |
| `docs/` | Owner publishing guide |

Edit the source data and scripts, then rebuild. Changes to generated HTML alone will be overwritten by the next build.

## Sources and coverage

Preserve the credits in [LICENSES.md](LICENSES.md) and the photo manifests. The Maharashtra Tourism PDF is included unchanged; its publisher retains rights. No blanket open-source licence is asserted for third-party material. Exact historical dates, trek conditions and brochure distances should be read with the source qualifications shown on each page.

127 forts have at least eight photos; 107 have fewer. Unphotographed research records are excluded from this public repository. See [QUALITY_REPORT.md](QUALITY_REPORT.md) for the current scope and limitations. Search metadata does not guarantee Google rankings.

## Repository and publishing status

Source repository: https://github.com/pranavchame/Swarajay-Explorer

Production website: pending Cloudflare deployment. Cloudflare runs website build validation on every deployment once connected. Optional GitHub Actions templates are preserved under `docs/workflow-templates/`; they are not active workflows.

## Roadmap

Expand credited galleries for forts with fewer photographs, review historical sources, and monitor accessibility, performance and search coverage after launch.
