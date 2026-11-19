"""Turn media/grok and media/envato originals into web files in src/img and src/video.
    <venv>/bin/python tools/media.py      (needs Pillow, numpy, scipy; ffmpeg on PATH)"""
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
ROOT = Path(__file__).resolve().parent.parent
G, E, IMG, VID = ROOT / "media/grok", ROOT / "media/envato", ROOT / "src/img", ROOT / "src/video"
ICONS = {"phone": "icon-phone_v1", "clock": "icon-clock_v1", "document": "icon-document_v1", "calculator": "icon-calculator_v1",
         "shield": "icon-shield_v1", "pin": "icon-pin_v1", "chat": "icon-chat_v1", "home": "icon-home-heart_v1",
         "handshake": "icon-handshake_v1", "star": "icon-star_v1", "calendar": "icon-calendar_v1", "car": "icon-car_v1",
         "scales": "icon-scales_v1", "money": "icon-money_v1"}
SCENES = {"night-call": (G / "scene-night-call_v1.jpg", None), "signing": (G / "scene-signing_v2.jpg", None),
          "desk": (G / "scene-agent-desk_v2.jpg", None), "reunion": (G / "scene-reunion_v2.jpg", None),
          "highway": (G / "scene-highway-night_v1.jpg", None),
          "raleigh": (next(E.glob("raleigh-north-carolina-usa-downtown*.jpg")), None)}

def cutout(src, out, size=256):
    """Remove the white background connected to the edges; keep inner highlights."""
    a = np.asarray(Image.open(src).convert("RGB")).astype(float)
    dist = np.sqrt(((255 - a) ** 2).sum(-1))            # distance from pure white
    bgish = dist < 38
    lab, _ = ndi.label(bgish)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(edge))
    near = ndi.binary_dilation(outside, iterations=3) & ~outside
    alpha = np.where(outside, 0, 255).astype(float)
    alpha[near] = np.clip(dist[near] / 70 * 255, 0, 255)  # soft edge and keep the soft shadow faintly
    rgba = np.dstack([a, alpha]).astype(np.uint8)
    im = Image.fromarray(rgba, "RGBA"); bb = im.getbbox(); im = im.crop(bb)
    w, h = im.size; s = max(w, h); pad = int(s * .06); can = Image.new("RGBA", (s + 2 * pad, s + 2 * pad), (0, 0, 0, 0))
    can.paste(im, ((s - w) // 2 + pad, (s - h) // 2 + pad)); can = can.resize((size, size), Image.LANCZOS)
    can.save(out, "WEBP", quality=88, method=6)

def scene(src, name):
    im = Image.open(src).convert("RGB")
    for w in (1600, 900):
        r = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        r.save(IMG / "scenes" / f"{name}-{w}.webp", "WEBP", quality=74, method=6)
        if w == 1600: r.save(IMG / "scenes" / f"{name}-{w}.jpg", quality=78, optimize=True)

def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)

def main():
    for k, v in ICONS.items(): cutout(G / f"{v}.jpg", IMG / "icons" / f"{k}.webp")
    for k, (p, _) in SCENES.items(): scene(p, k)
    ral = next(E.glob("raleigh-north-carolina-time-lapse*.mov")); dur = next(E.glob("durham-downtown*.mp4"))
    vf = "scale=1280:-2,format=yuv420p"
    ff("-i", str(ral), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-profile:v", "main", "-movflags", "+faststart", str(VID / "raleigh-dawn.mp4"))
    ff("-ss", "26", "-i", str(ral), "-frames:v", "1", "-vf", "scale=1600:-2", str(IMG / "scenes" / "raleigh-dawn-poster.jpg"))
    ff("-ss", "2", "-t", "16", "-i", str(dur), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", "30", "-profile:v", "main", "-movflags", "+faststart", str(VID / "durham-dusk.mp4"))
    ff("-ss", "10", "-i", str(dur), "-frames:v", "1", "-vf", "scale=1600:-2", str(IMG / "scenes" / "durham-1600.jpg"))
    Image.open(IMG / "scenes" / "durham-1600.jpg").save(IMG / "scenes" / "durham-1600.webp", "WEBP", quality=74)
    Image.open(IMG / "scenes" / "durham-1600.jpg").resize((900, 506)).save(IMG / "scenes" / "durham-900.webp", "WEBP", quality=74)
    p = IMG / "scenes" / "raleigh-dawn-poster.jpg"; Image.open(p).save(p.with_suffix(".webp"), "WEBP", quality=72)
    print("media ok")

if __name__ == "__main__":
    main()
