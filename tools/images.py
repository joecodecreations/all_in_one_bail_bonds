"""Make the logo sizes, favicon and social share card from the business's own logo.
    python3 tools/images.py     (needs Pillow)"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / "research/raw/img/342034831_559079556210862_7032403929832120700_n.jpg"
OUT = ROOT / "src/img"
logo = Image.open(SRC).convert("RGB")
for s in (88, 192, 512):
    logo.resize((s, s), Image.LANCZOS).save(OUT / f"logo-{s}.png", optimize=True)
logo.resize((48, 48), Image.LANCZOS).save(ROOT / "src/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
# share card 1200x630
W, H = 1200, 630
card = Image.new("RGB", (W, H), (15, 15, 18))
d = ImageDraw.Draw(card)
d.rectangle([0, H - 14, W, H], fill=(200, 16, 46))
mask = Image.new("L", (400, 400), 0); ImageDraw.Draw(mask).ellipse([0, 0, 400, 400], fill=255)
card.paste(logo.resize((400, 400), Image.LANCZOS), (70, 108), mask)
def font(sz, bold=True):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try: return ImageFont.truetype(p, sz)
        except OSError: pass
    return ImageFont.load_default()
d.text((530, 150), "24/7 BAIL BONDS", font=font(30), fill=(255, 184, 194))
d.text((530, 200), "Raleigh · Durham", font=font(66), fill="white")
d.text((530, 278), "Wilson, NC", font=font(66), fill="white")
d.text((530, 385), "(919) 247-9397", font=font(58), fill=(245, 179, 1))
d.text((530, 468), "5.0 stars · 494 Google reviews", font=font(30, False), fill=(233, 231, 228))
card.save(OUT / "og.png", optimize=True)
print("images ok")
