import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from glass import *
A = os.path.join(os.path.dirname(__file__), "..", "assets")
def w(name, s): open(os.path.join(A, name), "w").write(s)

# ---------- banner ----------
def banner():
    W,H = 1200,360
    grid = "".join(f'<path d="M{x} 0V{H}"/>' for x in range(0,W,40)) + "".join(f'<path d="M0 {y}H{W}"/>' for y in range(0,H,40))
    b = f'''<g stroke="#fff" stroke-opacity="0.04">{grid}</g>
<circle cx="220" cy="90" r="110" fill="#38bdf8" opacity="0.55" filter="url(#blurb)"><animate attributeName="cx" values="220;320;220" dur="14s" repeatCount="indefinite"/></circle>
<circle cx="640" cy="320" r="120" fill="#7c3aed" opacity="0.5" filter="url(#blurb)"><animate attributeName="cy" values="320;250;320" dur="12s" repeatCount="indefinite"/></circle>
<circle cx="1020" cy="80" r="110" fill="#06b6d4" opacity="0.45" filter="url(#blurb)"><animate attributeName="cx" values="1020;930;1020" dur="16s" repeatCount="indefinite"/></circle>
{panel("b",40,40,1120,280,24)}
<rect x="80" y="80" width="218" height="30" rx="15" fill="#fff" fill-opacity="0.07" stroke="#fff" stroke-opacity="0.2"/>
<circle cx="100" cy="95" r="4.5" fill="#34d399"><animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/></circle>
<text x="114" y="100" font-family="{FONT}" font-size="13" fill="#cbd5e1" letter-spacing="0.6">Open to freelance work</text>
<text x="80" y="178" font-family="{FONT}" font-size="68" font-weight="800" fill="#fff" letter-spacing="-1.5">Gajaananth</text>
<text x="80" y="222" font-family="{FONT}" font-size="25" font-weight="600" fill="url(#accb)">AI Engineer  •  Software Builder  •  Problem Solver</text>
<text x="80" y="258" font-family="{FONT}" font-size="16" fill="#94a3b8">Freelance innovator and entrepreneur building intelligent, reliable software for real business needs.</text>
<text x="80" y="288" font-family="{MONO}" font-size="13" fill="#64748b">Batticaloa, Sri Lanka  /  working worldwide</text>
<g font-family="{MONO}" font-size="13" fill="#e2e8f0">
<rect x="880" y="86" width="240" height="190" rx="16" fill="#0b1220" fill-opacity="0.6" stroke="#fff" stroke-opacity="0.16"/>
<circle cx="900" cy="106" r="5" fill="#f87171"/><circle cx="918" cy="106" r="5" fill="#fbbf24"/><circle cx="936" cy="106" r="5" fill="#34d399"/>
<text x="898" y="146" fill="#a78bfa">const</text><text x="942" y="146" fill="#38bdf8">dev</text><text x="972" y="146">= {{</text>
<text x="914" y="172" fill="#94a3b8">focus:</text><text x="962" y="172" fill="#fbbf24">"AI + Web"</text>
<text x="914" y="196" fill="#94a3b8">mode:</text><text x="962" y="196" fill="#fbbf24">"Full Stack"</text>
<text x="914" y="220" fill="#94a3b8">ships:</text><text x="962" y="220" fill="#34d399">true</text>
<text x="898" y="246">}};</text>
<rect x="922" y="234" width="8" height="15" fill="#38bdf8"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>
</g>'''
    return scene("b",W,H,"#38bdf8","#a78bfa",b,orbs=[])

# ---------- generic project card ----------
def card(uid, icon, title, tag, lines, tags, c1, c2, footer_text=None):
    W,H = 560,260
    d = "".join(f'<text x="40" y="{126+i*23}" font-family="{FONT}" font-size="15" fill="#cbd5e1">{esc(l)}</text>' for i,l in enumerate(lines))
    x=40; chips=""
    for t in tags:
        c,wd = chip(x,206,t); chips+=c; x+=wd+10
    b = (panel(uid,14,14,W-28,H-28) +
         f'<rect x="40" y="38" width="52" height="52" rx="14" fill="url(#acc{uid})"/><text x="66" y="73" text-anchor="middle" font-size="26">{icon}</text>'
         f'<text x="108" y="62" font-family="{FONT}" font-size="24" font-weight="700" fill="#fff">{esc(title)}</text>'
         f'<text x="108" y="84" font-family="{FONT}" font-size="12.5" fill="{c1}" letter-spacing="1.2">{esc(tag)}</text>{d}{chips}')
    if footer_text:
        b += f'<text x="{W-40}" y="224" text-anchor="end" font-family="{MONO}" font-size="12" fill="{c1}">{esc(footer_text)}</text>'
    return scene(uid,W,H,c1,c2,b,orbs=[(90,40,70,c1,0.55),(500,230,80,c2,0.5)])

# ---------- "now" strip ----------
def now():
    W,H=1200,150
    items=[("FREELANCING","AI and full-stack products","for clients worldwide","#38bdf8"),
           ("STUDYING","BIT (R) Undergraduate","University of Moratuwa","#a78bfa"),
           ("BUILDING","Solutions for finance, hospitality,","education and enterprise","#34d399")]
    b=""
    for i,(k,l1,l2,c) in enumerate(items):
        x=20+i*392
        b+=panel("n",x,16,376,118,18)
        b+=f'<circle cx="{x+30}" cy="46" r="5" fill="{c}"><animate attributeName="opacity" values="1;0.25;1" dur="{2+i*0.5}s" repeatCount="indefinite"/></circle>'
        b+=f'<text x="{x+46}" y="51" font-family="{FONT}" font-size="12" letter-spacing="2" fill="{c}">{k}</text>'
        b+=f'<text x="{x+28}" y="86" font-family="{FONT}" font-size="18" font-weight="700" fill="#fff">{esc(l1)}</text>'
        b+=f'<text x="{x+28}" y="110" font-family="{FONT}" font-size="15" fill="#94a3b8">{esc(l2)}</text>'
    return scene("n",W,H,"#38bdf8","#a78bfa",b,orbs=[(150,70,70,"#38bdf8",0.45),(600,80,70,"#7c3aed",0.4),(1050,70,70,"#34d399",0.35)],blur=30)

# ---------- services ----------
def services():
    W,H=1200,250
    items=[("🤖","AI and Automation",["AI workspaces, workflow","automation, LLM features"],"#a78bfa","#38bdf8"),
           ("🌐","Web Platforms",["Dashboards, finance and booking","systems for real operations"],"#38bdf8","#34d399"),
           ("📱","Mobile Apps",["Flutter apps designed for","unreliable connectivity"],"#f87171","#fb923c"),
           ("⚙️","Backends and APIs",["Django, FastAPI, Node.js","on PostgreSQL"],"#fbbf24","#f472b6")]
    b=""
    for i,(ic,t,ls,c1,c2) in enumerate(items):
        x=20+i*295
        b+=panel("v",x,18,277,214,20)
        b+=f'<defs><linearGradient id="g{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
        b+=f'<rect x="{x+24}" y="44" width="56" height="56" rx="16" fill="url(#g{i})"/><text x="{x+52}" y="81" text-anchor="middle" font-size="28">{ic}</text>'
        b+=f'<text x="{x+24}" y="140" font-family="{FONT}" font-size="20" font-weight="700" fill="#fff">{esc(t)}</text>'
        b+="".join(f'<text x="{x+24}" y="{168+j*22}" font-family="{FONT}" font-size="14" fill="#94a3b8">{esc(l)}</text>' for j,l in enumerate(ls))
        b+=f'<rect x="{x+24}" y="204" width="48" height="3" rx="1.5" fill="{c1}"/>'
    return scene("v",W,H,"#38bdf8","#a78bfa",b,orbs=[(150,60,70,"#a78bfa",0.45),(450,200,70,"#38bdf8",0.4),(750,60,70,"#f87171",0.35),(1050,200,70,"#fbbf24",0.35)],blur=34)

# ---------- tech stack ----------
def stack():
    W=1200
    groups=[("FRONTEND AND MOBILE","#38bdf8",[("React","#61DAFB"),("Next.js","#ffffff"),("TypeScript","#3178C6"),("JavaScript","#F7DF1E"),("HTML5","#E34F26"),("CSS3","#1572B6"),("Tailwind","#38BDF8"),("Flutter","#02569B"),("Dart","#00B4AB")]),
            ("BACKEND AND AI","#a78bfa",[("Python","#FFD43B"),("Django","#44B78B"),("FastAPI","#009688"),("Node.js","#6CC24A"),("Express","#ffffff"),("REST APIs","#a78bfa"),("AI Workflows","#f472b6")]),
            ("DATA AND DELIVERY","#34d399",[("PostgreSQL","#336791"),("MySQL","#4479A1"),("MongoDB","#47A248"),("Redis","#DC382D"),("Docker","#2496ED"),("Git","#F05032"),("GitHub","#ffffff"),("Vercel","#ffffff"),("Linux","#FCC624")])]
    b=""; y=18
    for name,c,items in groups:
        x0=300; x=x0; row=0
        pos=[]
        for t,col in items:
            wd=int(len(t)*14*0.62+44)
            if x+wd>1150: x=x0; row+=1
            pos.append((t,col,x,row,wd)); x+=wd+12
        h=96+row*42
        b+=panel("t",20,y,1160,h,18)
        b+=f'<rect x="44" y="{y+h/2-18}" width="4" height="36" rx="2" fill="{c}"/>'
        b+=f'<text x="64" y="{y+h/2+4}" font-family="{FONT}" font-size="12" letter-spacing="2" fill="{c}">{name}</text>'
        for t,col,x,r,wd in pos:
            yy=y+34+r*42
            b+=(f'<rect x="{x}" y="{yy}" width="{wd}" height="28" rx="14" fill="#fff" fill-opacity="0.07" stroke="#fff" stroke-opacity="0.2"/>'
                f'<circle cx="{x+16}" cy="{yy+14}" r="4" fill="{col}"/>'
                f'<text x="{x+28}" y="{yy+19}" font-family="{MONO}" font-size="14" fill="#e2e8f0">{esc(t)}</text>')
        y+=h+16
    H=y+2
    return scene("t",W,H,"#38bdf8","#a78bfa",b,orbs=[(150,60,80,"#38bdf8",0.4),(1050,H-60,90,"#a78bfa",0.4)],blur=34)

# ---------- process pipeline ----------
def process():
    W,H=1200,170
    steps=[("01","Discover","#38bdf8"),("02","Design","#a78bfa"),("03","Build","#34d399"),("04","Ship","#fbbf24"),("05","Scale","#f472b6")]
    b=panel("p",20,16,1160,138,20)
    b+='<path d="M120 84H1080" stroke="#fff" stroke-opacity="0.15" stroke-width="2" stroke-dasharray="6 8"/>'
    b+='<circle r="5" fill="#38bdf8"><animateMotion dur="6s" repeatCount="indefinite" path="M120 84H1080"/></circle>'
    for i,(n,t,c) in enumerate(steps):
        x=120+i*240
        b+=f'<circle cx="{x}" cy="84" r="30" fill="#0b1220" stroke="{c}" stroke-width="2"/><circle cx="{x}" cy="84" r="30" fill="{c}" opacity="0.12"/>'
        b+=f'<text x="{x}" y="90" text-anchor="middle" font-family="{MONO}" font-size="18" font-weight="700" fill="{c}">{n}</text>'
        b+=f'<text x="{x}" y="140" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="600" fill="#e2e8f0">{t}</text>'
    return scene("p",W,H,"#38bdf8","#a78bfa",b,orbs=[(200,80,70,"#38bdf8",0.4),(1000,80,70,"#a78bfa",0.4)],blur=30)

# ---------- divider / footer ----------
def divider():
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="20" viewBox="0 0 1200 20"><defs><linearGradient id="d" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#38bdf8" stop-opacity="0"/><stop offset="0.5" stop-color="#a78bfa"/><stop offset="1" stop-color="#38bdf8" stop-opacity="0"/></linearGradient></defs><rect x="0" y="9" width="1200" height="2" rx="1" fill="url(#d)"/><circle cx="600" cy="10" r="5" fill="#a78bfa"><animate attributeName="r" values="4;6;4" dur="3s" repeatCount="indefinite"/></circle></svg>'
def footer():
    W,H=1200,130
    b=panel("f",20,16,1160,98,20)+f'<text x="600" y="62" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="700" fill="#fff">Let\'s build something meaningful.</text><text x="600" y="90" text-anchor="middle" font-family="{FONT}" font-size="14" fill="#94a3b8">gajaananth.vercel.app  •  linkedin.com/in/gajaananth  •  github.com/Gajaananth</text>'
    return scene("f",W,H,"#38bdf8","#a78bfa",b,orbs=[(200,60,80,"#38bdf8",0.5),(1000,70,90,"#7c3aed",0.5)])

w("banner.svg",banner()); w("now.svg",now()); w("services.svg",services()); w("stack.svg",stack()); w("process.svg",process())
w("divider.svg",divider()); w("footer.svg",footer())
w("card-selva.svg",card("s","🚨","Selva NaDhanam","DISASTER-RESILIENT SOS APP",["Disaster-ready SOS app with a 10-layer","fail-safe communication system for when","connectivity is unreliable."],["Flutter","Django","Dart"],"#f87171","#fb923c","view on GitHub"))
w("card-gvc.svg",card("g","💼","GVC Agro","FINANCE PLATFORM / PRODUCTION",["Full-stack platform managing loans, savings,","customers and branches. Production software","built for real business operations."],["React","TypeScript","Node.js","PostgreSQL"],"#34d399","#38bdf8"))
w("card-karuppu.svg",card("k","🤖","Karuppu","AI WORKSPACE",["AI-powered workspace for managing tasks","and automating repetitive workflows,","cutting manual busywork."],["React","TypeScript","AI"],"#a78bfa","#38bdf8"))
w("card-treatooo.svg",card("t2","🏨","Treatooo Hotels","HOSPITALITY PLATFORM",["Web platform for hotel groups with multiple","properties, with a consistent brand presence","and a smooth booking flow."],["React","Django"],"#fbbf24","#f472b6"))
w("card-dearo.svg",card("d2","📍","Dearo Backend","FIELD VISIT APP / API",["Backend service powering an app built","for field visits, written in Python."],["Python","API"],"#22d3ee","#818cf8","view on GitHub"))
w("card-more.svg",card("m","✨","22 Repositories","EXPLORE THE REST",["More experiments, client builds and","learning projects live on my GitHub.","Come take a look."],["github.com/Gajaananth"],"#e879f9","#38bdf8"))
print("built")
