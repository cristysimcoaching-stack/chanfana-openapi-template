# -*- coding: utf-8 -*-
"""Rich original SVG hero illustrations for recipe pages, chapter dividers,
and section openers. Flat, modern, palette-driven. 100% original vector art —
no external or copyrighted assets."""

# color themes (tint = soft panel background, main/main2 = subject, accent/deco = details)
THEMES = {
 'mango':   dict(tint='#FEF5D8', main='#F5B301', main2='#F7C948', accent='#F58634', deco='#EF5A8C', surf='#EAD49A'),
 'berry':   dict(tint='#FDE7EF', main='#EF5A8C', main2='#F58BB0', accent='#D63A6E', deco='#F5B301', surf='#F0C4D6'),
 'blue':    dict(tint='#EAF2FE', main='#3E86F0', main2='#7FB2FA', accent='#1B6FEF', deco='#EF5A8C', surf='#C4D9F5'),
 'cocoa':   dict(tint='#EFE3D9', main='#8A5A34', main2='#AD7248', accent='#C9895A', deco='#F5B301', surf='#D6C0AE'),
 'banana':  dict(tint='#FEF7DC', main='#EFCB4E', main2='#F6E07A', accent='#E0B93A', deco='#8FBF6A', surf='#E7D79A'),
 'orange':  dict(tint='#FCEBDC', main='#F58634', main2='#F9A664', accent='#E06A1E', deco='#F5B301', surf='#EFC7A2'),
 'green':   dict(tint='#E4F5EC', main='#3AA873', main2='#6BC79A', accent='#1E7D50', deco='#F5B301', surf='#BEE4D0'),
 'melon':   dict(tint='#FDE7EF', main='#EF5A8C', main2='#F58BB0', accent='#3AA873', deco='#3AA873', surf='#F0C4D6'),
}
THEME_BY_N = {1:'mango',2:'blue',3:'melon',4:'banana',5:'banana',6:'berry',7:'cocoa',8:'cocoa',
 9:'orange',10:'mango',11:'banana',12:'orange',13:'blue',14:'orange',15:'orange',16:'orange',
 17:'green',18:'orange',19:'berry',20:'orange',21:'cocoa',22:'berry',23:'banana',24:'cocoa',
 25:'cocoa',26:'blue',27:'berry',28:'orange',29:'cocoa',30:'banana',31:'berry',32:'banana'}

def theme_for(n): return THEMES[THEME_BY_N.get(n,'blue')]

def _surface(t, y=176):
    return f'<ellipse cx="200" cy="{y}" rx="150" ry="12" fill="{t["surf"]}" opacity=".55"/>'

def _scatter(t):  # decorative dots + sparkles in the field
    d=t['deco']; d2=t['main2']
    pts=[(52,54,6,d),(360,58,7,d2),(70,150,5,d2),(338,150,6,d),(300,40,4,d),(96,40,4,d2)]
    s="".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".8"/>' for x,y,r,c in pts)
    for x,y in [(44,110),(356,104),(120,32),(280,158)]:
        s+=(f'<g stroke="{t["accent"]}" stroke-width="2.4" stroke-linecap="round" opacity=".7">'
            f'<line x1="{x-6}" y1="{y}" x2="{x+6}" y2="{y}"/><line x1="{x}" y1="{y-6}" x2="{x}" y2="{y+6}"/></g>')
    return s

def _steam(x, t):
    return (f'<g stroke="{t["accent"]}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".5">'
            f'<path d="M{x} 96c-7-8 7-14 0-22"/><path d="M{x+16} 92c-7-8 7-14 0-22"/>'
            f'<path d="M{x+32} 96c-7-8 7-14 0-22"/></g>')

# ---------------- subject templates (400 x 210 canvas) ----------------------
def _pop(t):
    body=""
    for x,rot,mc in [(150,-9,t['main']),(200,0,t['main2']),(250,9,t['accent'])]:
        body+=(f'<g transform="rotate({rot} {x+22} 100)">'
          f'<rect x="{x}" y="46" width="44" height="92" rx="22" fill="{mc}"/>'
          f'<rect x="{x+8}" y="56" width="9" height="40" rx="4.5" fill="#fff" opacity=".45"/>'
          f'<path d="M{x} 118c8 10 36 10 44 0v14c0 12-36 12-44 0z" fill="{t["main"]}" opacity=".55"/>'
          f'<rect x="{x+18}" y="136" width="8" height="30" rx="4" fill="#D9B98A"/></g>')
    return _surface(t,182)+body

def _snow(t):  # frozen bark on a tray
    berries="".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{t["main"]}"/>' for x,y in [(150,96),(196,86),(244,98),(180,112),(224,80)])
    chips="".join(f'<rect x="{x}" y="{y}" width="7" height="7" rx="1.6" fill="{t["accent"]}"/>' for x,y in [(168,78),(214,104),(258,84),(140,110)])
    frost="".join(f'<g stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".9"><line x1="{x-5}" y1="{y}" x2="{x+5}" y2="{y}"/><line x1="{x}" y1="{y-5}" x2="{x}" y2="{y+5}"/></g>' for x,y in [(130,70),(272,110),(300,74)])
    return (_surface(t,178)
      +f'<rect x="120" y="66" width="160" height="66" rx="12" fill="#fff"/>'
      +f'<rect x="120" y="66" width="160" height="66" rx="12" fill="{t["main2"]}" opacity=".28"/>'
      +berries+chips+frost
      +f'<path d="M286 128l24-10-4 30z" fill="{t["main2"]}" opacity=".7"/>')

def _cup(t):  # layered glass + spoon
    return (_surface(t,180)
      +f'<path d="M164 60h72l-9 104a10 10 0 0 1-10 9h-24a10 10 0 0 1-10-9z" fill="#fff"/>'
      +f'<path d="M170 118h60l-4 46a10 10 0 0 1-10 9h-32a10 10 0 0 1-10-9z" fill="{t["main"]}"/>'
      +f'<path d="M167 90h66l-2 24h-62z" fill="{t["main2"]}" opacity=".9"/>'
      +f'<rect x="164" y="54" width="72" height="12" rx="6" fill="{t["main2"]}"/>'
      +f'<circle cx="200" cy="50" r="9" fill="{t["deco"]}"/>'
      +f'<path d="M200 41c0-5 4-7 7-8" stroke="{t["accent"]}" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
      +f'<rect x="178" y="70" width="7" height="80" rx="3" fill="#fff" opacity=".4"/>'
      +f'<g transform="rotate(18 250 70)"><rect x="248" y="52" width="6" height="86" rx="3" fill="#B9C0CA"/>'
      +f'<ellipse cx="251" cy="52" rx="11" ry="8" fill="#CDD3DB"/></g>')

def _bowl(t):  # bowl with scoops + toppings
    scoops="".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x,y,r,c in [(178,96,24,t['main']),(214,92,26,t['main2']),(200,110,22,t['accent'])])
    tops="".join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{t["deco"]}"/>' for x,y in [(176,80),(210,72),(230,96),(190,86)])
    leaf=f'<path d="M226 70c8-10 20-8 22-2-10 4-16 8-22 2z" fill="{t["accent"] if THEMES else "#3AA873"}"/>'
    return (_surface(t,176)+scoops+tops
      +f'<path d="M150 118h100a50 50 0 0 1-100 0z" fill="{t["main"]}"/>'
      +f'<ellipse cx="200" cy="118" rx="50" ry="9" fill="{t["main2"]}"/>'
      +f'<path d="M150 118h100a50 50 0 0 1-100 0z" fill="#000" opacity=".05"/>')

def _cookie(t):
    edge=t['accent']
    def ck(x,y,r=30):
        chips="".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="3.4" fill="{t["accent"]}"/>' for dx,dy in [(-11,-6),(10,-9),(4,9),(-9,8),(13,4),(0,-2)])
        return (f'<ellipse cx="{x}" cy="{y+r-3}" rx="{r-2}" ry="6" fill="#000" opacity=".06"/>'
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["main"]}" stroke="{edge}" stroke-width="1.6"/>'
                f'<path d="M{x-r+6} {y}a{r-6} {r-6} 0 0 1 {2*(r-6)} 0z" fill="#fff" opacity=".14"/>{chips}')
    # two on the surface, one leaning behind for a "stack" feel
    return (_surface(t,170)
      +ck(168,116,28)+ck(232,116,28)
      +f'<g transform="rotate(-16 200 96)">{ck(200,100,30)}</g>')

def _muffin(t):
    liner=f'<path d="M168 108h64l-9 52a6 6 0 0 1-6 5h-34a6 6 0 0 1-6-5z" fill="{t["accent"]}"/>'
    lines="".join(f'<line x1="{x}" y1="112" x2="{x-2}" y2="160" stroke="#fff" stroke-width="2" opacity=".35"/>' for x in range(176,232,10))
    top=f'<path d="M160 108c3-30 22-42 40-42s37 12 40 42z" fill="{t["main"]}"/>'
    dots="".join(f'<circle cx="{x}" cy="{y}" r="3.6" fill="{t["deco"]}"/>' for x,y in [(186,86),(214,80),(200,96),(178,98),(222,96)])
    return _surface(t,172)+liner+lines+top+dots

def _apple(t):  # baking dish + warm fruit + steam
    cubes="".join(f'<rect x="{x}" y="{y}" width="16" height="14" rx="3" fill="{c}"/>' for x,y,c in
        [(168,104,t['main']),(188,100,t['main2']),(208,106,t['accent']),(226,102,t['main']),(178,116,t['main2']),(214,118,t['accent'])])
    crumble="".join(f'<rect x="{x}" y="{y}" width="6" height="6" rx="1.6" fill="{t["deco"]}"/>' for x,y in [(174,98),(198,94),(222,96),(206,120),(184,122)])
    return (_surface(t,176)
      +f'<rect x="150" y="96" width="100" height="48" rx="10" fill="#fff"/>'
      +f'<rect x="150" y="96" width="100" height="48" rx="10" fill="{t["surf"]}" opacity=".4"/>'
      +cubes+crumble
      +f'<rect x="146" y="140" width="108" height="9" rx="4.5" fill="{t["surf"]}"/>'
      +_steam(184,t))

def _berry(t):
    cluster="".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x,y,r,c in
        [(180,104,18,t['main']),(206,98,20,t['main2']),(224,116,16,t['accent']),(196,122,15,t['main']),(160,116,14,t['main2'])])
    seeds="".join(f'<circle cx="{x}" cy="{y}" r="1.5" fill="#fff" opacity=".7"/>' for x,y in [(178,100),(204,94),(222,112),(194,118)])
    leaf=f'<path d="M206 78c10-14 26-12 30-4-12 6-20 12-30 4z" fill="#3AA873"/><path d="M206 78c-2-10 4-18 12-22" stroke="#3AA873" stroke-width="3" fill="none" stroke-linecap="round"/>'
    return _surface(t,172)+cluster+seeds+leaf

TPL={'pop':_pop,'snow':_snow,'cup':_cup,'bowl':_bowl,'cookie':_cookie,'muffin':_muffin,'apple':_apple,'berry':_berry}

def hero(icon, n, w=150, h=None, deco=True):
    """Return a full hero illustration SVG (string) for the given icon/recipe."""
    t=theme_for(n)
    inner=TPL.get(icon,_cup)(t)
    field=(_scatter(t) if deco else "")
    hh = h if h else round(w*210/400,1)
    return (f'<svg viewBox="0 0 400 210" width="{w}mm" height="{hh}mm" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid meet" role="img" aria-label="Illustration of {icon}">'
            f'<rect x="2" y="2" width="396" height="206" rx="20" fill="{t["tint"]}"/>{field}{inner}</svg>')

def hero_plain(icon, theme_name, w=120):
    """Hero without the tint panel (for placing on colored backgrounds)."""
    t=THEMES[theme_name]; inner=TPL.get(icon,_cup)(t)
    return (f'<svg viewBox="0 0 400 210" width="{w}mm" xmlns="http://www.w3.org/2000/svg" '
            f'preserveAspectRatio="xMidYMid meet" role="img" aria-hidden="true">{_scatter(t)}{inner}</svg>')
