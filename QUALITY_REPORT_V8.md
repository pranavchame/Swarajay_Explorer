# V8 quality report — 16 November 2026

The existing site now includes the owner-supplied Maharashtra Tourism leaflet unchanged (12 pages, 8,086,105 bytes). All 20 named forts link to existing public profiles. Fourteen receive attributed supplements covering heritage, landmarks, nearby places, activities and brochure travel distances. Six are named-only recommendations, without invented brochure descriptions. The brochure directory and footer/source links expose the PDF for download. Its checksum matches the supplied original.

The leaflet has inconsistent historical claims and distances. Supplements retain existing source-based facts, paraphrase the reliable overview material and label ambiguous claims. Distance tables reproduce brochure figures with an explicit unverified/current-route caveat. No new coordinates, trek grades or photographs were inferred from the PDF. The original preserves every detail, image and publisher contact.

## SEO and hosting

All 234 fort pages now have individual descriptive titles, descriptions, keywords, Open Graph/Twitter tags and landmark/WebPage structured data. The other 36 indexable pages also have metadata: 270 total, all with unique titles and descriptions. reports/seo-inventory.csv and .json expose the exact tags. Requested keyword tags are included; Google does not use them for rankings. No ranking guarantee is made.

A production-URL build adds absolute canonical/social URLs, breadcrumbs, WebSite data, robots.txt and a 271-URL sitemap including the PDF. A test HTTPS URL with a repository subpath passed validation and was removed from all delivered HTML, metadata inventory, robots and sitemap. No actual domain was supplied; the default sitemap remains empty until deployment supplies one. site-config.json public_url, SITE_URL, CF_PAGES_URL and GITHUB_PAGES_URL are supported. GitHub Actions workflow and Cloudflare build instructions are included. No live deployment or Search Console verification occurred.

## Verification

- Standard-library build completed; data validator passed for 234 photographed forts, 27 districts and 179 source-referenced coordinates.
- All 270 page titles and descriptions are unique, requested metadata fields present, 14 supplements present and all 20 brochure links checked.
- Local-link audit: 312 HTML files and 25,346 references, no errors.
- Browser: brochure directory at 390px, Rajgad guide at 1365px and 390px, no horizontal overflow; travel disclosure opened; PDF download succeeded; checked console had no warnings/errors.
- Original PDF hash matched, JSON-LD parsed, production canonical/sitemap paths tested, all source Python files compiled. File sizes checked against the Cloudflare Pages 25 MiB asset ceiling.
- ZIP integrity and release checksum recorded separately after packaging.

Existing catalogue coverage remains 234 forts, 1,487 photographs, 61 history chapters. 127 forts have eight or more photographs; 107 have fewer. The 21 unpublished records stay outside the public project. V7 visual, map and motion changes remain; their historical verification is in reports/browser-v7.json and QUALITY_REPORT_V7.md. Current browser work focused on this update.

For hosting and Google Search Console steps, see DEPLOYMENT-SEO.md. Domain configuration and production indexing must be completed after choosing the public URL. Further exact historical tenures, route conditions and photo coverage remain incomplete as documented in the previous report.
