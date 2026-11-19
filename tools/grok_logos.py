"""25 logo samples with Grok Imagine (round 2, after the doorway mark was rejected).
    python3 tools/grok_logos.py [--jobs 6] [n ...]      -> media/grok/logos-r2/NN-slug.jpg"""
import argparse, json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import grok_images as g

g.OUT = g.ROOT / "media" / "grok" / "logos-r2"
g.OUT.mkdir(parents=True, exist_ok=True)
import urllib.parse
g.SESS = Path.home() / ".grok" / "sessions" / urllib.parse.quote(str(g.OUT), safe="")

BASE = ("A professional, original logo for a North Carolina bail bond company. The company name must appear spelled exactly "
        "\"All In One Bail Bonds\" (four words: All In One, then Bail Bonds), crisp and legible, correctly spelled. "
        "Clean flat vector style, centered on a plain white background, generous margin, print-ready, no mockup, no paper texture. "
        "Absolutely no handcuffs, no jail bars, no police badge, no shield, no sheriff star, no seal, no gavel, no doorway. Concept: ")
C = [
 ("bold-wordmark", "a bold modern wordmark: ALL IN ONE in heavy geometric sans-serif capitals, BAIL BONDS small and widely letter-spaced beneath, deep navy and bright royal blue, one sweeping gold underline."),
 ("a1-monogram", "an interlocking A and 1 monogram inside a rounded square, navy and gold, with the company name set to the right in a clean sans-serif."),
 ("three-rings", "three overlapping rings merging into one shape (all in one), blue gradient from navy to sky blue, company name below."),
 ("sunrise", "a half sun rising over a straight horizon line with rays, meaning a new day, navy and warm orange-gold, company name below in strong capitals."),
 ("key-a", "an old-fashioned key whose bow forms a letter A, navy and gold, company name beside it."),
 ("hands-house", "two open hands gently holding a small house, meaning family support, teal and navy, company name below."),
 ("bridge", "a simple arched bridge over a line of water, meaning getting back across, navy and sky blue, company name below."),
 ("north-star", "a four-point north star with a long glow, meaning guidance at night, navy and gold, company name below in elegant capitals."),
 ("rising-bird", "a stylized bird rising upward in flight made of three swooshes, meaning freedom and hope, royal blue and light blue, company name beside it."),
 ("clock-247", "a minimal clock face whose hands form a check mark, with 24/7 beneath it, navy and electric blue, company name to the right."),
 ("phone-bubble", "a phone handset inside a speech bubble, meaning we answer, navy and bright blue, company name to the right in rounded sans-serif."),
 ("hex-one", "a bold geometric hexagon emblem with a large numeral 1 cut into it, royal blue and navy, modern tech feel, company name below."),
 ("aio-stack", "a stacked lettermark AIO in chunky retro-modern letters, navy on cream with a thin gold outline, company name underneath."),
 ("script-gold", "an elegant gold brush-script All In One above navy spaced capitals BAIL BONDS, classic and premium, with a thin gold line between."),
 ("road-forward", "a road leading forward between two hills toward a small sun, meaning the path forward, deep blue and green, company name below."),
 ("lighthouse", "a slim lighthouse sending a beam of light across the dark, navy and warm yellow, company name beside it."),
 ("helping-hand", "one hand reaching down to clasp another hand, meaning a helping hand, two shades of blue, company name below."),
 ("infinity-one", "an infinity loop that turns into the numeral 1, blue gradient, company name to the right."),
 ("lit-window", "a small house at night with one warm lit window, meaning someone is waiting for you, navy and warm yellow, company name below."),
 ("nc-pin", "the outline of the state of North Carolina with a map pin, navy and gold, company name below with the words Statewide 24/7 in small type."),
 ("one-bars", "a numeral 1 built from three stacked bars joined together, black and bright blue, minimal and strong, company name to the right."),
 ("heart-home", "a heart shape that is also a house roof, meaning family first, navy and soft coral, company name below in friendly rounded letters."),
 ("arrow-forward", "three chevrons pointing right, getting brighter from navy to cyan, meaning moving forward, set to the left of a bold company name. No circles."),
 ("classic-banner", "a classic American sign-painter style wordmark: All In One in a bold flowing hand-lettered script, with Bail Bonds on a simple ribbon banner beneath it, navy, red and cream. No circle, no ring of text, no stars, nothing that looks like a seal or emblem."),
 ("luxe-serif", "an ultra-minimal luxury wordmark in a thin high-contrast serif with a small gold dot, black and gold, lots of white space."),
]
g.JOBS = {f"{i:02d}-{s}": ("1:1", BASE + p) for i, (s, p) in enumerate(C, 1)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--jobs", type=int, default=6); ap.add_argument("nums", nargs="*", type=int); a = ap.parse_args()
    todo = [k for k in g.JOBS if not a.nums or int(k[:2]) in a.nums]
    with ThreadPoolExecutor(a.jobs) as ex:
        out = list(ex.map(lambda s: g.run(s, 1), todo))
    (g.OUT / "log.json").write_text(json.dumps(out, indent=1))
    for r in out: print(r["slug"], r["exit"], r["secs"], r["files"], r.get("error", ""))
