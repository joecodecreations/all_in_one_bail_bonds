"""Full-page screenshots (desktop + mobile) with headless Chrome and Pillow.
    python3 tools/shots.py [--base http://localhost:8791/all_in_one_bail_bonds] [--pages home,faq]
Writes shots/<page>-desktop.png, -mobile.png (full page) and -mobile-fold.png (first screen)."""
import argparse, subprocess, tempfile
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
PAGES = {"home": "", "raleigh-office": "bail-bonds-raleigh-nc/", "wilson-office": "bail-bonds-wilson-nc/",
         "wake-county": "wake-county-bail-bonds/", "durham-county": "durham-county-bail-bonds/",
         "cost-calculator": "bail-bond-cost-nc/", "how-bail-works": "how-bail-works-nc/",
         "wake-jail-guide": "jail-guides/wake-county-jail/", "dwi": "dwi-bail-bonds/", "service-areas": "service-areas/",
         "faq": "faq/", "reviews": "reviews/", "about": "about/", "contact": "contact/", "fianzas": "fianzas/"}

def shot(url, out, w, h, mobile=False):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={max(w, 520)},{h}",
           "--virtual-time-budget=9000", f"--screenshot={out}"]
    if mobile:
        # Headless Chrome will not lay out narrower than ~500px, so frame the page at phone width and crop.
        frame = Path(tempfile.mkdtemp()) / "frame.html"
        frame.write_text(f'<body style="margin:0;background:#fff"><iframe src="{url}" style="border:0;width:{w}px;height:{h}px;display:block"></iframe>')
        cmd += ["--force-device-scale-factor=2", "--disable-web-security", "--allow-file-access-from-files"]
        url = frame.as_uri()
    subprocess.run(cmd + [url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    if mobile:
        im = Image.open(out); im.crop((0, 0, w * 2, im.size[1])).save(out)

def trim(path):
    """Cut the blank space below the footer (and the fixed mobile bar that sits at the window bottom)."""
    im = Image.open(path).convert("RGB"); W, H = im.size; px = im.load()
    white = lambda y: all(sum(px[x, y]) > 740 for x in range(0, W, max(1, W // 40)))
    y = H - 1
    while y > 0 and not white(y): y -= 1          # fixed action bar, if any
    if y < H * 0.5: return                        # page fills the window: nothing to trim
    while y > 0 and white(y): y -= 1
    if y > 200: im.crop((0, 0, W, y + 1)).save(path, optimize=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--base", default="http://localhost:8791/all_in_one_bail_bonds")
    ap.add_argument("--pages", default=""); ap.add_argument("--out", default=str(ROOT / "shots")); a = ap.parse_args()
    out = Path(a.out); out.mkdir(exist_ok=True)
    want = set(filter(None, a.pages.split(",")))
    for name, path in PAGES.items():
        if want and name not in want: continue
        url = a.base.rstrip("/") + "/" + path + "?shot"
        shot(url, out / f"{name}-desktop.png", 1440, 9000); trim(out / f"{name}-desktop.png")
        shot(url, out / f"{name}-mobile.png", 390, 9000, True); trim(out / f"{name}-mobile.png")
        shot(url, out / f"{name}-mobile-fold.png", 390, 844, True)
        print("shot", name)
if __name__ == "__main__": main()
