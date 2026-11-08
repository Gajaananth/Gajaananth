"""Shared glass-style SVG helpers (no external resources, safe for GitHub <img>)."""
FONT = "'Segoe UI','Inter',-apple-system,Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Consolas,'Fira Code',monospace"

def defs(uid, c1="#38bdf8", c2="#a78bfa", blur=38):
    return f'''<defs>
<linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#05070d"/><stop offset="1" stop-color="#0b1220"/></linearGradient>
<linearGradient id="glass{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.14"/><stop offset="1" stop-color="#fff" stop-opacity="0.03"/></linearGradient>
<linearGradient id="edge{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.55"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.08"/><stop offset="1" stop-color="{c1}" stop-opacity="0.5"/></linearGradient>
<linearGradient id="acc{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<filter id="blur{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{blur}"/></filter>
</defs>'''

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def panel(uid, x, y, w, h, r=20):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glass{uid})" stroke="url(#edge{uid})" stroke-width="1.5"/>'
            f'<rect x="{x+r/2}" y="{y+1}" width="{w-r}" height="1" fill="#fff" opacity="0.35"/>')

def chip(x, y, text, fs=12):
    w = int(len(text)*fs*0.62+26)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="14" fill="#fff" fill-opacity="0.07" stroke="#fff" stroke-opacity="0.2"/>'
            f'<text x="{x+w/2}" y="{y+18.5}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" fill="#e2e8f0">{esc(text)}</text>'), w

def scene(uid, W, H, c1, c2, body, orbs=None, rx=24, blur=38):
    orbs = orbs or [(W*0.12,H*0.2,90,c1,0.5),(W*0.88,H*0.85,100,c2,0.5)]
    o = "".join(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{c}" opacity="{op}"/>' for cx,cy,r,c,op in orbs)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs(uid,c1,c2,blur)}<rect width="{W}" height="{H}" rx="{rx}" fill="url(#bg{uid})"/>'
            f'<g filter="url(#blur{uid})">{o}</g>{body}</svg>')
