# Publish and search setup

Upload the contents of Swarajya-Explorers to the root of your GitHub repository. The source PDF is included at assets/documents/MH-Leaflet-Forts-Slides.pdf and linked from tourism-brochure.html, sources.html and 14 fort guides. Keep its publisher attribution. The PDF is supplied unchanged; its publisher retains copyright.

## One main URL

If publishing on both services, choose one preferred public address. Set public_url in site-config.json to that HTTPS address, or set the SITE_URL deployment variable. SITE_URL takes precedence. The other host will then use canonical links to that preferred address. No domain was supplied in chat, so this delivery intentionally has no invented production address.

## GitHub Pages

1. Push the included project files to a main or master branch.
2. In repository Settings > Pages, choose GitHub Actions as the source.
3. The included .github/workflows/pages.yml generates HTML, checks data/links, creates the sitemap and deploys. It obtains the Pages base URL from actions/configure-pages, including a repository subpath.
4. If you prefer Cloudflare as the canonical host, set repository variable SITE_URL to that public address before running the workflow.

## Cloudflare Pages

Connect the repository. Framework preset: None. Build command: `python scripts/build_site.py`. Build output directory: `.` (repository root). No npm install is needed. Set environment variable SITE_URL to your preferred production HTTPS address, especially for custom domains. When not set, CF_PAGES_URL supplies the build URL; preview deployments may therefore self-canonicalize unless SITE_URL is configured.

For Direct Upload, first run `python scripts/generate_pages.py --base-url https://YOUR-REAL-ADDRESS/` locally and upload the generated site folder. Never publish the placeholder address. The original PDF is about 7.7 MiB, below Cloudflare Pages' 25 MiB per-file limit.

## Search metadata

All 234 public forts have individual titles, meta descriptions, requested keyword tags, Open Graph/Twitter metadata and landmark/WebPage JSON-LD. All other indexable pages have metadata too. Production builds add absolute canonical URLs, absolute social images, breadcrumbs and a valid absolute sitemap. Redirects and 404 remain noindex. Source figure ambiguities are visible on brochure fort guides.

Review reports/seo-inventory.csv or .json for the complete page-by-page metadata. Google does not use meta keywords for ranking; they are included because requested. Page quality and useful sourced content matter. Metadata does not guarantee a position or indexing.

After deployment, verify the chosen domain in Google Search Console, submit its sitemap.xml and inspect representative fort URLs. This requires your own account and live domain; no verification token was invented. Hosting configuration is supplied and build-tested locally; no deployment was performed in this task.

References: https://developers.google.com/search/docs/appearance/snippet ; https://developers.google.com/search/docs/crawling-indexing/special-tags ; https://developers.google.com/search/docs/appearance/title-link
