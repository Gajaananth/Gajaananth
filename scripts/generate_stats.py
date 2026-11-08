#!/usr/bin/env python3
"""Generates assets/stats.svg and assets/languages.svg for the profile README.
Run by GitHub Actions daily (needs GH_TOKEN). `--demo` writes the starter files offline."""
import os, sys, json, datetime as dt, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from glass import *

USER = os.environ.get("PROFILE_USER", "Gajaananth")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

def gql(query, token):
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=60))
    if "errors" in r: raise RuntimeError(r["errors"])
    return r["data"]

def fetch(token):
    d = gql('query{user(login:"%s"){createdAt followers{totalCount} repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){totalCount nodes{stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}' % USER, token)["user"]
    created = dt.datetime.fromisoformat(d["createdAt"].replace("Z","+00:00")).year
    days = []
    for y in range(created, dt.date.today().year + 1):
        c = gql('query{user(login:"%s"){contributionsCollection(from:"%d-01-01T00:00:00Z",to:"%d-12-31T23:59:59Z"){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}' % (USER,y,y), token)
        for w in c["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            days += [(x["date"], x["contributionCount"]) for x in w["contributionDays"]]
    days.sort(); total = sum(c for _,c in days)
    longest = run = 0
    for _,c in days:
        run = run+1 if c else 0; longest = max(longest, run)
    today = dt.date.today().isoformat(); cur = 0
    for date,c in reversed([d for d in days if d[0] <= today]):
        if c: cur += 1
        elif date == today: continue
        else: break
    langs = {}
    for n in d["repositories"]["nodes"]:
        for e in n["languages"]["edges"]:
            l = langs.setdefault(e["node"]["name"], [0, e["node"]["color"] or "#94a3b8"]); l[0] += e["size"]
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    s = sum(v[0] for _,v in top) or 1
    return dict(repos=d["repositories"]["totalCount"], followers=d["followers"]["totalCount"],
                stars=sum(n["stargazerCount"] for n in d["repositories"]["nodes"]),
                total=total, longest=longest, current=cur,
                langs=[(n, v[0]/s*100, v[1]) for n,v in top], updated=today)

def stats_svg(s):
    W,H = 580,260
    items = [("Repositories", s["repos"], "#38bdf8"), ("Followers", s["followers"], "#a78bfa"),
             ("Contributions", s["total"], "#34d399"), ("Longest streak", f'{s["longest"]}d', "#fbbf24")]
    b = panel("s",14,14,W-28,H-28) + f'<text x="40" y="52" font-family="{FONT}" font-size="13" letter-spacing="2" fill="#94a3b8">GITHUB ACTIVITY</text>'
    for i,(lab,val,col) in enumerate(items):
        x = 40 + (i%2)*260; y = 78 + (i//2)*80
        b += (f'<rect x="{x}" y="{y}" width="240" height="68" rx="14" fill="#fff" fill-opacity="0.05" stroke="#fff" stroke-opacity="0.12"/>'
              f'<rect x="{x}" y="{y+14}" width="4" height="40" rx="2" fill="{col}"/>'
              f'<text x="{x+22}" y="{y+38}" font-family="{FONT}" font-size="28" font-weight="800" fill="#fff">{esc(val)}</text>'
              f'<text x="{x+22}" y="{y+58}" font-family="{FONT}" font-size="12" fill="#94a3b8">{lab}</text>')
    b += f'<text x="{W-40}" y="52" text-anchor="end" font-family="{MONO}" font-size="11" fill="#64748b">updated {s["updated"]}</text>'
    return scene("s",W,H,"#38bdf8","#a78bfa",b)

def langs_svg(s):
    W,H = 580,260; L = s["langs"]
    b = panel("l",14,14,W-28,H-28) + f'<text x="40" y="52" font-family="{FONT}" font-size="13" letter-spacing="2" fill="#94a3b8">TOP LANGUAGES</text>'
    if L and L[0][1] is not None:
        bar_x, bar_w, x = 40, W-80, 40
        b += f'<clipPath id="cl"><rect x="{bar_x}" y="70" width="{bar_w}" height="12" rx="6"/></clipPath><g clip-path="url(#cl)">'
        for n,p,c in L:
            w = bar_w*p/100; b += f'<rect x="{x:.1f}" y="70" width="{w:.1f}" height="12" fill="{c}"/>'; x += w
        b += '</g>'
        for i,(n,p,c) in enumerate(L):
            cx = 40 + (i%2)*260; cy = 112 + (i//2)*38
            b += (f'<circle cx="{cx+6}" cy="{cy}" r="6" fill="{c}"/><text x="{cx+22}" y="{cy+5}" font-family="{FONT}" font-size="15" fill="#e2e8f0">{esc(n)}</text>'
                  f'<text x="{cx+240}" y="{cy+5}" text-anchor="end" font-family="{MONO}" font-size="13" fill="#94a3b8">{p:.1f}%</text>')
    return scene("l",W,H,"#a78bfa","#38bdf8",b)

def streak_svg(s):
    W,H = 580,260
    b = panel("k",14,14,W-28,H-28) + f'<text x="40" y="52" font-family="{FONT}" font-size="13" letter-spacing="2" fill="#94a3b8">CONTRIBUTION STREAK</text>'
    cols = [("Total", s["total"], "#34d399", 100), ("Current", s["current"], "#38bdf8", 290), ("Longest", s["longest"], "#fbbf24", 480)]
    for lab,val,c,cx in cols:
        r = 44 if lab=="Current" else 34
        b += (f'<circle cx="{cx}" cy="140" r="{r}" fill="{c}" fill-opacity="0.08" stroke="{c}" stroke-width="3"/>'
              f'<text x="{cx}" y="{148 if lab=="Current" else 147}" text-anchor="middle" font-family="{FONT}" font-size="{30 if lab=="Current" else 22}" font-weight="800" fill="#fff">{val}</text>'
              f'<text x="{cx}" y="214" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{c}">{lab}</text>')
    return scene("k",W,H,"#34d399","#38bdf8",b)

def demo():
    return dict(repos=22, followers=2, stars=0, total=921, longest=16, current=1,
                langs=[], updated=dt.date.today().isoformat())

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    demo_mode = "--demo" in sys.argv
    s = demo() if demo_mode else fetch(os.environ["GH_TOKEN"])
    open(os.path.join(OUT,"stats.svg"),"w").write(stats_svg(s))
    open(os.path.join(OUT,"streak.svg"),"w").write(streak_svg(s))
    if demo_mode:  # starter card: pinned-repo languages only, no invented percentages
        b = panel("l",14,14,552,232) + f'<text x="40" y="52" font-family="{FONT}" font-size="13" letter-spacing="2" fill="#94a3b8">PRIMARY LANGUAGES</text>'
        x = 40
        for n,c in [("Python","#3572A5"),("Dart","#00B4AB"),("TypeScript","#3178c6")]:
            w = int(len(n)*14*0.62+44)
            b += (f'<rect x="{x}" y="90" width="{w}" height="28" rx="14" fill="#fff" fill-opacity="0.07" stroke="#fff" stroke-opacity="0.2"/>'
                  f'<circle cx="{x+16}" cy="104" r="4" fill="{c}"/><text x="{x+28}" y="109" font-family="{MONO}" font-size="14" fill="#e2e8f0">{n}</text>')
            x += w+12
        b += f'<text x="40" y="170" font-family="{FONT}" font-size="14" fill="#94a3b8">Live language breakdown appears here after the</text><text x="40" y="192" font-family="{FONT}" font-size="14" fill="#94a3b8">profile workflow runs for the first time.</text>'
        open(os.path.join(OUT,"languages.svg"),"w").write(scene("l",580,260,"#a78bfa","#38bdf8",b))
    else:
        open(os.path.join(OUT,"languages.svg"),"w").write(langs_svg(s))
    print("ok", {k:v for k,v in s.items() if k!="langs"})
