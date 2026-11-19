"""Brand images from src/brand/mark.svg, rendered with headless Chrome:
logo PNGs (88/192/512), favicon.ico and the 1200x630 social share card.
    python3 tools/images.py      (needs Pillow and Google Chrome)"""
import subprocess, tempfile
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent; SRC = ROOT / "src"; IMG = SRC / "img"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MARK = (SRC / "brand" / "mark.svg").as_uri(); FONT = (SRC / "assets/fonts/jakarta-latin.woff2").as_uri()
SCENE = (IMG / "scenes" / "highway-1600.jpg").as_uri()

def render(html, out, w, h, transparent=False):
    f = Path(tempfile.mkdtemp()) / "x.html"; f.write_text(html)
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
           f"--window-size={w},{h}", f"--screenshot={out}", "--virtual-time-budget=1500"]
    if transparent: cmd.append("--default-background-color=00000000")
    subprocess.run(cmd + [f.as_uri()], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

render(f'<body style="margin:0;background:transparent"><img src="{MARK}" width="512" height="512" style="display:block">', IMG / "logo-512.png", 512, 512, True)
big = Image.open(IMG / "logo-512.png").convert("RGBA")
for s in (192, 88): big.resize((s, s), Image.LANCZOS).save(IMG / f"logo-{s}.png", optimize=True)
big.resize((64, 64), Image.LANCZOS).save(SRC / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
render(f'''<style>@font-face{{font-family:J;src:url({FONT})}}*{{margin:0}}body{{width:1200px;height:630px;font-family:J,Helvetica;color:#fff;
background:linear-gradient(90deg,rgba(6,17,31,.96) 35%,rgba(6,17,31,.45)),url({SCENE}) center/cover;position:relative}}
.k{{position:absolute;left:80px;top:78px;display:flex;align-items:center;gap:22px}}.k b{{font-size:44px;font-weight:800;letter-spacing:-1px;display:block}}
.k small{{display:block;color:#F2B33D;font-weight:700;font-size:17px;letter-spacing:8px;margin-top:6px}}
h1{{position:absolute;left:80px;top:230px;font-size:84px;font-weight:800;letter-spacing:-3px;line-height:1}}h1 em{{font-style:normal;color:#F2B33D}}
p{{position:absolute;left:80px;top:350px;font-size:30px;color:#d6e0f0}}.ph{{position:absolute;left:80px;top:440px;background:#F2B33D;color:#06111F;font-weight:800;font-size:40px;padding:18px 34px;border-radius:18px}}
.r{{position:absolute;left:520px;top:458px;font-size:26px;color:#d6e0f0}}.r i{{color:#F2B33D;font-style:normal;letter-spacing:3px}}</style>
<div class="k"><img src="{MARK}" width="96" height="96"><div><b>All In One</b><small>BAIL BONDS</small></div></div>
<h1>Bring them <em>home.</em></h1><p>24/7 bail bonds · Raleigh · Durham · Wilson, NC</p>
<div class="ph">(919) 247-9397</div><div class="r"><i>★★★★★</i> 5.0 · 494 Google reviews</div>''', IMG / "og.png", 1200, 630)
print("brand images ok")
