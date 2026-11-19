"""Page copy for the All In One Bail Bonds site. Imported by build.py.

Rules this copy follows (see ../ASSUMPTIONS.md and ../research/C_keywords_market_law.md):
- No release-time or outcome guarantees. No price promises beyond what NC law states.
- Never name or recommend an attorney (G.S. 58-71-95(4)). No rewards or discounts (58-71-95(3)).
- Jail and court pages carry a "not affiliated with any government agency" notice (58-71-95(9)).
- Reviews are reported as counts only; no customer's words are reproduced without permission.
"""
from build import *  # noqa: F401,F403

N = S["name"]
AG = S["agent"]
PAY = S["payment_line"]
STEPS3 = [
    ("Call us with the basics", "Tell us the person's full name, date of birth if you know it, and which county jail they are in. We find the bond amount and the conditions the magistrate or judge set."),
    ("We explain the cost and the paperwork", "You hear the premium and any collateral up front, before you sign anything. The person who signs with us (the cosigner) agrees to make sure the defendant goes to every court date."),
    ("We post the bond at the jail", "A licensed agent posts the bond with the jail. The jail then processes the release. How long that takes is up to the jail, not the bondsman."),
]
READY = ["The person's full legal name (and date of birth if you have it)",
         "The county or jail where they are being held",
         "The charge and the bond amount, if you know them",
         "Your own name and a phone number where we can reach you"]

CHARGES = [
    ("dwi-bail-bonds", "DWI / DUI bail bonds", "Arrested for driving while impaired? What happens at the magistrate's office and how a bond gets posted."),
    ("felony-bail-bonds", "Felony bail bonds", "Larger bonds, and some charges where only a judge can set release conditions."),
    ("misdemeanor-bail-bonds", "Misdemeanor bail bonds", "Smaller bonds that can often be handled over the phone in one call."),
    ("domestic-violence-bail-bonds", "Domestic violence bonds", "Why there is usually a wait before a bond is set, and what the 48-hour rule means."),
    ("failure-to-appear-bonds", "Missed court / failure to appear", "An order for arrest after a missed court date, and how to deal with it before it gets worse."),
]

FAQ_CORE = [
    ("How much does a bail bond cost in North Carolina?",
     "North Carolina law caps the bail bond premium at 15% of the bond amount (N.C. Gen. Stat. § 58-71-95). On a $5,000 bond the premium can be no more than $750. A bondsman may also ask for collateral, but may not charge extra application or processing fees. Call us for the exact cost of a specific bond."),
    ("Are you really open 24 hours?",
     f"Yes. Arrests happen at night, on weekends and on holidays, so a licensed bail agent answers {PHONE} around the clock."),
    ("Do I get the premium back when the case is over?",
     "No. The premium is the fee for the bondsman's service and for taking on the risk of the full bond, so it is not returned when the case ends. Collateral is different: under NC law it must be returned within 15 days after the bondsman's liability on the bond finally ends."),
    ("Can I make payments?",
     f"{PAY}. Whether a payment arrangement is available depends on the bond and your situation. When part of the premium is paid after release, North Carolina law requires a written agreement, signed by both sides, that lists every payment date and amount, and you get a copy."),
    ("How long does it take to get someone out of jail?",
     "It depends on the jail. We can usually start the paperwork as soon as a bond has been set. After we post the bond, the jail processes the release, and that part is outside any bondsman's control. Busy nights and shift changes can add time."),
    ("What does the person who signs the bond agree to?",
     "The cosigner (also called the indemnitor) promises that the defendant will go to every court date. If the defendant misses court and the bond is forfeited, the cosigner can be responsible for the full bond amount."),
]

FAQ_MORE = [
    ("What is a secured bond?",
     "A secured bond means money or property has to back the bond before the person is released. It can be secured with a cash deposit of the full amount, with a mortgage on property, or by a licensed bail bondsman acting as surety. An unsecured bond needs no money up front; the person owes the amount only if they miss court."),
    ("Who decides the bond amount?",
     "A magistrate sets release conditions soon after most arrests. For some cases, including certain serious felonies and domestic violence charges, North Carolina law says a judge must set the conditions, and the person can be held up to 48 hours until a judge does."),
    ("Did the law on pretrial release change recently?",
     "Yes. Since December 1, 2025, a written promise to appear is no longer a release option in North Carolina. Courts must also order a secured bond or house arrest with electronic monitoring for defendants with three or more convictions for Class 1 misdemeanors or higher in the past 10 years, and release rules are stricter for charges the law defines as violent offenses."),
    ("Can you bail someone out in any county?",
     "We write bonds across North Carolina. Our offices are in Raleigh, Durham and Wilson, and we work regularly in the surrounding counties. Call us with the county and we will tell you right away whether we can help there."),
    ("Can I handle everything by phone?",
     "Often, yes. Call us and we will tell you what can be done by phone or electronically for your bond and what needs a signature in person."),
    ("What happens if the defendant misses a court date?",
     "The court can issue an order for arrest and start forfeiting the bond. Call us right away if a court date was missed or is about to be. Acting quickly gives everyone more options."),
    ("Can you recommend a lawyer?",
     "No. North Carolina law does not allow a bail bondsman to recommend or suggest any particular attorney. If you cannot afford a lawyer, ask the court about a court-appointed attorney at the first appearance."),
    ("What forms of payment do you take?",
     "Call us and we will go over payment options for your bond."),
    ("Is my call private?",
     "Yes. We keep what you tell us discreet. An arrest is stressful enough without the whole neighborhood knowing."),
    ("How do I find out if someone is in jail?",
     f"Many county sheriffs publish an inmate lookup, and you can always call the jail. Our <a href=\"{u('service-areas/')}\">county pages</a> list the jail phone number and the official lookup link for each county we serve. If you are not sure where the person is, call us and we will help you find out."),
]


def steps_cards():
    return '<div class="grid c3">' + "".join(
        f'<div class="card rv">{tile(["phone", "document", "home"][i - 1])}<h3>{i}. {t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS3, 1)) + "</div>"


def cost_examples():
    rows = "".join(f"<tr><th>${a:,} bond</th><td>No more than ${a * 15 // 100:,}</td></tr>" for a in (1000, 2500, 5000, 10000, 25000, 50000))
    return f'<table class="facts"><tr><th>Bond amount</th><td><strong>Maximum premium under NC law (15%)</strong></td></tr>{rows}</table>'


def service_ld(name, desc):
    return {"@type": "Service", "name": name, "description": desc, "provider": {"@id": absu("#org")},
            "areaServed": {"@type": "State", "name": "North Carolina"}, "serviceType": "Bail bond service"}


# ------------------------------------------------------------------ home
def calc_html(start=5000, count=True, heading="What will a bail bond cost?", track="call-calculator"):
    chips = "".join(f'<button type="button" data-v="{v}">${v:,}</button>' for v in (1000, 2500, 5000, 10000, 25000, 50000))
    cnt = f"""<div class="row"><div class="lab"><label for="c-n-{start}">Number of bonds</label><span class="val o-count">1 bond</span></div>
<input class="r-count" id="c-n-{start}" type="range" min="1" max="5" step="1" value="1" aria-describedby="c-n-help-{start}">
<div class="ticks" id="c-n-help-{start}"><span>1</span><span>Separate charges can each have a bond</span><span>5</span></div></div>""" if count else ""
    return f"""<div class="calc" data-calc>
<h2>{icon("calculator", "", "")}{heading}</h2>
<div class="row"><div class="lab"><label for="c-a-{start}">Bond amount set by the court</label><output class="o-amount" for="c-a-{start}">${start:,}</output></div>
<input class="r-amount" id="c-a-{start}" type="range" min="0" max="60" step="1" value="20" data-start="{start}">
<div class="ticks"><span>$250</span><span>$10,000</span><span>$250,000</span></div>
<div class="chips" aria-label="Common bond amounts">{chips}</div></div>
{cnt}
<div class="result">
<div><div class="big o-premium">${start * 15 // 100:,}</div><div class="cap">most a bondsman may charge under NC law (15%)</div></div>
</div>
<div style="margin-top:16px;font-size:.9rem;color:#cbd7ec">
<div style="display:flex;justify-content:space-between"><span>Paying the court in cash</span><b class="o-cash" style="color:#fff">${start:,}</b></div>
<div style="height:10px;border-radius:99px;background:rgba(255,255,255,.12);margin:6px 0 12px"><div class="bar-cash" style="height:100%;width:100%;border-radius:99px;background:#5d7397"></div></div>
<div style="display:flex;justify-content:space-between"><span>With a bondsman, at most</span><b class="o-premium" style="color:var(--sky2)">${start * 15 // 100:,}</b></div>
<div style="height:10px;border-radius:99px;background:rgba(255,255,255,.12);margin:6px 0 4px"><div class="bar-prem" style="height:100%;width:15%;border-radius:99px;background:var(--gold)"></div></div>
<div style="color:#9fb1cf;margin-top:8px">Cash you don't have to put up: <b class="o-keep" style="color:#fff">${start * 85 // 100:,}</b></div>
</div>
<small class="fine">The legal maximum, not a quote. Larger bonds may also need collateral. Call {PHONE} for the exact cost of your bond.</small>
{call_btn("btn btn-gold", "Get the exact cost: " + PHONE, track=track)}
</div>"""


FEATURES = [
    ("clock", "Open 24/7, really", "A licensed bail agent answers at 2 a.m., on weekends and on holidays."),
    ("star", f"{TOTAL_REVIEWS} five-star reviews", "A 5.0 rating at all three offices, earned one family at a time."),
    ("pin", "Three local offices", "Raleigh, Durham and Wilson, plus bonds written across North Carolina."),
    ("money", "Clear about cost", "You hear the premium and any collateral before you sign. Never above the 15% legal cap."),
    ("chat", "Call or text", "Text if you can't talk freely. We'll answer the same way."),
    ("shield", "Discreet", "Your family's business stays your family's business."),
]


def home():
    title = "24/7 Bail Bonds in Raleigh, Durham & Wilson NC | All In One"
    desc = f"Fast, discreet bail bonds across North Carolina, open 24/7. Offices in Raleigh, Durham and Wilson. 5.0 stars from {TOTAL_REVIEWS} Google reviews. Call {PHONE}."
    ready = "".join(f"<li>{x}</li>" for x in READY)
    feats = '<div class="grid c3 feats">' + "".join(
        f'<div class="card rv">{tile(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in FEATURES) + "</div>"
    journey = [("night-call", "The call", "Any hour", "Call or text any hour. Tell us the name and the county; we find the bond and the conditions."),
               ("signing", "The paperwork", "Before you sign", "You hear the cost before you sign. The cosigner agrees to make sure every court date is kept."),
               ("reunion", "The ride home", "When the jail releases", "We post the bond at the jail. The jail processes the release, and your family is back together.")]
    jhtml = '<div class="journey">' + "".join(
        f'<div class="step rv">{pic(img, alt, sizes="(min-width: 760px) 33vw, 100vw")}<div class="in"><span class="n">{i}</span><span class="t">{when}</span><h3>{t}</h3><p>{d}</p></div></div>'
        for i, (img, t, when, d) in enumerate(journey, 1)
        for alt in [{"night-call": "A woman on the phone at her kitchen table late at night",
                     "signing": "Hands signing a bond agreement at a desk under a lamp",
                     "reunion": "A young man hugging his mother at sunrise"}[img]]) + "</div>"
    offices = '<div class="grid c3">' + "".join(f'<div class="rv">{office_card(o)}</div>' for o in OFFICES) + "</div>"
    charges = '<div class="grid c3">' + "".join(
        f'<a class="card rv" href="{u(s + "/")}">{tile(ic)}<h3>{t}</h3><p>{d}</p><span class="more">Learn more →</span></a>'
        for (s, t, d), ic in zip(CHARGES, ["car", "scales", "document", "home", "calendar"])) + \
        f'<a class="card rv" href="{u("payment-plans/")}">{tile("handshake")}<h3>Payment arrangements</h3><p>{PAY}. See how they work and what the law requires.</p><span class="more">Learn more →</span></a></div>'
    body = f"""
<section class="hero">
<div class="hero-media"><video autoplay muted loop playsinline preload="metadata" poster="{u('img/scenes/raleigh-dawn-poster.jpg')}" aria-hidden="true"><source src="{u('video/raleigh-dawn.mp4')}" type="video/mp4"></video></div>
<div class="wrap hero-grid">
<div>
<span class="live"><i></i>Open now · An agent answers 24/7</span>
<h1>Bring them <em>home.</em></h1>
<p class="lede">When someone you love is in jail, you need a straight answer fast. Call {N} and a licensed North Carolina bail agent tells you what the bond costs and what happens next, in Raleigh, Durham, Wilson and across the state.</p>
<div class="cta">{call_btn(track="call-hero")}{text_btn()}</div>
<ul class="proof">
<li><span class="stars" aria-hidden="true">★★★★★</span> 5.0 · {TOTAL_REVIEWS} Google reviews</li>
<li>Licensed NC bail agents</li>
<li>{PAY}</li>
</ul>
</div>
<div class="glass"><h2>Have this ready when you call</h2><ul class="checks">{ready}</ul><p style="margin:14px 0 0;color:#b9c7de;font-size:.93rem">Don't have all of it? Call anyway. We can usually find the rest.</p></div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
<div class="stat-row stat-float">
<div class="stat rv"><b data-count="{TOTAL_REVIEWS}">{TOTAL_REVIEWS}</b><small>five-star Google reviews</small></div>
<div class="stat rv"><b data-count="5.0">5.0</b><small>rating at all 3 offices</small></div>
<div class="stat rv"><b>3</b><small>offices: Raleigh, Durham, Wilson</small></div>
<div class="stat rv"><b>24/7</b><small>a bail agent answers</small></div>
</div>
<p class="sub" style="margin-top:12px;font-size:.85rem">Google review counts as of {S['reviews_as_of']}.</p>
</div></section>

<section class="section" style="padding-top:10px"><div class="wrap">
<span class="eyebrow">How it works</span>
<h2>From tonight's phone call to the ride home</h2>
<p class="sub">Three steps. We handle the parts we can, and we're honest about the parts only the jail controls.</p>
{jhtml}
<p style="margin-top:20px"><a href="{u('how-bail-works-nc/')}"><b>Read the full guide to how bail works in North Carolina →</b></a></p>
</div></section>

<section class="section alt"><div class="wrap two">
<div class="prose rv">
<span class="eyebrow">Cost</span>
<h2>Know the cost before you call</h2>
<p>North Carolina law caps the bail bond premium at <strong>15% of the bond amount</strong>. A bondsman may ask for collateral on larger bonds, but may not add application or processing fees on top.</p>
<p>Slide to the bond amount the court set. The calculator shows the most any licensed bondsman in North Carolina is allowed to charge, and how much cash you don't have to put up.</p>
<p>{PAY}. If part of the premium is paid after release, the schedule goes in a written agreement both sides sign, and you get a copy.</p>
<p><a class="btn btn-line" href="{u('bail-bond-cost-nc/')}">Full cost guide</a></p>
</div>
<div class="rv">{calc_html(5000, count=False, track="call-calculator-home")}</div>
</div></section>

<section class="section"><div class="wrap">
<span class="eyebrow">Why families call us</span>
<h2>The bondsman who answers</h2>
{feats}
</div></section>

<section class="section office-band"><div class="bg">{pic("raleigh", "", sizes="100vw")}</div><div class="wrap">
<span class="eyebrow" style="color:var(--sky2)">Our offices</span>
<h2>Three offices, one phone call</h2>
<p class="sub" style="color:#c6d3e8">We write bonds statewide. Most of our work is in the counties around these three offices.</p>
{offices}
</div></section>

<section class="section alt"><div class="wrap">
<span class="eyebrow">Bonds we post</span>
<h2>Misdemeanor, felony, DWI and more</h2>
{charges}
</div></section>

<section class="section dark review-band"><div class="wrap rv">
<div class="stars" aria-hidden="true">★★★★★</div>
<div class="big" data-count="{TOTAL_REVIEWS}">{TOTAL_REVIEWS}</div>
<h2 style="margin-top:6px">five-star reviews on Google</h2>
<p class="sub" style="margin:0 auto 20px">Every one of our offices holds a 5.0 rating. Read what families wrote, in their own words.</p>
<div class="reviews-grid">{"".join(f'<a class="card" style="text-decoration:none" href="{maps_url(o["maps_query"])}" rel="noopener"><h3>{o["city"]}</h3><p class="stars" style="margin:0">★★★★★</p><p style="margin:4px 0 0">{o["google_rating"]} · {o["google_reviews"]} reviews <span style="color:var(--sky2)">→</span></p></a>' for o in OFFICES)}</div>
</div></section>

<section class="section"><div class="wrap two flip">
<div class="figure rv">{pic("desk", "A tidy office desk at night with paperwork, a lamp and a phone")}</div>
<div class="prose rv">
<span class="eyebrow">A word from your bondsman</span>
<h2>Helping every step of the way</h2>
<p>"I know when a loved one is in jail it is a trying experience, not only for the defendant, but the family as well. Our friendly, knowledgeable staff will be happy to answer any questions you may have. We want to earn your trust, we take pride in the services we provide, and we look forward to handling your jail release needs."</p>
<p><strong>{AG['name']}</strong><br>{AG['title']}</p>
<p><a href="{u('about/')}">About {N} →</a></p>
</div></div></section>

<section class="section alt"><div class="wrap">
<span class="eyebrow">Where we work</span>
<h2>Counties we serve</h2>
<p class="sub">Each county page lists the jail address, the clerk's phone number and the official inmate lookup.</p>
{county_pills()}
<p style="margin-top:16px">Not on the list? <a href="{TEL}">Call {PHONE}</a>. We write bonds across North Carolina.</p>
</div></section>

<section class="section"><div class="wrap">
<span class="eyebrow">Questions</span>
<h2>What families ask us first</h2>
{faq_html(FAQ_CORE)}
<p style="margin-top:16px"><a href="{u('faq/')}"><b>More questions and answers →</b></a></p>
</div></section>
"""
    shell("", title, desc, body, ld=[office_ld(o) for o in OFFICES] + [faq_ld(FAQ_CORE)])


# ------------------------------------------------------------------ offices
def office_pages():
    for o in OFFICES:
        cs = [c for c in COUNTIES if S["county_office"].get(c["name"]) == o["city"]]
        home_c = next(c for c in COUNTIES if c["name"] == o["county"])
        j = home_c["jail"]
        title = f'Bail Bonds {o["city"]} NC | 24/7 Bondsman | All In One Bail Bonds'
        desc = f'24-hour bail bondsman in {o["city"]}, NC. {o["google_rating"]} stars from {o["google_reviews"]} Google reviews. {o["street"]}. Call {o["phone"]} any time.'
        faqs = [
            (f'Where is your {o["city"]} office?', f'{o["street"]}, {o["locality"]}, NC {o["zip"]}. {o["area_note"]} Call {o["phone"]} before you come so an agent can meet you.'),
            (f'Which jail serves {o["county"]} County?', f'People arrested in {o["county"]} County are usually held at the {j["name"]}, {j["address"]}, {j["city"]}. See our <a href="{u(county_slug(home_c) + "/")}">{o["county"]} County page</a> for phone numbers and the official lookup.'),
            (f'Do I have to come to the {o["city"]} office in person?', 'Not always. Call first. We will tell you what can be handled by phone or electronically for your bond and what needs a signature in person.'),
            FAQ_CORE[0], FAQ_CORE[3],
        ]
        pills = '<ul class="pill-list">' + "".join(f'<li><a href="{u(county_slug(c) + "/")}">{c["name"]} County</a></li>' for c in cs) + "</ul>"
        towns = ", ".join(home_c["towns"])
        guide = {"Wake": "wake-county-jail", "Durham": "durham-county-jail", "Wilson": "wilson-county-jail"}[o["county"]]
        body = page_hero(f'Bail bonds in {o["city"]}, NC',
                         f'A licensed bail agent answers 24 hours a day for {o["city"]} and all of {o["county"]} County. Call {o["phone"]} and we will tell you the cost and the next step.',
                         f'{o["label"]} · Open 24/7', bg={"Raleigh": "raleigh", "Durham": "durham", "Wilson": "highway"}[o["city"]], office=o) + f"""
<section class="section"><div class="wrap two">
<div class="prose">
<h2>Your {o["city"]} bail bondsman</h2>
<p>{N} posts misdemeanor, felony and DWI bonds for people held in {o["county"]} County, at the {j["name"]} and the surrounding county jails. Our {o["city"]} office has a {o["google_rating"]}-star rating from {o["google_reviews"]} Google reviews (as of {S['reviews_as_of']}).</p>
<p>We serve {towns} and the rest of {o["county"]} County.</p>
<h3>How it works</h3>
<ol>{"".join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in STEPS3)}</ol>
<p><a href="{u('jail-guides/' + guide + '/')}">Step-by-step guide to bailing someone out of the {o["county"]} County jail →</a></p>
<h3>What it costs</h3>
<p>North Carolina caps the premium at 15% of the bond amount. {PAY}. <a href="{u('bail-bond-cost-nc/')}">See the cost calculator</a>.</p>
</div>
<div>
{office_card(o, link=False)}
<table class="facts" style="margin-top:16px">
<tr><th>Hours</th><td>Open 24 hours, every day</td></tr>
<tr><th>Phone</th><td><a href="tel:{o['phone_e164']}">{o['phone']}</a></td></tr>
<tr><th>Email</th><td><a href="mailto:{S['email']}">{S['email']}</a></td></tr>
<tr><th>County jail</th><td>{e(j['name'])}<br>{e(j['address'])}, {j['city']}</td></tr>
<tr><th>Courthouse</th><td>{e(home_c['courthouse']['name'])}<br>{e(home_c['courthouse']['address'])}, {home_c['courthouse']['city']}</td></tr>
</table>
</div>
</div></section>
<section class="section alt"><div class="wrap">
<h2>Counties served from the {o["city"]} office</h2>
{pills}
</div></section>
<section class="section"><div class="wrap">
<h2>{o["city"]} bail bond questions</h2>
{faq_html(faqs)}
{GOV_NOTE}
</div></section>
"""
        shell(o["slug"] + "/", title, desc, body, crumbs=[("Locations", "service-areas/"), (f'{o["city"]}', o["slug"] + "/")],
              ld=[office_ld(o), faq_ld(faqs)])


# ------------------------------------------------------------------ counties
PHONE_LABEL = {"Wilson": "Sheriff's Office", "Franklin": "Sheriff's Office", "Person": "bond inquiries", "Pitt": "inmate information"}
LOOKUP_LABEL = {"Wake": "Wake County arrest records search (recent arrests)", "Harnett": "Harnett County inmate population reports"}
LOOKUP_SKIP = {"Sampson"}   # county links a bare IP address; not something to send families to
MAG_AT_JAIL = {"Harnett", "Orange", "Wayne", "Sampson"}   # read directly on official pages
JAIL2_NO_PHONE = {"Wake"}


def jail_cell(j, label=None, show_phone=True):
    if not j:
        return ""
    addr = f'{e(j["address"])}, ' if j["address"] else ""
    z = f' {j["zip"]}' if j["zip"] else ""
    ph = f'<br><a href="tel:{"".join(ch for ch in j["phone"] if ch.isdigit())}">{j["phone"]}</a>' + (f" ({label})" if label else "") if (j["phone"] and show_phone) else ""
    return f'{e(j["name"])}<br>{addr}{j["city"]}, NC{z}{ph}'


def county_pages():
    for c in COUNTIES:
        n, seat, j, ch = c["name"], c["seat"], c["jail"], c["courthouse"]
        city = S["county_office"][n]
        o = office_by_city(city)
        slug = county_slug(c) + "/"
        lookup = "" if n in LOOKUP_SKIP else c["inmate_lookup_url"]
        lk_label = LOOKUP_LABEL.get(n, f"{n} County inmate lookup (official)")
        lookup_row = (f'<a href="{e(lookup)}" rel="noopener nofollow">{lk_label}</a>' if lookup else
                      "No official online lookup found. Call the jail, or call us and we will check for you.")
        jail_where = f'{j["name"]}' + (f', {j["address"]}, {j["city"]}' if j["address"] else f' in {j["city"]}')
        j2 = c.get("jail2")
        j2row = f'<tr><th>Second facility</th><td>{jail_cell(j2, show_phone=n not in JAIL2_NO_PHONE)}</td></tr>' if j2 else ""
        mag = "<tr><th>Magistrate</th><td>The magistrate's office is in the same building as the detention center.</td></tr>" if n in MAG_AT_JAIL else ""
        towns = ", ".join(c["towns"])
        title = f"{n} County Bail Bonds | 24/7 Bondsman in {seat}, NC"
        desc = f"24/7 bail bonds for the {j['name']} in {seat}, NC. Jail address, clerk phone and how to post bond. Call {PHONE}."
        faqs = [
            (f"Where is the {n} County jail?", f"People arrested in {n} County are generally held at the {jail_where}." + (f" {n} County also uses the {j2['name']}, {j2['address']}, {j2['city']}." if j2 else "") + " Call the facility to confirm someone is there before you drive over."),
            (f"How do I find out if someone is in the {n} County jail?", (f'Use the <a href="{e(lookup)}" rel="noopener nofollow">{lk_label}</a> or call the jail' if lookup else "Call the jail") + (f" at {j['phone']}" if j["phone"] else "") + f". You can also call us at {PHONE} and we will check for you."),
            (f"Where is criminal court in {n} County?", f"The {ch['name']} is at {ch['address']}, {ch['city']}, NC {ch['zip']}. The Clerk of Superior Court's number is {ch['clerk_phone']}. You can look up a court date on the <a href=\"{STATE['court_date_lookup']['url']}\" rel=\"noopener nofollow\">NC eCourts portal</a>."),
            (f"How much is a bail bond in {n} County?", "The same rule applies in every North Carolina county: the premium cannot be more than 15% of the bond amount. On a $2,500 bond that is no more than $375. Call us for the exact cost of a specific bond."),
        ]
        body = page_hero(f"{n} County bail bonds",
                         f"Is someone you care about being held in {seat}? {N} posts bonds in {n} County 24 hours a day. Call {PHONE} and a licensed NC bail agent will tell you the cost and what happens next.",
                         f"{seat}, North Carolina · Open 24/7", bg="highway") + f"""
<section class="section"><div class="wrap two">
<div class="prose">
<h2>Bail bondsman for {seat} and {n} County</h2>
<p>We post misdemeanor, felony and DWI bonds for people held at the {e(j['name'])}. {n} County is served from our <a href="{u(o['slug'] + '/')}">{city} office</a>, and you can reach an agent at any hour.</p>
<p>Towns we serve in {n} County include {towns}.</p>
<h3>How to bail someone out in {n} County</h3>
<ol>
<li><strong>Confirm where they are.</strong> {"Check the official lookup or call" if lookup else "Call"} the jail{f" at {j['phone']}" if j['phone'] else ""}. Or call us and we will find out.</li>
<li><strong>Find out the bond.</strong> A magistrate usually sets release conditions soon after arrest. Some charges must wait for a judge, which can take up to 48 hours.</li>
<li><strong>Call {PHONE}.</strong> We tell you the premium and any collateral before you sign anything.</li>
<li><strong>We post the bond.</strong> A licensed agent posts it with the jail, and the jail processes the release.</li>
</ol>
<h3>What it costs</h3>
<p>North Carolina law caps the bail bond premium at 15% of the bond amount. {PAY}. <a href="{u('bail-bond-cost-nc/')}">Use the cost calculator</a> or <a href="{u('payment-plans/')}">read about payment arrangements</a>.</p>
</div>
<div>
<table class="facts">
<tr><th>County jail</th><td>{jail_cell(j, PHONE_LABEL.get(n))}</td></tr>
{j2row}
<tr><th>Find an inmate</th><td>{lookup_row}</td></tr>
{mag}
<tr><th>Courthouse</th><td>{e(ch['name'])}<br>{e(ch['address'])}, {ch['city']}, NC {ch['zip']}</td></tr>
<tr><th>Clerk of Superior Court</th><td><a href="tel:{''.join(x for x in ch['clerk_phone'] if x.isdigit())}">{ch['clerk_phone']}</a></td></tr>
<tr><th>Court information</th><td><a href="{c['nccourts_url']}" rel="noopener nofollow">{n} County on nccourts.gov</a></td></tr>
<tr><th>Our nearest office</th><td><a href="{u(o['slug'] + '/')}">{city}</a>: {e(o['street'])}</td></tr>
</table>
</div>
</div></section>
<section class="section alt"><div class="wrap">
<h2>{n} County bail questions</h2>
{faq_html(faqs)}
{GOV_NOTE}
</div></section>
<section class="section"><div class="wrap">
<h2>Other counties we serve</h2>
{county_pills(exclude=n)}
</div></section>
"""
        shell(slug, title, desc, body, crumbs=[("Locations", "service-areas/"), (f"{n} County", slug)],
              ld=[service_ld(f"Bail bonds in {n} County, NC", desc), faq_ld(faqs)])


def service_areas():
    groups = ""
    for o in OFFICES:
        cs = [c for c in COUNTIES if S["county_office"].get(c["name"]) == o["city"]]
        groups += f'<div class="card"><h3><a href="{u(o["slug"] + "/")}">{o["city"]} office</a></h3><p>{e(o["street"])}, {o["locality"]}, NC {o["zip"]}<br><a href="tel:{o["phone_e164"]}">{o["phone"]}</a></p><ul class="pill-list">' + \
            "".join(f'<li><a href="{u(county_slug(c) + "/")}">{c["name"]} County</a></li>' for c in cs) + "</ul></div>"
    body = page_hero("Bail bond locations and counties we serve",
                     f"{N} has offices in Raleigh, Durham and Wilson and writes bonds across North Carolina. Pick a county for the jail address, clerk's phone number and how to post bond there.",
                     "Serving North Carolina · Open 24/7", bg="raleigh") + f"""
<section class="section"><div class="wrap"><div class="grid c3">{groups}</div>
<p style="margin-top:22px">Don't see your county? North Carolina licenses bail agents to write bonds in every county, and we do. <a href="{TEL}">Call {PHONE}</a> and tell us where the person is being held.</p>
</div></section>
"""
    shell("service-areas/", "Bail Bond Locations & Counties Served | All In One Bail Bonds NC",
          f"Offices in Raleigh, Durham and Wilson. 24/7 bail bonds in Wake, Durham, Wilson, Johnston, Harnett and surrounding NC counties. Call {PHONE}.",
          body, crumbs=[("Locations", "service-areas/")], ld=[office_ld(o) for o in OFFICES])


# ------------------------------------------------------------------ guides
def how_bail_works():
    faqs = [FAQ_MORE[0], FAQ_MORE[1], FAQ_MORE[2], FAQ_CORE[5], FAQ_CORE[2]]
    body = page_hero("How bail works in North Carolina",
                     "A plain-language walk through what happens after an arrest in NC: who sets the bond, the kinds of release, what a bail bondsman does and what the cosigner agrees to.",
                     "Guide · Updated November 2026", bg="signing") + f"""
<section class="section"><div class="wrap prose">
<h2>The short version</h2>
<p>After an arrest, a court official decides the conditions for release until the case is over. If the condition is a <strong>secured bond</strong>, money or property has to back it. A licensed bail bondsman can post that bond for a fee called the premium, which North Carolina caps at 15% of the bond amount. The person is released and must go to every court date.</p>

<h2>Step 1: The arrest and the magistrate</h2>
<p>After booking, the person is taken before a magistrate, who sets the conditions of pretrial release in most cases. In a few situations the law says a judge has to set them instead, and the person can be held for up to 48 hours until a judge is available. That applies to domestic violence charges and to certain serious felonies and new charges picked up while already on pretrial release.</p>

<h2>Step 2: The kinds of release</h2>
<p>North Carolina's pretrial release statute (G.S. 15A-534) lists the options a court can use:</p>
<ul>
<li><strong>Unsecured bond.</strong> No money up front. The person owes the amount only if they miss court.</li>
<li><strong>Custody release.</strong> The person is released into the supervision of a named person or organization.</li>
<li><strong>Secured bond.</strong> The bond must be backed by a cash deposit of the full amount, a mortgage on property, or a licensed bail bondsman acting as surety.</li>
<li><strong>House arrest with electronic monitoring</strong>, which also requires a secured bond.</li>
</ul>
<p class="note"><strong>Changed December 1, 2025:</strong> a written promise to appear is no longer a release option in North Carolina. The same law requires a secured bond or monitored house arrest for defendants with three or more convictions for Class 1 misdemeanors or higher in the last 10 years, and it tightens release for charges the statute defines as violent offenses.</p>

<h2>Step 3: Posting a secured bond</h2>
<p>You have three ways to satisfy a secured bond: pay the full amount in cash to the court, pledge property, or hire a bail bondsman. Most families use a bondsman because they do not have the full amount on hand. With a bondsman you pay the premium, and the bondsman guarantees the full bond to the court.</p>
<p>See <a href="{u('bail-bond-cost-nc/')}">what a bail bond costs in NC</a> for the numbers.</p>

<h2>Step 4: The paperwork</h2>
<p>The cosigner signs an agreement taking responsibility for the defendant showing up in court. For larger bonds the bondsman may ask for collateral. NC law requires a written receipt describing any collateral, and requires it to be returned within 15 days after the bondsman's liability on the bond finally ends.</p>

<h2>Step 5: Release, and what comes after</h2>
<p>The bondsman posts the bond with the jail and the jail processes the release. From then on the most important thing is simple: <strong>go to every court date</strong>. When the case ends, the bond is discharged. The premium is not refunded, because it paid for the service.</p>
<p>If a court date is missed, call your bondsman immediately. See <a href="{u('failure-to-appear-bonds/')}">what happens after a missed court date</a>.</p>

<h2>Common questions</h2>
{faq_html(faqs)}
<p class="note gov">This guide is general information about North Carolina's bail process, not legal advice. For advice about a specific case, talk to a licensed attorney. Statutes referenced: N.C. Gen. Stat. §§ 15A-533, 15A-534, 15A-534.1, 58-71-95 and 58-71-100.</p>
</div></section>
"""
    shell("how-bail-works-nc/", "How Bail Works in North Carolina (2026) | All In One",
          "How bail works in NC, step by step: who sets the bond, secured vs unsecured bonds, the 15% premium cap, the cosigner's role and the 2025 law changes.",
          body, crumbs=[("How bail works", "how-bail-works-nc/")], ld=[faq_ld(faqs)])


def cost():
    faqs = [FAQ_CORE[0], FAQ_CORE[2], FAQ_CORE[3],
            ("Can a bondsman charge extra fees?", "No. Under N.C. Gen. Stat. § 58-71-95 a bail bondsman may not accept anything of value except the premium, which is capped at 15%, and collateral. There are no lawful application, travel or processing fees on top."),
            ("What is collateral, and when do I get it back?", "Collateral is property or money pledged to protect the bondsman if the defendant does not go to court. Not every bond needs it. The bondsman must give you a written receipt describing it and must return it within 15 days after liability on the bond finally ends."),
            ("If the judge lowers the bond later, do I get part of the premium back?", "No. North Carolina law says the surety is not required to return any portion of the premium when a bond is reduced after it has been posted.")]
    body = page_hero("How much does a bail bond cost in North Carolina?",
                     "State law caps the bail bond premium at 15% of the bond amount. Slide to your bond amount to see the most a bondsman can charge, then call us for the exact cost.",
                     "Cost guide · NC 15% cap", bg="desk") + f"""
<section class="section"><div class="wrap two">
<div class="prose">
<h2>The 15% rule</h2>
<p>In North Carolina the fee for a bail bond is called the <strong>premium</strong>. Under N.C. Gen. Stat. § 58-71-95 it "shall not exceed fifteen percent (15%) of the face amount of the bond." On a $5,000 bond, the premium can be no more than $750.</p>
<p>The same statute says a bondsman may not accept anything else of value from you except collateral. That means no application fees, travel fees or processing fees.</p>
{cost_examples()}
<h2>What else to expect</h2>
<ul>
<li><strong>Collateral.</strong> Larger bonds may need property or money pledged as security. You get a written receipt, and it comes back within 15 days after the bond's liability finally ends.</li>
<li><strong>Payment arrangements.</strong> {PAY}. Any part of the premium paid after release goes into a signed written agreement with dates and amounts. <a href="{u('payment-plans/')}">How payment arrangements work</a>.</li>
<li><strong>No refund of the premium.</strong> The premium pays for the service of guaranteeing the bond, so it is not returned when the case ends.</li>
</ul>
</div>
<div>
<div class="sticky">{calc_html(5000, count=True, heading="Bail bond cost calculator")}</div>
</div>
</div></section>
<section class="section alt"><div class="wrap">
<h2>Cost questions</h2>
{faq_html(faqs)}
<p class="note gov">General information, not legal advice. Statutes referenced: N.C. Gen. Stat. §§ 58-71-95, 58-71-100, 58-71-16 and 58-71-167.</p>
</div></section>
"""
    shell("bail-bond-cost-nc/", "How Much Does a Bail Bond Cost in NC? 15% Rule + Calculator",
          "NC law caps the bail bond premium at 15% of the bond. See what a $1,000 to $50,000 bond costs, what collateral is, and whether you get money back.",
          body, crumbs=[("Cost", "bail-bond-cost-nc/")], ld=[faq_ld(faqs)])


def payment_plans():
    faqs = [FAQ_CORE[3],
            ("Does everyone qualify for a payment arrangement?", "No. It depends on the size of the bond, the charge, and the cosigner's situation. Call us and we will tell you honestly what we can do for your bond."),
            ("What has to be in the written agreement?", "North Carolina law (G.S. 58-71-167) requires the agreement to state the amount of premium still owed at release and the schedule: every payment date and the amount due on each date. It must be signed and dated by the defendant and the bondsman, and you are entitled to a copy."),
            ("What happens if a payment is missed?", "Call us before the due date if you see a problem coming. Staying in touch matters. Under NC law, willfully failing to pay the agreed premium is one of the reasons a bondsman is allowed to surrender a defendant back to custody.")]
    body = page_hero("Bail bond payment arrangements",
                     f"{PAY}. Here is how they work in North Carolina and what the law requires, so there are no surprises.",
                     "Payments", bg="signing") + f"""
<section class="section"><div class="wrap prose">
<h2>How a payment arrangement works</h2>
<p>If you cannot pay the whole premium at once, ask us about a payment arrangement when you call. If one is available for your bond, part of the premium is paid up front and the rest on a schedule you agree to.</p>
<h2>It has to be in writing</h2>
<p>North Carolina law protects you here. When any part of the premium is paid after the defendant is released, the bondsman must put the arrangement in a written memorandum that lists the amount still owed and each payment date and amount. Both sides sign and date it, and you get a copy.</p>
<h2>What we need from you</h2>
<ul>
<li>A cosigner with a steady address and a way to reach them</li>
<li>Honest information about the charge and any earlier missed court dates</li>
<li>Payments on the dates in the agreement, and a call if something changes</li>
</ul>
<p>{call_btn("btn btn-gold", "Ask about payment options", track="call-payments")}</p>
<h2>Payment questions</h2>
{faq_html(faqs)}
<p class="note gov">General information, not legal advice. Statutes referenced: N.C. Gen. Stat. §§ 58-71-167 and 58-71-20.</p>
</div></section>
"""
    shell("payment-plans/", "Bail Bond Payment Arrangements in NC | All In One Bail Bonds",
          f"Can't pay the whole premium at once? {PAY}. How bail bond payment arrangements work in North Carolina. Call {PHONE}, 24/7.",
          body, crumbs=[("Payment arrangements", "payment-plans/")], ld=[faq_ld(faqs)])


CHARGE_COPY = {
    "dwi-bail-bonds": {
        "bg": "highway",
        "h1": "DWI and DUI bail bonds in North Carolina",
        "title": "DWI / DUI Bail Bonds in NC | All In One Bail Bonds",
        "desc": f"Arrested for DWI in Raleigh, Durham or Wilson? What happens at the magistrate, how the bond is set and how to get released. Call {PHONE}, 24/7.",
        "lede": "A DWI arrest usually happens late at night. We answer at any hour, find out the bond and tell you what it will cost.",
        "sections": [
            ("What happens after a DWI arrest", "After testing and booking, the person goes before a magistrate, who sets the conditions of release. North Carolina calls the charge driving while impaired (DWI); people often search for DUI, and it means the same thing here."),
            ("Why there can be a wait", "In an impaired-driving case the magistrate can order the person held until they are no longer impaired or until a sober, responsible adult agrees to take responsibility for them. That hold is separate from the bond. We can get the paperwork ready so the bond is posted as soon as the jail will accept it."),
            ("How we help", "Call us with the person's name and the county. We confirm the bond amount, explain the premium and any collateral, and post the bond with the jail. We cannot give legal advice about the DWI charge itself or the license consequences; a licensed attorney can."),
        ],
        "faqs": [("Is DUI different from DWI in North Carolina?", "No. North Carolina's charge is driving while impaired (DWI). DUI is the term many other states use, and people use both for the same offense here."),
                 ("Can I pick the person up myself?", "Often a sober, responsible adult is exactly what the magistrate wants to see. Call us and we will tell you what the jail is asking for in this case."),
                 FAQ_CORE[0], FAQ_CORE[4]],
    },
    "felony-bail-bonds": {
        "bg": "desk",
        "h1": "Felony bail bonds in North Carolina",
        "title": "Felony Bail Bonds in NC | All In One Bail Bonds",
        "desc": f"Felony bonds are larger and some must be set by a judge. How felony bail works in NC since the 2023 and 2025 law changes. Call {PHONE}, 24/7.",
        "lede": "Felony bonds are larger, and for some charges only a judge can set release conditions. We explain where the case stands and what it will take to post the bond.",
        "sections": [
            ("Who sets a felony bond", "A magistrate sets conditions for many felony charges. For a list of serious felonies, and for new charges picked up while a person is already on pretrial release, a judge must set the conditions. The person can be held up to 48 hours until a judge acts."),
            ("What changed on December 1, 2025", "For charges the statute defines as violent offenses, the law now starts from a presumption against release, and a judge who does allow release must order a secured bond or house arrest with electronic monitoring. Defendants with three or more convictions for Class 1 misdemeanors or higher in the past 10 years must also get a secured bond or monitored house arrest."),
            ("Collateral on larger bonds", "A larger bond may need collateral, such as property. You get a written receipt describing it, and NC law requires it to be returned within 15 days after liability on the bond finally ends."),
        ],
        "faqs": [("Why hasn't a bond been set yet?", "If the charge is one a judge must handle, the magistrate cannot set the bond. The person waits for a judge, up to 48 hours. Call us and we will find out which situation applies."),
                 ("What if no bond is allowed?", "For some charges a judge can decide that no release conditions are enough. A bondsman cannot change that. An attorney can ask the court to review it."),
                 FAQ_CORE[0], FAQ_CORE[3]],
    },
    "misdemeanor-bail-bonds": {
        "bg": "night-call",
        "h1": "Misdemeanor bail bonds in North Carolina",
        "title": "Misdemeanor Bail Bonds in NC | All In One Bail Bonds",
        "desc": f"Fast help with misdemeanor bonds in Wake, Durham and Wilson counties. What they cost under NC's 15% cap and how to post one. Call {PHONE}, 24/7.",
        "lede": "Most misdemeanor bonds are small, and many can be arranged in a single phone call. Tell us the name and the county and we take it from there.",
        "sections": [
            ("What to expect", "A magistrate usually sets the release conditions shortly after arrest. If the condition is a secured bond, you can pay the full amount to the court in cash or have a bondsman post it for a premium of no more than 15%."),
            ("Small bonds still matter", "A night in jail can cost someone a job. We treat a $500 bond with the same urgency as a $50,000 one."),
            ("Since December 1, 2025", "A written promise to appear is no longer a release option in North Carolina, and people with three or more convictions for Class 1 misdemeanors or higher in the past 10 years must now get a secured bond or monitored house arrest."),
        ],
        "faqs": [("What would a $1,000 bond cost me?", "No more than $150. North Carolina caps the premium at 15% of the bond amount."),
                 FAQ_MORE[4], FAQ_CORE[4]],
    },
    "domestic-violence-bail-bonds": {
        "bg": "night-call",
        "h1": "Domestic violence bail bonds in North Carolina",
        "title": "Domestic Violence Bonds NC: 48-Hour Rule | All In One",
        "desc": f"In NC a judge, not a magistrate, sets release conditions in domestic violence cases, which can mean a wait of up to 48 hours. Call {PHONE}, 24/7.",
        "lede": "In a domestic violence case a judge sets the conditions of release, not a magistrate. That is why families are often told there is no bond yet.",
        "sections": [
            ("The 48-hour rule", "Under N.C. Gen. Stat. § 15A-534.1, a judge decides the release conditions in domestic violence cases. The person can be held for up to 48 hours after arrest until a judge does. If no judge has acted within 48 hours, a magistrate sets the conditions."),
            ("Conditions that come with release", "The court can add conditions such as staying away from the other person or from a home, school or workplace. Breaking a condition can lead to a new arrest. Read the release order carefully and follow it exactly."),
            ("How we help", "Call us as soon as you know about the arrest. We track when the bond is set and have the paperwork ready, so the bond can be posted as soon as there is one."),
        ],
        "faqs": [("Why can't you post a bond right now?", "Until a judge (or, after 48 hours, a magistrate) sets the conditions, there is no bond to post. We can get everything ready in the meantime."),
                 ("Does the 48 hours mean they will be held for two full days?", "Not necessarily. 48 hours is the maximum wait for a judge. If court is in session sooner, the conditions can be set sooner."),
                 FAQ_CORE[0]],
    },
    "failure-to-appear-bonds": {
        "bg": "desk",
        "h1": "Missed court? Bonds after a failure to appear",
        "title": "Missed Court in NC? Failure to Appear Bonds | All In One",
        "desc": f"Missed a court date in North Carolina? What an order for arrest means, what happens to the bond and how to handle it. Call {PHONE}, 24/7.",
        "lede": "A missed court date does not fix itself. The sooner it is dealt with, the more options there are.",
        "sections": [
            ("What happens when court is missed", "The judge can issue an order for arrest and begin forfeiting the bond that was posted. The cosigner on that bond can end up responsible for the full amount."),
            ("If we wrote your bond", "Call us right away, even if the date was missed by accident. Do not wait to be picked up. We will tell you where things stand and what needs to happen next."),
            ("If you need a new bond", "After an arrest on an order for arrest, new release conditions are set, and courts generally set a higher secured bond after a missed date. Call us with the county and we will find out the amount."),
        ],
        "faqs": [("How do I check my court date?", f"Use the <a href=\"{STATE['court_date_lookup']['url']}\" rel=\"noopener nofollow\">NC eCourts portal</a> or call the Clerk of Superior Court in the county where the case is. Our <a href=\"{u('service-areas/')}\">county pages</a> list each clerk's phone number."),
                 ("Can I just turn myself in?", "People do, and having a bondsman lined up beforehand can shorten the time in custody. Call us first so we can explain how it would work in your county. For advice about the case itself, talk to a licensed attorney."),
                 FAQ_CORE[5]],
    },
}


def charge_pages():
    for slug, name, _ in CHARGES:
        c = CHARGE_COPY[slug]
        secs = "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in c["sections"])
        body = page_hero(c["h1"], c["lede"], "Open 24/7", bg=c.get("bg", "night-call")) + f"""
<section class="section"><div class="wrap two">
<div class="prose">{secs}
<h2>What it costs</h2>
<p>North Carolina caps the bail bond premium at 15% of the bond amount. {PAY}. <a href="{u('bail-bond-cost-nc/')}">See the cost calculator</a>.</p>
</div>
<div><div class="card"><h3>Have this ready when you call</h3><ol>{"".join(f"<li>{x}</li>" for x in READY)}</ol>{call_btn("btn btn-gold", track="call-" + slug)}</div></div>
</div></section>
<section class="section alt"><div class="wrap">
<h2>Questions</h2>
{faq_html(c["faqs"])}
<p class="note gov">General information about North Carolina's bail process, not legal advice. For advice about a specific case, talk to a licensed attorney. We cannot recommend one; NC law does not allow bail agents to.</p>
</div></section>
"""
        shell(slug + "/", c["title"], c["desc"], body, crumbs=[(name, slug + "/")],
              ld=[service_ld(name, c["desc"]), faq_ld(c["faqs"])])


JAIL_GUIDES = [("Wake", "wake-county-jail"), ("Durham", "durham-county-jail"), ("Wilson", "wilson-county-jail")]


def jail_guides():
    for n, slug in JAIL_GUIDES:
        c = next(x for x in COUNTIES if x["name"] == n)
        j, j2, ch = c["jail"], c.get("jail2"), c["courthouse"]
        o = office_by_city(S["county_office"][n])
        lookup = c["inmate_lookup_url"]
        lk_label = LOOKUP_LABEL.get(n, f"{n} County inmate lookup (official)")
        path = f"jail-guides/{slug}/"
        find = (f'<a href="{e(lookup)}" rel="noopener nofollow">{lk_label}</a>' if lookup else
                "The county does not publish a web inmate lookup that we could find, so the phone is the fastest way")
        two = (f"<p>{n} County uses two facilities: the <strong>{e(j['name'])}</strong> at {e(j['address'])}, and the <strong>{e(j2['name'])}</strong> at {e(j2['address'])} in downtown {j2['city']}. Ask which one the person is in before you drive.</p>" if j2 else "")
        faqs = [
            (f"What is the address of the {n} County jail?", f"The {j['name']} is at {j['address']}, {j['city']}, NC{(' ' + j['zip']) if j['zip'] else ''}." + (f" The {j2['name']} is at {j2['address']}, {j2['city']}, NC {j2['zip']}." if j2 else "")),
            (f"How do I find out if someone is in the {n} County jail?", (f"Use the {find}, or call" if lookup else "Call") + f" {j['phone']}" + (f" ({PHONE_LABEL[n]})" if n in PHONE_LABEL else "") + f". You can also call us at {PHONE} and we will check."),
            ("How long does release take after the bond is posted?", "That is up to the jail. Release processing varies with how busy the facility is. No bondsman can promise a release time."),
            FAQ_CORE[0],
        ]
        body = page_hero(f"How to bail someone out of the {n} County jail",
                         f"A step-by-step guide for families: how to confirm someone is in the {j['name']}, find the bond amount and get the bond posted.",
                         f"Jail guide · {j['city']}, NC", bg="highway") + f"""
<section class="section"><div class="wrap two">
<div class="prose">
{GOV_NOTE}
{two}
<h2>Step 1: Confirm where they are</h2>
<p>{("Start with the " + find) if lookup else find}. You can also call {j['phone']}{(' (' + PHONE_LABEL[n] + ')') if n in PHONE_LABEL else ''}. Have the person's full legal name and date of birth ready.</p>
<h2>Step 2: Find out the bond and the conditions</h2>
<p>A magistrate sets release conditions soon after most arrests. Domestic violence charges and certain serious felonies must wait for a judge, which can take up to 48 hours. If the condition is a secured bond, a bondsman can post it.</p>
<h2>Step 3: Call a bondsman</h2>
<p>Call {N} at <a href="{TEL}">{PHONE}</a>. We confirm the bond, tell you the premium (never more than 15% of the bond in North Carolina) and explain what the cosigner signs.</p>
<h2>Step 4: Paperwork and payment</h2>
<p>Call first and we will tell you what can be done by phone or electronically and what needs a signature in person at our <a href="{u(o['slug'] + '/')}">{o['city']} office</a>. {PAY}.</p>
<h2>Step 5: We post the bond</h2>
<p>A licensed agent posts the bond with the jail. The jail then processes the release on its own schedule.</p>
<h2>Step 6: Court</h2>
<p>The {e(ch['name'])} is at {e(ch['address'])}, {ch['city']}. Check the date on the <a href="{STATE['court_date_lookup']['url']}" rel="noopener nofollow">NC eCourts portal</a> or call the Clerk of Superior Court at {ch['clerk_phone']}. Go to every court date.</p>
</div>
<div>
<table class="facts">
<tr><th>Jail</th><td>{jail_cell(j, PHONE_LABEL.get(n))}</td></tr>
{f'<tr><th>Second facility</th><td>{jail_cell(j2, show_phone=n not in JAIL2_NO_PHONE)}</td></tr>' if j2 else ''}
<tr><th>Courthouse</th><td>{e(ch['name'])}<br>{e(ch['address'])}, {ch['city']}, NC {ch['zip']}</td></tr>
<tr><th>Clerk of Court</th><td>{ch['clerk_phone']}</td></tr>
<tr><th>Victim notification</th><td><a href="{STATE['vinelink']['url']}" rel="noopener nofollow">VINELink North Carolina</a></td></tr>
<tr><th>More on this county</th><td><a href="{u(county_slug(c) + '/')}">{n} County bail bonds</a></td></tr>
</table>
<div class="card" style="margin-top:16px"><h3>Need help right now?</h3><p>We answer 24 hours a day.</p>{call_btn("btn btn-gold", track="call-jail-" + n.lower())}</div>
</div>
</div></section>
<section class="section alt"><div class="wrap"><h2>{n} County jail questions</h2>{faq_html(faqs)}</div></section>
"""
        shell(path, f"How to Bail Someone Out of {n} County Jail | {j['city']}, NC",
              f"{n} County jail guide: address, phone, how to find an inmate, how the bond is set and how to post it. 24/7 bail bonds, call {PHONE}.",
              body, crumbs=[("Locations", "service-areas/"), (f"{n} County jail guide", path)], ld=[faq_ld(faqs)])


def faq_page():
    faqs = FAQ_CORE + FAQ_MORE
    body = page_hero("Bail bond questions and answers", "Straight answers to what families ask us most, written for North Carolina.", "FAQ", bg="night-call") + f"""
<section class="section"><div class="wrap prose">{faq_html(faqs)}
<p class="note gov">General information, not legal advice. For advice about a specific case, talk to a licensed attorney.</p></div></section>
"""
    shell("faq/", "Bail Bond FAQ for North Carolina | All In One Bail Bonds",
          "Answers about bail in NC: cost and the 15% cap, payment arrangements, cosigners, secured bonds, release times and the 2025 law changes.",
          body, crumbs=[("FAQ", "faq/")], ld=[faq_ld(faqs)])


def reviews():
    cards = "".join(
        f'<div class="card office"><h3>{o["city"]}</h3><p class="rating"><span class="stars" aria-hidden="true">★★★★★</span> {o["google_rating"]} · {o["google_reviews"]} Google reviews</p>'
        f'<div class="acts"><a class="btn btn-line btn-sm" href="{maps_url(o["maps_query"])}" rel="noopener">Read {o["city"]} reviews on Google</a></div></div>' for o in OFFICES)
    body = page_hero(f"{TOTAL_REVIEWS} five-star Google reviews",
                     f"Every one of our three offices holds a 5.0 rating on Google. Counts are as of {S['reviews_as_of']}; follow the links to read what families wrote in their own words.",
                     "Reviews", bg="reunion") + f"""
<section class="section"><div class="wrap">
<div class="grid c3">{cards}</div>
<div class="prose" style="margin-top:28px">
<h2>Did we help your family?</h2>
<p>A short, honest Google review helps the next family find someone they can trust at a hard moment. Pick the office that helped you from the links above. We read every review.</p>
</div></div></section>
"""
    shell("reviews/", f"5.0 Stars from {TOTAL_REVIEWS} Google Reviews | All In One Bail Bonds",
          f"All In One Bail Bonds holds a 5.0 Google rating at all three offices: Raleigh ({OFFICES[0]['google_reviews']}), Durham ({OFFICES[1]['google_reviews']}) and Wilson ({OFFICES[2]['google_reviews']}).",
          body, crumbs=[("Reviews", "reviews/")])


def about():
    lic = f"<tr><th>NC license</th><td>#{e(AG['license_number'])}</td></tr>" if AG["license_number"] else ""
    person = {"@type": "Person", "@id": absu("about/#agent"), "name": AG["name"], "jobTitle": "Bail agent",
              "worksFor": {"@id": absu("#org")}, "url": absu("about/")}
    body = page_hero(f"About {N}", "A North Carolina bail bond agency with three offices and one promise: a real person answers, day or night.", "About us", bg="desk") + f"""
<section class="section"><div class="wrap two">
<div class="prose">
<h2>Helping every step of the way</h2>
<p>"I know when a loved one is in jail it is a trying experience, not only for the defendant, but the family as well. Our friendly, knowledgeable staff will be happy to answer any questions you may have. We want to earn your trust, we take pride in the services we provide, and we look forward to handling your jail release needs."</p>
<p><strong>{AG['name']}</strong>, {AG['title']}</p>
<h2>What we do</h2>
<p>{N} provides fast, affordable and discreet bail bond service in Raleigh and throughout Wake County, Durham County, Wilson County and the surrounding counties, and writes bonds across North Carolina. Our agents are available 24 hours a day, 365 days a year, so people can go back to their jobs and families while their case moves through court.</p>
<h2>How we work</h2>
<ul>
<li><strong>We answer.</strong> Day, night, weekend or holiday.</li>
<li><strong>We explain before you sign.</strong> You hear the premium and any collateral up front.</li>
<li><strong>We follow the rules.</strong> North Carolina caps the premium at 15%, and every payment arrangement goes in writing with a copy for you.</li>
<li><strong>We keep it discreet.</strong> Your family's business stays your family's business.</li>
</ul>
</div>
<div>
<table class="facts">
<tr><th>Bail agent</th><td>{AG['name']}</td></tr>
{lic}
<tr><th>Offices</th><td>Raleigh, Durham, Wilson</td></tr>
<tr><th>Hours</th><td>24 hours, every day</td></tr>
<tr><th>Google rating</th><td>5.0 from {TOTAL_REVIEWS} reviews ({S['reviews_as_of']})</td></tr>
<tr><th>Regulator</th><td><a href="{STATE['ncdoi_bail']['url']}" rel="noopener nofollow">NC Department of Insurance, Bail Bond Regulatory Division</a></td></tr>
</table>
<div class="figure" style="margin-top:16px">{pic("desk", "The All In One Bail Bonds desk, ready at night")}</div>
</div>
</div></section>
"""
    shell("about/", "About All In One Bail Bonds | NC Licensed Bail Agents",
          f"All In One Bail Bonds is a North Carolina bail agency led by {AG['name']}, with offices in Raleigh, Durham and Wilson and a 5.0 Google rating.",
          body, crumbs=[("About", "about/")], ld=[person])


def form_html(lang="en"):
    es = lang == "es"
    t = (lambda a, b: b if es else a)
    sms = f'<button class="btn btn-line" id="bond-sms" type="button">{t("Send as a text message instead", "Enviar por mensaje de texto")}</button>' if S["sms_enabled"] else ""
    counties = "".join(f"<option>{c['name']} County</option>" for c in COUNTIES)
    return f"""<form class="form" id="bond-form" data-email="{S['email']}" data-sms="{S['phone_e164']}" data-lang="{lang}">
<h2 style="font-size:1.25rem">{t("Start a bond request", "Solicite una fianza")}</h2>
<small>{t("For the fastest help, call. This form opens an email (or text) in your own app; nothing is stored on this website.", "Para ayuda inmediata, llame. Este formulario abre un correo (o mensaje) en su propio teléfono; no se guarda nada en este sitio.")}</small>
<label for="f-name">{t("Your name", "Su nombre")}</label><input id="f-name" name="yourname" autocomplete="name" required>
<label for="f-phone">{t("Your phone", "Su teléfono")}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required>
<label for="f-def">{t("Name of the person in custody", "Nombre de la persona detenida")}</label><input id="f-def" name="defendant">
<label for="f-county">{t("Jail or county", "Cárcel o condado")}</label><select id="f-county" name="county"><option value="">{t("Not sure", "No estoy seguro")}</option>{counties}<option>{t("Another NC county", "Otro condado de NC")}</option></select>
<label for="f-amt">{t("Bond amount, if known", "Monto de la fianza, si lo sabe")}</label><input id="f-amt" name="amount" inputmode="decimal">
<label for="f-notes">{t("Anything else we should know", "Algo más que debamos saber")}</label><textarea id="f-notes" name="notes"></textarea>
<button class="btn btn-gold" type="submit">{t("Send request by email", "Enviar por correo")}</button>
{sms}
</form>"""


def contact():
    body = page_hero("Contact All In One Bail Bonds", f"The fastest way to reach us is to call {PHONE}. A licensed bail agent answers 24 hours a day.", "Contact · Open 24/7", bg="night-call") + f"""
<section class="section"><div class="wrap two">
<div>
<div class="grid">{"".join(office_card(o) for o in OFFICES)}</div>
<p style="margin-top:16px">Email: <a href="mailto:{S['email']}">{S['email']}</a></p>
</div>
<div>{form_html()}</div>
</div></section>
"""
    shell("contact/", "Contact All In One Bail Bonds | Call 24/7: " + PHONE,
          f"Call {PHONE} any time. Offices at 6104 Westgate Rd in Raleigh, 3326 Guess Rd in Durham and 2509 Nash St N in Wilson, NC.",
          body, crumbs=[("Contact", "contact/")], ld=[office_ld(o) for o in OFFICES])


def fianzas():
    if not S["spanish_enabled"]:
        return
    faqs = [
        ("¿Cuánto cuesta una fianza en Carolina del Norte?", "La ley de Carolina del Norte limita la prima de una fianza al 15% del monto de la fianza (N.C. Gen. Stat. § 58-71-95). En una fianza de $5,000, la prima no puede ser más de $750. Llámenos para saber el costo exacto."),
        ("¿Me devuelven la prima cuando termina el caso?", "No. La prima es el pago por el servicio del fiador y no se devuelve. La garantía (colateral) sí se devuelve dentro de los 15 días después de que termina la responsabilidad del fiador."),
        ("¿Puedo pagar a plazos?", "Aceptamos algunos arreglos de pago. Depende de la fianza y de su situación. Todo arreglo de pago se pone por escrito, firmado por ambas partes, y usted recibe una copia."),
        ("¿Cuánto tarda en salir la persona?", "Depende de la cárcel. Después de que presentamos la fianza, la cárcel procesa la salida, y ese tiempo no lo controla ningún fiador."),
        ("¿Están abiertos de noche y los fines de semana?", f"Sí. Contestamos el {PHONE} las 24 horas, todos los días del año."),
    ]
    steps = [("Llámenos", "Díganos el nombre completo de la persona, su fecha de nacimiento si la sabe, y en qué condado está detenida."),
             ("Le explicamos el costo", "Le decimos la prima y si hace falta garantía antes de que firme cualquier documento."),
             ("Presentamos la fianza", "Un agente con licencia presenta la fianza en la cárcel, y la cárcel procesa la salida.")]
    body = f"""
<section class="page-hero has-bg"><div class="bg">{pic("reunion", "", eager=True, sizes="100vw")}</div><div class="wrap">{{{{CRUMBS}}}}<span class="live"><i></i>Abierto 24 horas</span>
<h1>Fianzas en Raleigh, Durham y Wilson, Carolina del Norte</h1>
<p class="lede">Cuando un ser querido está en la cárcel, usted necesita una respuesta clara y rápida. Llame a {N} a cualquier hora y un agente de fianzas con licencia le explica el costo y los pasos a seguir.</p>
<div class="cta">{call_btn(label="Llame al " + PHONE, track="call-es")}{text_btn(label="Envíe un mensaje")}</div></div></section>
<section class="section"><div class="wrap">
<h2>Cómo funciona</h2>
<div class="grid c3">{"".join(f'<div class="card rv">{tile(["phone", "money", "home"][i - 1])}<h3>{i}. {t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps, 1))}</div>
</div></section>
<section class="section alt"><div class="wrap two">
<div class="prose">
<h2>Lo que cuesta una fianza</h2>
<p>En Carolina del Norte la prima no puede ser más del <strong>15% del monto de la fianza</strong>. El fiador puede pedir una garantía en fianzas grandes, pero no puede cobrar cargos adicionales de solicitud o de trámite.</p>
<h2>Nuestras oficinas</h2>
<ul>{"".join(f'<li><strong>{o["city"]}:</strong> {e(o["street"])}, {o["locality"]}, NC {o["zip"]}. <a href="tel:{o["phone_e164"]}">{o["phone"]}</a></li>' for o in OFFICES)}</ul>
<h2>Preguntas frecuentes</h2>
{faq_html(faqs)}
<p class="note gov">Somos una agencia privada de fianzas. No somos abogados, no damos consejo legal y no estamos afiliados con ninguna corte, cárcel ni agencia del gobierno.</p>
</div>
<div>{form_html("es")}</div>
</div></section>
"""
    shell("fianzas/", "Fianzas en Raleigh, Durham y Wilson NC | Abierto 24 Horas",
          f"Fianzas en Carolina del Norte las 24 horas. Oficinas en Raleigh, Durham y Wilson. La prima no puede ser más del 15%. Llame al {PHONE}.",
          body, crumbs=[("Español", "fianzas/")], ld=[faq_ld(faqs)], lang="es")


def not_found():
    body = page_hero("Page not found", f"That page isn't here. If you need a bail bond right now, call {PHONE}.", "404") + f"""
<section class="section"><div class="wrap"><ul class="pill-list"><li><a href="{u('')}">Home</a></li><li><a href="{u('service-areas/')}">Locations</a></li><li><a href="{u('how-bail-works-nc/')}">How bail works</a></li><li><a href="{u('contact/')}">Contact</a></li></ul></div></section>"""
    shell("404.html", "Page not found | All In One Bail Bonds", "Page not found.", body)


def build_all():
    home(); office_pages(); service_areas(); county_pages(); how_bail_works(); cost(); payment_plans()
    charge_pages(); jail_guides(); faq_page(); reviews(); about(); contact(); fianzas(); not_found()
