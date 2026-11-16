# Original archive audit

All 29 top-level files in Hari harr.zip were inventoried. All HTML pages were parsed for titles, headings, links and images; Homepage.html, Maps.html, Style.css, script.js and fortE.html were read in detail. A contact sheet of every original JPG/PNG was visually inspected.

Findings repaired in the rebuilt project:

- Homepage.html did not load script.js, so Explore was disconnected. The old script also assumed search elements that were absent, causing null-reference risks if connected unchanged.
- Explore’s modal linked to nonexistent `#maps`, and search only displayed an alert. The new homepage search, directory and map actions use real records.
- Homepage contained stray checkbox/text markup unrelated to the page; removed.
- Maps.html used a fixed-pixel image map with missing `satar.html`, missing `thane.html`, wrong `kolhapur.html`, and leading spaces in Palghar/Nashik links. Replaced with real Leaflet mapping and consistent navigation.
- `fortE.html` contained “Pending”, duplicate body tags and no useful fort-location content. It now redirects to the complete directory.
- Several district pages were empty or displayed a single fort instead of a district list. All represented districts now have generated guides with counts and filters.
- `raigad1.html` described Raigad but used Rajgad.jpg / Rajgad1.jpg. It now redirects to the actual Raigad record and an appropriately sourced photograph.
- Ratnagiri’s Suvarnadurg image filenames did not exist. All generated image paths are checked automatically.
- Original photographs lacked clear license metadata; some were visibly watermarked. They were left in the preserved original project and not republished.
- Metadata, shared navigation, responsive styles, keyboard focus and source credits were inconsistent or missing. These are generated consistently now.

Legacy district spelling variants receive redirects where they can coexist on Windows. A case-only Maps.html alias cannot coexist with maps.html in a Windows extraction; the actual page and every new navigation link use lowercase maps.html.

No instructions found inside archive content were used as authorization. The supplied pasted development request governed the scope of work.
