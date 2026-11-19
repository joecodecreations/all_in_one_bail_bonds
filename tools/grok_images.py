"""Generate site icons and scene images with Grok Imagine through the grok CLI (headless).

    python3 tools/grok_images.py [--jobs 4] [--variants 2] [slug ...]

Each grok run may only call image_gen. Images land in ~/.grok/sessions/<cwd>/<sessionId>/images/;
this script copies them to media/grok/<slug>_v<n>.jpg and appends to media/grok/log.json.
Brand rule: no jail cells, handcuffed people, badges, seals or anything that looks official.
"""
import argparse, json, shutil, subprocess, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "media" / "grok"
GROK = str(Path.home() / ".local/bin/grok")
SESS = Path.home() / ".grok" / "sessions" / urllib.parse.quote(str(OUT), safe="")
RULES = ("This is a scripted image-generation job. Use only the image_gen tool. "
         "Do not run trackers (orbital-track), do not search for or call MCP tools, do not spawn agents.")

ICON = ("A single 3D icon in a soft, glossy clay style, colored deep navy blue (#0B2559) and bright azure blue (#1E6FF0) with small "
        "white highlights, centered on a pure plain white background, soft studio lighting, a gentle soft shadow "
        "beneath it, generous empty margin around it. No text, no letters, no numbers, no border, no frame. "
        "Minimal, premium, friendly, consistent app-icon quality. The object: ")
PHOTO = ("Cinematic editorial photograph, realistic, natural skin tones, shallow depth of field, subtle film grain, "
         "no text, no logos, no watermarks, no police, no handcuffs, no jail. Scene: ")
LOGO = ("A flat vector logo symbol for a trustworthy family-owned bail bond agency, deep navy blue (#14305E) and warm gold (#F2B33D) only, "
        "bold simple geometric shapes, works at small sizes, centered on a pure plain white background, generous margin. "
        "No text, no words, no letters except where asked, no handcuffs, no bars, no badge, no shield, no police or government symbols. The symbol: ")
JOBS = {
 "icon-phone": ("1:1", ICON + "a modern smartphone with three curved ringing sound waves beside it."),
 "icon-clock": ("1:1", ICON + "a round alarm clock with a blank face and a small crescent moon beside it, meaning open all night."),
 "icon-document": ("1:1", ICON + "a clipboard holding a document with a signature line and a fountain pen resting on it."),
 "icon-calculator": ("1:1", ICON + "a chunky calculator with blank rounded keys."),
 "icon-shield": ("1:1", ICON + "a rounded shield with a bold check mark on it."),
 "icon-pin": ("1:1", ICON + "a map location pin standing on a small folded map."),
 "icon-chat": ("1:1", ICON + "two overlapping speech bubbles, one navy and one bright blue, with three dots in one of them."),
 "icon-home-heart": ("1:1", ICON + "a small house with a heart on its front, meaning family and home."),
 "icon-handshake": ("1:1", ICON + "two hands in a firm handshake."),
 "icon-star": ("1:1", ICON + "a five-point star with three small sparkles around it."),
 "icon-calendar": ("1:1", ICON + "a desk calendar page with a large check mark on it, meaning a court date kept."),
 "icon-car": ("1:1", ICON + "a small compact car seen from the front three-quarter angle with a car key beside it."),
 "icon-scales": ("1:1", ICON + "a balance scale, perfectly level."),
 "icon-money": ("1:1", ICON + "a neat stack of paper money with a small coin, wrapped in a band."),
 "scene-night-call": ("16:9", PHOTO + "a worried woman in her forties sits at her kitchen table late at night, phone pressed to her ear, "
                      "lit warmly by a single pendant lamp and the glow of the phone, the rest of the room in deep shadow with a faint cool blue accent light, "
                      "she looks hopeful, framed off-center to the right leaving dark empty space on the left."),
 "scene-agent-desk": ("16:9", PHOTO + "a tidy small-business office at night: a wooden desk with neat paperwork, a pen, a coffee mug and a desk lamp glowing, "
                      "a phone face down, city lights blurred through the window behind, warm and calm, nobody in the frame."),
 "scene-reunion": ("16:9", PHOTO + "early morning, golden sunrise light, a young man hugs his relieved mother tightly in a quiet parking lot beside "
                   "a car, faces partly turned away from the camera, emotional and warm, North Carolina pine trees in the background."),
 "scene-highway-night": ("16:9", PHOTO + "a North Carolina highway at night with long-exposure gold and white light trails curving through "
                         "tall pine tree silhouettes under a deep blue sky, wide, atmospheric, lots of dark sky at the top."),
 "scene-signing": ("16:9", PHOTO + "close-up of two pairs of hands across a desk, one hand signing a paper form with a pen while the other hand "
                   "gently points to the signature line, warm lamp light, reassuring, faces not visible."),
 "logo-door": ("1:1", LOGO + "an arched open doorway with warm golden light pouring out onto a path, meaning coming home."),
 "logo-sunrise": ("1:1", LOGO + "a rising sun over a simple house roofline, meaning home by morning."),
 "logo-key": ("1:1", LOGO + "an old-fashioned key whose bow is shaped like a house."),
 "logo-a1": ("1:1", LOGO + "an elegant monogram of the letters A and 1 joined into one mark inside a circle."),
 "logo-link": ("1:1", LOGO + "three interlocking rings forming one unbroken loop, meaning all in one."),
 "logo-north": ("1:1", LOGO + "a compass star whose north point is a tiny house, meaning guidance home."),
}


def run(slug, k):
    ar, prompt = JOBS[slug]
    pf = OUT / "prompts" / f"{slug}.txt"; pf.parent.mkdir(parents=True, exist_ok=True)
    pf.write_text(f"Call the image_gen tool exactly {k} time(s), all in the same step, each with aspect_ratio \"{ar}\" and "
                  "with the prompt set to exactly the text between the markers below, copied character for character. "
                  "Do not call any other tool. When done, reply with just the word done.\n\n<<<PROMPT\n" + prompt + "\nPROMPT>>>\n")
    cmd = [GROK, "--prompt-file", str(pf), "--cwd", str(OUT), "--output-format", "json", "--tools", "image_gen",
           "--disallowed-tools", "use_tool,search_tool,Agent", "--max-turns", "4", "--rules", RULES, "--no-auto-update"]
    t0 = time.time(); p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(OUT), timeout=900)
    res = {"slug": slug, "exit": p.returncode, "secs": round(time.time() - t0), "files": []}
    try:
        sid = json.loads(p.stdout)["sessionId"]
    except Exception:
        res["error"] = (p.stdout or p.stderr)[-400:]; return res
    calls, results = {}, {}
    for line in (SESS / sid / "chat_history.jsonl").read_text().splitlines():
        m = json.loads(line)
        for tc in m.get("tool_calls") or []: calls[tc["id"]] = tc
        if m.get("type") == "tool_result": results[m["tool_call_id"]] = m.get("content")
    v = 0
    for cid, tc in calls.items():
        try:
            src = Path(json.loads(results.get(cid) or "")["path"])
        except Exception:
            continue
        v += 1; dst = OUT / f"{slug}_v{v}{src.suffix}"; shutil.copy2(src, dst); res["files"].append(dst.name)
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--jobs", type=int, default=4); ap.add_argument("--variants", type=int, default=2)
    ap.add_argument("slugs", nargs="*"); a = ap.parse_args()
    todo = a.slugs or list(JOBS)
    with ThreadPoolExecutor(a.jobs) as ex:
        out = list(ex.map(lambda s: run(s, a.variants), todo))
    log = OUT / "log.json"; old = json.loads(log.read_text()) if log.exists() else []
    log.write_text(json.dumps(old + out, indent=1))
    for r in out: print(r["slug"], r["exit"], r["secs"], "s", r["files"], r.get("error", ""))


if __name__ == "__main__":
    main()
