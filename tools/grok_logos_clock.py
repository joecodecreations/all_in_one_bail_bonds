"""25 clock-theme logo samples (round 3), after the owner liked #10 (24/7 clock with a check mark).
    python3 tools/grok_logos_clock.py [--jobs 7] [n ...]   -> media/grok/logos-r3/NN-slug_v1.jpg"""
import argparse, json, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import grok_images as g
g.OUT = g.ROOT / "media" / "grok" / "logos-r3"; g.OUT.mkdir(parents=True, exist_ok=True)
g.SESS = Path.home() / ".grok" / "sessions" / urllib.parse.quote(str(g.OUT), safe="")
BASE = ("A professional, original logo for a North Carolina bail bond company that is open around the clock. The company name must appear "
        "spelled exactly \"All In One Bail Bonds\" (All In One, then Bail Bonds), crisp, legible and correctly spelled. Clean flat vector style, "
        "centered on a plain white background, generous margin, print-ready, no mockup. The logo is built around a CLOCK. "
        "No handcuffs, no jail bars, no police badge, no shield, no sheriff star, no seal, no gavel. Concept: ")
C = [
 ("check-classic", "a round clock outline with tick marks whose hands form a bold check mark, with 24/7 under the clock and the name to the right; navy and bright azure blue. A refined version of a clock-and-check logo."),
 ("check-filled", "a solid navy circle clock face with a white check mark as the hands and small white tick marks, name to the right in bold navy and azure."),
 ("check-ring-gap", "a thin clock ring that opens at the top right where the check mark's long stroke breaks out of it, meaning breaking out to freedom, navy and azure, name to the right."),
 ("247-inside", "a clock face with 24/7 written inside it in bold numerals instead of hour marks, name below, navy and azure."),
 ("247-around", "the numbers 2, 4, 7 placed around a circular dial like hour marks with a check mark in the center, name to the right, navy and azure."),
 ("stopwatch", "a stopwatch with a check mark on its face, meaning fast response, name to the right, navy and azure."),
 ("alarm-clock", "a friendly round alarm clock with two bells and a check mark as its hands, name below, navy and azure."),
 ("moon-clock", "a clock face whose left half is a crescent moon and right half a small sun, meaning day and night, check-mark hands, name to the right, navy and azure."),
 ("phone-clock", "a phone handset curving around a clock face, meaning call any hour, name to the right, navy and azure."),
 ("minimal-line", "an ultra-minimal single-line clock icon: a circle and two hands in one continuous stroke ending in a check mark, lots of white space, name in a light modern sans-serif, navy only with one azure accent."),
 ("monogram-clock", "the letters A and 1 forming the hour and minute hands of a clock, name to the right, navy and azure."),
 ("o-is-clock", "a wordmark where the letter O in One is drawn as a small clock face with check-mark hands, Bail Bonds below, navy and azure."),
 ("badge-free-square", "a rounded square app-style icon containing a clock with check-mark hands, name to the right, navy square with azure check."),
 ("clock-24-ring", "a clock face surrounded by a thin ring of 24 small ticks, check-mark hands, the words Open 24/7 beneath in small caps, name to the right, navy and azure."),
 ("bold-geometric", "a bold geometric clock built from a thick circle and two chunky hands at the 10 and 2 positions forming a V for victory, name to the right in heavy sans-serif, navy and azure."),
 ("hourglass-clock", "a clock face with a tiny hourglass at the center instead of hands, meaning no waiting, name below, navy and azure."),
 ("arrow-clock", "a circular arrow going around like a refresh symbol forming a clock, with a check mark inside, name to the right, navy and azure."),
 ("sunrise-clock", "a half clock face rising from a horizon line like a sunrise with check-mark hands, name below, navy, azure and a touch of warm orange."),
 ("heart-clock", "a clock face whose hands form a small heart shape at the center, meaning families, name to the right, navy and azure."),
 ("house-clock", "a clock face set in the gable of a simple house outline, meaning home any hour, check-mark hands, name below, navy and azure."),
 ("signal-clock", "a clock face with three small signal waves coming off its top right, meaning always reachable, check-mark hands, name to the right, navy and azure."),
 ("stacked-247", "the characters 24/7 (two, four, slash, seven: all four characters must appear) set large and bold, with a small clock face sitting above the slash, the company name below, navy and azure."),
 ("retro-clock", "a mid-century retro style rounded wall clock with a soft cream face and check-mark hands, no star points and no rays, name in a confident retro sans-serif, navy, azure and cream."),
 ("gold-premium", "an elegant premium clock face with thin roman-numeral-free tick marks and check-mark hands, name in a classic serif, navy and soft gold."),
 ("green-go", "a clock face with check-mark hands, name to the right, deep navy and fresh green, meaning go, you are free to go home."),
]
g.JOBS = {f"{i:02d}-{s}": ("1:1", BASE + p) for i, (s, p) in enumerate(C, 1)}
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--jobs", type=int, default=7); ap.add_argument("nums", nargs="*", type=int); a = ap.parse_args()
    todo = [k for k in g.JOBS if not a.nums or int(k[:2]) in a.nums]
    with ThreadPoolExecutor(a.jobs) as ex: out = list(ex.map(lambda s: g.run(s, 1), todo))
    (g.OUT / "log.json").write_text(json.dumps(out, indent=1))
    for r in out: print(r["slug"], r["exit"], r["files"], r.get("error", ""))
