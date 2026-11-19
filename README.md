# All In One Bail Bonds: website

A fast, mobile-first website for All In One Bail Bonds (Raleigh, Durham and Wilson, NC), built to rank in Google and to be quoted by AI assistants.

- **Preview:** https://joecodecreations.github.io/all_in_one_bail_bonds/ (GitHub Pages, served from `docs/`)
- **Status:** preview for the owner. Every page has `noindex` and a "Preview" ribbon, and `robots.txt` blocks crawlers, so it cannot compete with allinonebailbonds.org in Google.

## How it's built

- Plain static HTML, one CSS file and one small JavaScript file. No framework, no tracking, no web fonts, no third-party scripts.
- `python3 build.py` (standard library only) turns `src/` and `content.py` into `docs/`.
- **Every business fact lives in `src/site.json`:** phones, addresses, review counts, payment wording, the agent's name. Change it there, rebuild, and every page, the structured data, `llms.txt` and the sitemap update together.
- **Every county fact lives in `src/data/counties.json`** (jail, courthouse, clerk phone, official inmate lookup), each with its source links.
- Page copy is in `content.py`.

## What's on the site (39 pages)

Home · 3 office pages · 18 county pages · service areas · how bail works in NC · cost guide with a 15% calculator · payment arrangements · 5 charge pages (DWI, felony, misdemeanor, domestic violence, missed court) · 3 jail guides (Wake, Durham, Wilson) · FAQ · reviews · about · contact · Spanish page (`/fianzas/`).

## SEO and AI-search features

- Unique title and description on every page, one H1, clean URLs, breadcrumbs (visible and in structured data).
- JSON-LD on every page, generated from `site.json`: `Organization`, three `LocalBusiness` offices, `WebSite`, `BreadcrumbList`, `FAQPage` (always matching the visible FAQ), `Service`, `Person`.
- Answer-first copy with real numbers, `llms.txt`, `sitemap.xml`, share cards, web manifest.
- Tap-to-call on every screen, a sticky Call / Text bar on phones, and a bond request form that opens the visitor's own email or text app (nothing is stored).
- Legal guardrails for NC bail agents are built into the copy: no price promises beyond the 15% statutory cap, no attorney recommendations, no rewards, and a "not affiliated with any government agency" notice on jail and county pages.

## Commands

```bash
python3 build.py              # build docs/ (prints WARN lines for broken internal links)
python3 tools/images.py       # logo sizes, favicon and share card (needs Pillow)
python3 tools/shots.py        # full-page screenshots, desktop + mobile (needs Pillow and Google Chrome)
```

## Going live on allinonebailbonds.org

1. Confirm the items marked `CONFIRM` in `src/site.json` with the owner (Wilson suite and ZIP, texting, Spanish service, license number, payment methods).
2. Set `"preview": false` and rebuild. That removes `noindex` and the ribbon, opens `robots.txt`, and points canonical URLs, the sitemap, structured data and `llms.txt` at `https://allinonebailbonds.org`.
3. Point the domain at GitHub Pages (add a `CNAME` file to `docs/`) or upload `docs/` to any static host.
4. Redirect the old URLs: `/contact` → `/contact/`, and `/projects` and `/biography` (template filler) → `/about/`.
