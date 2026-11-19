"""Search Envato (app.envato.com) in the Orbital browser session and list results.
    python3 tools/envato_search.py stock-video "raleigh skyline night" [stock-photo "..."] ..."""
import json, subprocess, sys, time, urllib.parse
def B(*a, t=120):
    p = subprocess.run(["orbital", "browser", "--session", "aio-envato", *a, "--timeout", str(t)], capture_output=True, text=True)
    return p.stdout
JS = r"""(async()=>{for(let i=0;i<6;i++){(document.querySelector('main')||document.scrollingElement).scrollBy(0,2500);document.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+200&&getComputedStyle(e).overflowY.match(/auto|scroll/))e.scrollTop+=2500});await new Promise(r=>setTimeout(r,700));}
 const seen=new Set(),rows=[];document.querySelectorAll('a[href*="/search/"]').forEach(a=>{const m=a.href.match(/search\/(stock-video|photos|stock-photo)\/([0-9a-f-]{36})/);if(!m||seen.has(m[2]))return;seen.add(m[2]);
 let c=a;for(let k=0;k<5&&c.parentElement&&c.innerText.trim().length<8;k++)c=c.parentElement;rows.push({id:m[2],kind:m[1],t:c.innerText.replace(/\s+/g,' ').trim().slice(0,120)})});return JSON.stringify(rows.slice(0,40))})()"""
args = sys.argv[1:]
for kind, term in zip(args[::2], args[1::2]):
    B("navigate", f"https://app.envato.com/search?itemType={kind}&term={urllib.parse.quote_plus(term)}")
    time.sleep(4)
    out = B("eval", JS)
    try:
        rows = json.loads(json.loads(out))
    except Exception:
        rows = []; print("PARSE", out[:300])
    print(f"== {kind}: {term} ({len(rows)})")
    for r in rows: print("  ", r["kind"], r["id"], "|", r["t"])
