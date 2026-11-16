# Swarajya Explorer — complete publishing and maintenance guide

Use the latest V8 release. This guide assumes GitHub stores your code and Cloudflare Pages serves your main website. GitHub Pages is an optional second host. You do not need to buy a domain to start.

## 1. Find the correct files

The editable project is the local repository folder containing index.html.

Portable download: Swarajya-Explorers-V8.zip, in the outputs folder alongside this guide. Right-click the ZIP > Extract All. Open the extracted Swarajya-Explorers folder. The ZIP is about 391 MB; allow it to finish extracting.

Your website root is the folder containing index.html. Copy everything INSIDE that folder into the GitHub repository root. Do not put the ZIP in the repository. Do not create an extra Swarajya-Explorers folder inside the repository root.

Expected repository structure:

```text
swarajya-explorer/
  index.html
  forts.html
  maps.html
  tourism-brochure.html
  site-config.json
  sitemap.xml
  robots.txt
  .nojekyll
  _redirects
  .github/
    workflows/pages.yml
  assets/
    documents/MH-Leaflet-Forts-Slides.pdf
    images/...
    vendor/...
  css/...
  js/...
  data/...
  forts/...
  districts/...
  scripts/...
  reports/...
```

Windows Explorer: View > Show > Hidden items if you cannot see .github. Keep .github and .nojekyll. Keep the original PDF under assets/documents; do not upload it separately to every fort folder. All 14 brochure supplements already link to that one file.

## 2. Put the project on GitHub with GitHub Desktop

Because the project contains thousands of files, use GitHub Desktop for the upload.

1. Create/sign into your account at https://github.com/.
2. Install GitHub Desktop from https://desktop.github.com/ and sign in.
3. In GitHub Desktop, choose File > New repository.
4. Name: swarajya-explorer (or your preferred unused repository name).
5. Description: Maharashtra fort histories, authentic photographs and travel guides.
6. Local path: choose a parent folder such as Documents\GitHub. Desktop creates the repository folder under it.
7. Git ignore: None. Licence: None unless you have chosen appropriate licensing for your own code. Third-party photographs and the brochure keep their own rights. Leave README initialization unchecked because the project already includes one.
8. Click Create repository.
9. Choose Repository > Show in Explorer. This opens the new local repository folder.
10. Open the project folder from step 1 in a second Explorer window. Select all project CONTENTS with Ctrl+A and copy with Ctrl+C. Paste them into the new repository folder with Ctrl+V.
11. Verify index.html is directly inside the new repository folder, alongside .github, assets, data and scripts.
12. Return to GitHub Desktop. Wait until the changed files appear.
13. In the Summary box, type: Add Swarajya Explorer V8 website.
14. Click Commit to main (or the branch shown).
15. Click Publish repository. Keep the name you chose. For a public heritage website and straightforward GitHub Pages setup, clear Keep this code private. Publish repository.
16. Wait for the upload to finish. Open Repository > View on GitHub.
17. The repository Code tab must show index.html, assets, scripts and .github at its top level.

If using an existing repository instead, clone it with GitHub Desktop, keep a backup of existing work, copy this project's contents into the clone, review changes, commit and Push origin. Do not delete an existing repository or overwrite unrelated work.

A GitHub Actions run may fail before GitHub Pages is enabled. That is separate from Cloudflare hosting. Enable GitHub Pages in step 6 if you want that second deployment.

Official Desktop guide: https://docs.github.com/en/desktop/overview/creating-your-first-repository-using-github-desktop

## 3. Publish on Cloudflare Pages

1. Create/sign into your account at https://dash.cloudflare.com/.
2. Open Workers & Pages.
3. Choose Create application, then the Pages option. If offered Workers deployment, switch to Pages.
4. Choose Connect to Git / Import an existing Git repository.
5. Choose GitHub and authorize Cloudflare to access the swarajya-explorer repository. Select that repository and continue.
6. Choose the project name. Its production address will be shown by Cloudflare, typically https://PROJECT-NAME.pages.dev/. Copy the actual address rather than guessing it.
7. Enter these build settings:

| Setting | Enter |
| --- | --- |
| Production branch | main, or the branch that contains your project |
| Framework preset | None |
| Build command | python scripts/build_site.py |
| Build output directory | . |
| Root directory | Leave default/blank when index.html is at repository root |

The output directory is one dot, not dist or public. This is a static Python-generated site, not a Node/React app.

8. Add environment variable SITE_URL. Value: your actual preferred HTTPS production address, such as the pages.dev address shown for this project. Include the full https:// address. Add it to Production and Preview if you want both to use the main site's canonical URLs.
9. Choose Save and Deploy. Wait for a successful deployment.
10. Open Visit site / the production address shown by Cloudflare.
11. If you could not set SITE_URL initially, deploy once, copy the production address, then go to the Pages project Settings > Variables and Secrets (or Environment variables), add SITE_URL and trigger a new production deployment.

No npm install or local Python installation is required for this Git-connected publishing workflow. The build runs on Cloudflare. No custom domain is required.

Official Pages guide: https://developers.cloudflare.com/pages/get-started/git-integration/
Build settings: https://developers.cloudflare.com/pages/configuration/build-configuration/

## 4. Set your main URL correctly

Choose one main address for Google. If Cloudflare Pages is your main website, use its address in SITE_URL on both hosting services. If you later buy a custom domain, connect it in the Cloudflare Pages project's Custom domains section, complete its DNS instructions, then change SITE_URL to the new HTTPS domain and redeploy.

The project supports these URL settings, in precedence order:

1. Explicit --base-url when running generate_pages.py manually.
2. SITE_URL environment variable.
3. public_url in site-config.json.
4. CF_PAGES_URL from Cloudflare.
5. GITHUB_PAGES_URL from the GitHub workflow.

You can leave site-config.json unchanged when SITE_URL is set. Alternatively edit that file's public_url string, preserving valid JSON. Do not leave an example URL in a production setting.

The production build automatically writes the canonical tags, absolute share-image addresses, structured data, sitemap.xml and robots.txt. You do not manually create tags for 234 forts.

## 5. Verify the live website

On your actual production address, open:

- / — homepage.
- /forts.html — fort directory; try a search/filter.
- /forts/rajgad/index.html — Rajgad profile.
- /forts/rajgad/index.html#tourism-guide — brochure supplement.
- /tourism-brochure.html — all 20 brochure forts; test Download PDF.
- /assets/documents/MH-Leaflet-Forts-Slides.pdf — original PDF.
- /maps.html — choose Load interactive map.
- /sitemap.xml — XML containing your real production URL; 271 entries in V8.
- /robots.txt — should include Sitemap: followed by your real URL and /sitemap.xml.

Right-click a fort page > View page source. Ctrl+F for description, keywords, canonical and application/ld+json. Confirm the canonical address uses your preferred domain. Test your phone's menu and a gallery too.

Map basemaps use the owner-supplied MapTiler browser key in js/config.js. In your MapTiler account, configure permitted website origins for the hosts you use. If maps fail only after publishing, check those origins and the account's service usage. Keep the map attribution.

If hosting under GitHub's repository subpath, append these page paths after that repository path rather than after github.io alone.

## 6. Optional: also enable GitHub Pages

GitHub stores the code even if you skip this section. Cloudflare can publish directly from that code.

1. Open your repository on GitHub > Settings > Pages.
2. Under Build and deployment, choose GitHub Actions as Source.
3. The included workflow is .github/workflows/pages.yml.
4. If Cloudflare is the main site, open Settings > Secrets and variables > Actions > Variables > New repository variable.
5. Name: SITE_URL. Value: the same main production address you set on Cloudflare. Save.
6. Open Actions > Publish Swarajya Explorer to GitHub Pages > Run workflow. Select main and run it. If the UI instead offers Re-run jobs for a failed initial run, rerun after Pages is configured.
7. Wait for success. Open the page_url shown by the deployment or the Visit site link in Settings > Pages.
8. A project repository commonly uses https://YOUR-GITHUB-USERNAME.github.io/REPOSITORY-NAME/. Copy the actual address GitHub shows.

When GitHub Pages is your only host, leave SITE_URL unset and public_url empty; the workflow obtains the correct URL automatically, including the repository path.

Official workflow instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## 7. Add the website to Google Search Console

1. First finish the live-site and sitemap checks above.
2. Open https://search.google.com/search-console/ and sign into your Google account.
3. Add a property. For a free pages.dev or github.io website, select URL prefix and paste the complete main site address, including a repository path if applicable.
4. Click Continue. Choose the HTML file verification method if offered.
5. Download Google's verification HTML file, usually named google followed by a unique code and .html.
6. Copy that file unchanged into your LOCAL GitHub repository root, beside index.html. Do not rename it or put it in assets.
7. GitHub Desktop: commit the verification file and Push origin.
8. Wait for the main host's deployment to succeed. Open the exact verification-file URL Google asks you to check. It must show Google's verification text.
9. Return to Search Console and click Verify. Keep that verification file in the repository for future deployments.
10. Open Sitemaps. Enter sitemap.xml, or the complete sitemap URL requested by the interface, and click Submit.
11. Check its status. If it reports an error, inspect the details and confirm the public XML uses the same main address.
12. Use URL inspection for the homepage and a representative fort URL. Test live URL; if eligible, Request indexing.
13. Revisit the Pages and Performance reports later. Indexing is not immediate and is not guaranteed for every page. A sitemap submission does not guarantee search positions.

If HTML file verification is unavailable, use one of the methods Google offers. A custom domain's Domain-property verification uses DNS; follow Google's supplied record rather than inventing one. HTML tag verification would require preserving that token in the page generator, since editing generated HTML alone is overwritten by a rebuild.

Google verification guide: https://support.google.com/webmasters/answer/9008080?hl=en
Sitemap submission: https://support.google.com/webmasters/answer/7451001?hl=en

## 8. Where every important file is

All paths below are relative to your local repository root.

| File or folder | Purpose / what to edit |
| --- | --- |
| index.html | Generated homepage; do not use it as the main source for lasting edits |
| forts/<slug>/index.html | Generated individual fort pages |
| districts/<district>/index.html | Generated district guides |
| data/forts.json | Main fort facts, histories and source references |
| data/gallery-attribution.json | Per-fort photo lists and credits |
| data/heritage-events.json | History timeline chapters |
| data/tourism-brochure.json | Fourteen brochure supplements, page references and six named-only forts |
| assets/documents/MH-Leaflet-Forts-Slides.pdf | Original brochure; already included |
| assets/images/ | Published photos and thumbnails; preserve attribution |
| scripts/v8_content.py | Brochure-page layout, supplement layout, fort SEO title/description/keyword template |
| scripts/seo_publish.py | Canonicals, social metadata, JSON-LD, sitemap and metadata inventory |
| scripts/v7_design.py | Current header and About layout |
| scripts/v4_design.py | Existing homepage, fort and history layouts |
| scripts/generate_pages.py | Main HTML generator and page definitions |
| scripts/build_site.py | Deployment build: generate pages, validate data, check links |
| css/v7.css | Current visual overrides and brochure styles |
| js/navigation.js | Desktop sliding indicator and mobile menu |
| js/mascot.js | Desktop Mavala companion |
| js/config.js | MapTiler browser configuration |
| site-config.json | Optional preferred public URL |
| .github/workflows/pages.yml | GitHub Pages build and deployment |
| reports/seo-inventory.csv | Readable table of metadata for all 270 indexable pages |
| reports/seo-inventory.json | Same inventory as JSON |
| reports/seo-status.json | Whether production URL/canonicals were configured in the latest build |
| QUALITY_REPORT.md | Current verified coverage and limitations |

Editing the CSV does not update the website. For SEO template changes, edit scripts/v8_content.py. Metadata titles/descriptions are generated separately for each fort using its name and district. Google ignores meta keywords; useful content, sensible titles and descriptions are the priority.

The 21 unphotographed research records are intentionally outside the public project in Unpublished-fort-research.json. Do not publish them as complete profiles until genuine images are sourced.

## 9. Make future updates

1. Edit the appropriate SOURCE file locally. Preserve valid JSON syntax when changing data files: double quotes, commas between items, no trailing commas.
2. GitHub Desktop shows the changes. Review them.
3. Type a clear Summary, such as Update Rajgad brochure notes.
4. Commit to your production branch and Push origin.
5. Cloudflare automatically builds and publishes from that branch. The optional GitHub workflow also runs on main/master.
6. Open the deployment log. Only treat the update as live after success. Then check the changed page on the production URL.
7. If the browser shows an older version, try Ctrl+F5. Confirm you are using the production address rather than an old preview URL.

Changing a PDF or adding a new photograph requires keeping source attribution and updating the relevant source data. Do not simply rename a different fort's image. New public fort records must have real photographs; the generator checks this.

## 10. Common problems and fixes

| Problem | Check / fix |
| --- | --- |
| Cloudflare cannot find scripts/build_site.py | Project files are inside an extra folder. Put index.html and scripts at the repository root, or intentionally set the correct Root directory |
| Cloudflare homepage is 404 | Confirm build output directory is . and root-level index.html exists |
| Styles/images do not load | Confirm css, js and assets were all committed and uploaded |
| Sitemap has no URLs | Set SITE_URL to your real HTTPS address and redeploy |
| Sitemap/canonical uses the wrong host | Check SITE_URL first; it overrides site-config.json and automatic host URLs |
| Build reports a broken JSON file | Fix the syntax in the edited data file; inspect the build log for its filename |
| Fort generation rejects a record | Check for genuine photographs and a corresponding gallery entry |
| GitHub Actions permissions/Pages error | Enable Settings > Pages > GitHub Actions; confirm Actions are permitted, then rerun |
| Cloudflare cannot see the GitHub repository | Review the Cloudflare GitHub app's repository access |
| Verification file is 404 | Put it beside index.html, commit/push, wait for successful deployment, use Google's exact URL |
| Maps fail | Check browser key configuration, allowed origins and MapTiler usage |
| Google does not show the site immediately | Check Search Console verification, live URL inspection, sitemap fetch and indexing reports; allow crawling time |

Do not replace your real site files with this guide. This guide and the SEO CSV are reference documents. No live repository upload or production deployment was performed by the assistant.
