#!/usr/bin/env python3
"""Build the All In One Bail Bonds site: src/ -> docs/ (GitHub Pages serves docs/).

    python3 build.py

Standard library only. Every business fact comes from src/site.json; every county fact
(jail, courthouse, clerk phone) comes from src/data/counties.json. Page copy lives in content.py.
"""
import html
import json
import shutil
from pathlib import Path
from urllib.parse import quote_plus, urlparse

ROOT = Path(__file__).resolve().parent
SRC, OUT = ROOT / "src", ROOT / "docs"
S = json.loads((SRC / "site.json").read_text())
CD = json.loads((SRC / "data" / "counties.json").read_text())
COUNTIES = CD["counties"]
STATE = CD["statewide"]

BASE_URL = (S["base_url"] if S["preview"] else S["live_base_url"]).rstrip("/")
B = urlparse(BASE_URL).path.rstrip("/")          # "" on a root domain, "/all_in_one_bail_bonds" on Pages
OFFICES = S["offices"]
TOTAL_REVIEWS = sum(o["google_reviews"] for o in OFFICES)
PHONE, TEL = S["phone"], "tel:" + S["phone_e164"]
SMS = "sms:" + S["phone_e164"]
e = html.escape

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.1.37 2.3.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.3.2 2.500.57 3.600a1 1 0 0 1-.25 1z"/></svg>'.replace("2.500", "2.5").replace("3.600", "3.6")
ICON_MSG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/></svg>'


def u(path=""):
    """Site-relative URL that works on a root domain and under /repo-name/ on GitHub Pages."""
    return B + "/" + path.lstrip("/")


def absu(path=""):
    return BASE_URL + "/" + path.lstrip("/")


def call_btn(cls="btn btn-gold", label=None, tel=TEL, phone=PHONE, track="call"):
    return f'<a class="{cls}" href="{tel}" data-track="{track}">{ICON_PHONE}{label or "Call " + phone}</a>'


def text_btn(cls="btn btn-glass", label="Text us"):
    if not S["sms_enabled"]:
        return ""
    return f'<a class="{cls}" href="{SMS}" data-track="text">{ICON_MSG}{label}</a>'


MARK = (SRC / "brand" / "mark.svg").read_text().replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"', 1)
MENU_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h11" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" fill="none"/></svg>'


def icon(name, cls="ico", alt=""):
    return f'<img class="{cls}" src="{u("img/icons/" + name + ".webp")}" width="64" height="64" alt="{e(alt)}" loading="lazy" decoding="async">'


def tile(name):
    return f'<span class="ico-tile">{icon(name, "")}</span>'


def pic(name, alt="", cls="", eager=False, sizes="(min-width: 1000px) 50vw, 100vw"):
    """Responsive scene image from src/img/scenes (900 and 1600 px WebP, JPEG fallback)."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{u("img/scenes/" + name + "-900.webp")} 900w, {u("img/scenes/" + name + "-1600.webp")} 1600w" sizes="{sizes}">'
            f'<img class="{cls}" src="{u("img/scenes/" + name + "-1600.jpg")}" alt="{e(alt)}" width="1600" height="900" {load} decoding="async"></picture>')


def maps_url(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(q)


def office_by_city(city):
    return next(o for o in OFFICES if o["city"] == city)


def county_slug(c):
    return c["slug"] + "-bail-bonds"


GOV_NOTE = ('<p class="note gov"><strong>Please note:</strong> All In One Bail Bonds is a private bail bond agency. '
            'We are not affiliated with any sheriff\'s office, jail, court or government agency. '
            'Addresses and phone numbers on this page come from official county and North Carolina Judicial Branch '
            'websites; call the facility to confirm before you drive there.</p>')


def faq_html(faqs):
    return "\n".join(f'<details><summary>{e(q)}</summary><div><p>{a}</p></div></details>' for q, a in faqs)


def strip_tags(s):
    import re
    return html.unescape(re.sub(r"<[^>]+>", "", s))


# ---------------------------------------------------------------- structured data
def org_ld():
    same = [v for k, v in S["social"].items() if not k.startswith("_") and v]
    d = {"@type": "Organization", "@id": absu("#org"), "name": S["name"], "url": absu(""),
         "logo": absu("img/logo-512.png"), "telephone": S["phone_e164"], "email": S["email"],
         "slogan": S["tagline"], "areaServed": {"@type": "State", "name": "North Carolina"}}
    if same:
        d["sameAs"] = same
    return d


def office_ld(o):
    return {"@type": "LocalBusiness", "@id": absu(o["slug"] + "/#office"),
            "name": f'{S["name"]} {o["city"]}', "url": absu(o["slug"] + "/"),
            "image": absu("img/og.png"), "telephone": o["phone_e164"], "email": S["email"],
            "priceRange": "$$", "parentOrganization": {"@id": absu("#org")},
            "address": {"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["locality"],
                        "addressRegion": "NC", "postalCode": o["zip"], "addressCountry": "US"},
            "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                          "opens": "00:00", "closes": "23:59"},
            "areaServed": [{"@type": "AdministrativeArea", "name": f"{c} County, North Carolina"}
                           for c, city in S["county_office"].items() if city == o["city"]]}


def crumbs_ld(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": absu(p)} for i, (n, p) in enumerate(crumbs)]}


def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs]}


# ---------------------------------------------------------------- page shell
NAV = [("Locations", "service-areas/"), ("How bail works", "how-bail-works-nc/"), ("Cost", "bail-bond-cost-nc/"),
       ("FAQ", "faq/"), ("Reviews", "reviews/"), ("About", "about/"), ("Contact", "contact/")]
PAGES = []  # (path, title, lastmod-priority) for sitemap + llms.txt


def shell(path, title, desc, body, crumbs=None, ld=None, lang="en", hero=""):
    """Wrap a page. `crumbs` is [(name, path)] after Home."""
    crumbs = [("Home", "")] + (crumbs or [])
    graph = [org_ld(), {"@type": "WebSite", "@id": absu("#site"), "url": absu(""), "name": S["name"],
                         "publisher": {"@id": absu("#org")}, "inLanguage": "en-US"}]
    if len(crumbs) > 1:
        graph.append(crumbs_ld(crumbs))
    graph += ld or []
    canonical = absu(path)
    robots = '<meta name="robots" content="noindex,nofollow">' if S["preview"] else '<meta name="robots" content="index,follow,max-image-preview:large">'
    ribbon = '<div class="ribbon"><b>Preview</b> for owner review. Not yet the live All In One Bail Bonds website.</div>' if S["preview"] else ""
    nav = "".join(f'<a href="{u(p)}"{" aria-current=\"page\"" if p == path else ""}>{n}</a>' for n, p in NAV)
    drawer = "".join(f'<a href="{u(p)}">{n}</a>' for n, p in
                     [(f'{o["city"]} office', o["slug"] + "/") for o in OFFICES] + NAV +
                     ([("Español", "fianzas/")] if S["spanish_enabled"] else []))
    bar_cls = "actionbar" if S["sms_enabled"] else "actionbar one"
    es = f' · <a href="{u("fianzas/")}" lang="es">Español</a>' if S["spanish_enabled"] else ""
    lic = f' · NC license #{e(S["agent"]["license_number"])}' if S["agent"]["license_number"] else ""
    offices_f = "".join(
        f'<li style="margin-bottom:12px"><a href="{u(o["slug"] + "/")}"><strong>{o["city"]}</strong></a><br>'
        f'{e(o["street"])}<br>{o["locality"]}, NC {o["zip"]}<br><a href="tel:{o["phone_e164"]}">{o["phone"]}</a></li>'
        for o in OFFICES)
    crumb_html = ""
    if len(crumbs) > 1:
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(
            (f'<a href="{u(p)}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page">{e(n)}</span>')
            for i, (n, p) in enumerate(crumbs)) + "</nav>"
    body = body.replace("{{CRUMBS}}", crumb_html)
    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0A1A33">
<link rel="preload" href="{u('assets/fonts/jakarta-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<meta name="format-detection" content="telephone=yes">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(S['name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{absu('img/og.png')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{u('favicon.ico')}" sizes="32x32">
<link rel="icon" href="{u('brand/mark.svg')}" type="image/svg+xml">
<link rel="icon" href="{u('img/logo-192.png')}" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{u('img/logo-192.png')}">
<link rel="manifest" href="{u('site.webmanifest')}">
<link rel="stylesheet" href="{u('assets/style.css')}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{ribbon}
<header class="site"><div class="wrap">
<a class="brand" href="{u('')}" aria-label="All In One Bail Bonds, home">{MARK}<span><b>All In One</b><i>Bail Bonds</i></span></a>
<nav class="main" aria-label="Main">{nav}</nav>
<div class="hdr-cta">{call_btn("btn btn-gold btn-sm", '<span class="lbl">Call </span>24/7', track="call-header")}<button class="menu-btn" aria-expanded="false" aria-controls="drawer" aria-label="Menu">{MENU_ICON}</button></div>
</div><nav class="drawer" id="drawer" aria-label="Mobile">{drawer}</nav></header>
<main id="main">
{body}
<section class="band"><div class="bg">{pic("highway", "")}</div><div class="wrap rv"><span class="live"><i></i>An agent is available now</span><h2 style="margin-top:12px">We answer. Any hour.</h2><p>A licensed bail agent answers 24 hours a day, every day. Have the person's full name and the county ready if you can.</p><div class="cta">{call_btn(track="call-band")}{text_btn("btn btn-glass", "Text " + PHONE)}</div></div></section>
</main>
<footer class="site"><div class="wrap"><div class="fgrid">
<div><a class="brand" href="{u('')}" style="margin-bottom:14px"><img src="{u('brand/mark.svg')}" width="44" height="44" alt=""><span><b>All In One</b><i>Bail Bonds</i></span></a><p>24-hour bail bond service across North Carolina, with offices in Raleigh, Durham and Wilson.</p><p><a href="{TEL}"><strong>{PHONE}</strong></a><br><a href="mailto:{S['email']}">{S['email']}</a></p></div>
<div><h3>Offices</h3><ul>{offices_f}</ul></div>
<div><h3>Bail bonds</h3><ul><li><a href="{u('dwi-bail-bonds/')}">DWI / DUI bonds</a></li><li><a href="{u('felony-bail-bonds/')}">Felony bonds</a></li><li><a href="{u('misdemeanor-bail-bonds/')}">Misdemeanor bonds</a></li><li><a href="{u('domestic-violence-bail-bonds/')}">Domestic violence bonds</a></li><li><a href="{u('failure-to-appear-bonds/')}">Missed court / failure to appear</a></li><li><a href="{u('payment-plans/')}">Payment arrangements</a></li></ul></div>
<div><h3>Help</h3><ul><li><a href="{u('how-bail-works-nc/')}">How bail works in NC</a></li><li><a href="{u('bail-bond-cost-nc/')}">What a bail bond costs</a></li><li><a href="{u('jail-guides/wake-county-jail/')}">Wake County jail guide</a></li><li><a href="{u('jail-guides/durham-county-jail/')}">Durham County jail guide</a></li><li><a href="{u('jail-guides/wilson-county-jail/')}">Wilson County jail guide</a></li><li><a href="{u('service-areas/')}">All counties we serve</a></li><li><a href="{u('faq/')}">FAQ</a></li></ul></div>
</div><p class="legal">© 2026 {e(S['name'])}. {e(S['agent']['name'])}, {e(S['agent']['title'])}{lic}. We are a private bail bond agency, not a law firm, and nothing on this site is legal advice. We are not affiliated with any court, sheriff's office, jail or government agency. In North Carolina the bail bond premium cannot exceed 15% of the bond amount (N.C. Gen. Stat. § 58-71-95).{es}</p></div></footer>
<div class="{bar_cls}">{call_btn("btn btn-gold", "Call 24/7", track="call-sticky")}{text_btn("btn btn-glass", "Text us")}</div>
<script src="{u('assets/app.js')}" defer></script>
</body>
</html>
"""
    dest = OUT / path / "index.html" if not path.endswith(".html") else OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc)
    if not path.endswith(".html"):
        PAGES.append((path, title, desc))


def page_hero(h1, lede, eyebrow="", cta=True, bg=None, office=None):
    eb = f'<span class="live"><i></i>{eyebrow}</span>' if eyebrow else ""
    cb = call_btn(tel="tel:" + office["phone_e164"], phone=office["phone"]) if office else call_btn()
    c = f'<div class="cta">{cb}{text_btn()}</div>' if cta else ""
    b = f'<div class="bg">{pic(bg, "", eager=True, sizes="100vw")}</div>' if bg else ""
    return f'<section class="page-hero{" has-bg" if bg else ""}">{b}<div class="wrap">{{{{CRUMBS}}}}{eb}<h1>{h1}</h1><p class="lede">{lede}</p>{c}</div></section>'


def office_card(o, link=True):
    more = f'<a class="btn btn-line btn-sm" href="{u(o["slug"] + "/")}">Office details</a>' if link else ""
    return (f'<div class="card office"><h3>{o["city"]}, NC</h3>'
            f'<p class="rating"><span class="stars" aria-hidden="true">★★★★★</span> {o["google_rating"]} · {o["google_reviews"]} Google reviews</p>'
            f'<address>{e(o["street"])}<br>{o["locality"]}, NC {o["zip"]}</address>'
            f'<div class="acts">{call_btn("btn btn-gold btn-sm", o["phone"], "tel:" + o["phone_e164"], track="call-office-" + o["city"].lower())}'
            f'<a class="btn btn-line btn-sm" href="{maps_url(o["maps_query"])}" rel="noopener">Directions</a>{more}</div></div>')


def county_pills(exclude=None):
    return '<ul class="pill-list">' + "".join(
        f'<li><a href="{u(county_slug(c) + "/")}">{c["name"]} County</a></li>' for c in COUNTIES if c["name"] != exclude) + "</ul>"


def write_static():
    for d in ("assets", "img", "video", "brand"):
        if (SRC / d).exists():
            shutil.copytree(SRC / d, OUT / d, dirs_exist_ok=True)
    if (SRC / "favicon.ico").exists():
        shutil.copy(SRC / "favicon.ico", OUT / "favicon.ico")
    (OUT / ".nojekyll").write_text("")
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": S["name"], "short_name": "All In One Bail", "start_url": u(""), "display": "browser",
        "background_color": "#0F0F12", "theme_color": "#0F0F12",
        "icons": [{"src": u("img/logo-192.png"), "sizes": "192x192", "type": "image/png"},
                  {"src": u("img/logo-512.png"), "sizes": "512x512", "type": "image/png"}]}, indent=1))
    # robots.txt: a preview must not be indexed; the live site welcomes search and AI crawlers.
    if S["preview"]:
        robots = "User-agent: *\nDisallow: /\n"
    else:
        robots = "User-agent: *\nAllow: /\n\nSitemap: " + absu("sitemap.xml") + "\n"
    (OUT / "robots.txt").write_text(robots)
    urls = "".join(f"<url><loc>{absu(p)}</loc><lastmod>2026-11-19</lastmod></url>\n" for p, _, _ in PAGES)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    # llms.txt: a plain-language fact sheet for AI assistants.
    L = [f"# {S['name']}", "",
         f"> 24-hour bail bond agency in North Carolina with offices in Raleigh, Durham and Wilson. "
         f"Licensed NC bail agents post secured appearance bonds at county jails statewide. Main phone {PHONE}.", "",
         "## Key facts",
         f"- Phone (24/7): {PHONE}. Email: {S['email']}.",
         f"- Bail agent: {S['agent']['name']}, {S['agent']['title']}.",
         f"- Hours: {S['hours']}.",
         "- Cost: in North Carolina the bail bond premium cannot exceed 15% of the bond amount (N.C. Gen. Stat. 58-71-95). The premium is the fee for the service and is not refunded when the case ends.",
         f"- Payment: {S['payment_line'].lower()}; any deferred payment is put in a signed written agreement, as NC law requires.",
         f"- Google reviews as of {S['reviews_as_of']}: " + "; ".join(f"{o['city']} {o['google_rating']} stars ({o['google_reviews']} reviews)" for o in OFFICES) + ".",
         "- Not a law firm; does not give legal advice or recommend attorneys. Not affiliated with any court, jail or government agency.", "",
         "## Offices"]
    L += [f"- {o['city']}: {o['street']}, {o['locality']}, NC {o['zip']}. Phone {o['phone']}." for o in OFFICES]
    L += ["", "## Pages"] + [f"- [{t}]({absu(p)}): {d}" for p, t, d in PAGES]
    (OUT / "llms.txt").write_text("\n".join(L) + "\n")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    from content import build_all  # content.py uses the helpers above
    build_all()
    write_static()
    # sanity: every internal link must resolve to a built file
    import re
    bad = set()
    for f in OUT.rglob("*.html"):
        for href in re.findall(r'href="([^"#]+)', f.read_text()):
            if href.startswith(B + "/") or href == B:
                rel = href[len(B):].lstrip("/")
                t = OUT / rel
                if not (t.is_file() or (t / "index.html").is_file()):
                    bad.add(href)
    for h in sorted(bad):
        print("WARN broken link:", h)
    print(f"built {len(PAGES)} pages -> {OUT}  (preview={S['preview']}, base={BASE_URL})")


if __name__ == "__main__":
    import build  # run as the importable module so content.py shares one set of globals
    build.main()
