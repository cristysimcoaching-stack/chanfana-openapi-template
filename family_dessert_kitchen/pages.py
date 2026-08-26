# -*- coding: utf-8 -*-
"""Assembles the full book HTML from build.py infra + recipes.py data.
Run:  python3 pages.py   ->  writes family_dessert_kitchen.html + fields.json
"""
import json, os
from build import *
from recipes import RECIPES
import art

CH = {5:"Frozen & Fruity",6:"Yogurt, Pudding & Creamy Cups",7:"Muffins, Bites & Small Bakes",
      8:"Warm Fruit Desserts",9:"Cookies, Bars & Squares",10:"Build-Your-Own Family Desserts"}

CSS = f"""
@page {{ size:A4; margin:0; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; padding:0; }}
body {{ font-family:'Liberation Sans','DejaVu Sans',Arial,sans-serif; color:{INK};
  font-size:10.6pt; line-height:1.5; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
.page {{ position:relative; width:210mm; height:297mm; page-break-after:always;
  padding:15mm 17mm 15mm 17mm; overflow:hidden; background:#fff; }}
.page:last-child {{ page-break-after:auto; }}
h1,h2,h3,h4 {{ margin:0; color:{INK_DK}; font-weight:700; line-height:1.16; }}
p {{ margin:0 0 7pt 0; }}
.serif {{ font-family:'DejaVu Serif',Georgia,serif; }}
.mute {{ color:{MUTE}; }} .small {{ font-size:8.7pt; }} .tiny {{ font-size:7.8pt; }}
.center {{ text-align:center; }}
b,strong {{ color:{INK_DK}; }}
.rh {{ display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid {RULE};
  padding-bottom:6pt; margin-bottom:13pt; font-size:7.6pt; letter-spacing:.12em; text-transform:uppercase; color:{MUTE}; }}
.rh .brand {{ font-weight:700; color:{INK_DK}; }} .rh .sec {{ color:{BLUE}; font-weight:700; }}
.eyebrow {{ font-size:8pt; letter-spacing:.16em; text-transform:uppercase; color:{BLUE}; font-weight:700; }}
.h-xl {{ font-size:30pt; letter-spacing:-.4pt; }} .h-lg {{ font-size:21pt; }} .h-md {{ font-size:15pt; }}
.rule {{ height:1px; background:{RULE}; border:0; margin:11pt 0; }}
.rule-blue {{ height:2.4pt; width:46pt; background:{BLUE}; border:0; border-radius:2pt; margin:8pt 0 12pt; }}
.panel {{ border-radius:9pt; padding:11pt 13pt; margin:9pt 0; }}
.p-blue {{ background:{BLUE_BG}; border:1px solid {BLUE_BD}; }}
.p-mango {{ background:{MANGO_BG}; border:1px solid #F1D98A; }}
.p-berry {{ background:{BERRY_BG}; border:1px solid #F6C2D5; }}
.p-orange {{ background:{ORANGE_BG}; border:1px solid #F3CBA6; }}
.p-leaf {{ background:{LEAF_BG}; border:1px solid #BFE6D1; }}
.p-soft {{ background:#F7F8FA; border:1px solid {RULE}; }}
.p-dark {{ background:{DARK_BG}; color:{DARK_TX}; }}
.p-dark h3,.p-dark h4,.p-dark b {{ color:#fff; }} .p-dark a {{ color:{BLUE_LT}; }}
.panel h4 {{ font-size:10.4pt; margin-bottom:5pt; display:flex; align-items:center; gap:7pt; }}
.panel.tight {{ padding:8pt 11pt; }}
.chip {{ display:inline-block; font-size:7.6pt; font-weight:700; letter-spacing:.05em;
  padding:2.5pt 8pt; border-radius:20pt; text-transform:uppercase; }}
.devstamp {{ display:inline-block; background:{DARK_BG}; color:#fff; font-size:7.6pt; font-weight:700;
  letter-spacing:.08em; text-transform:uppercase; padding:4pt 10pt; border-radius:5pt; }}
.ic {{ vertical-align:middle; }}
.icwrap {{ display:inline-flex; align-items:center; justify-content:center; width:34pt; height:34pt;
  border-radius:9pt; background:{BLUE_BG}; }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:11pt; }}
.grid3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:10pt; }}
.flexrow {{ display:flex; gap:12pt; align-items:flex-start; }}
.fldwrap {{ position:relative; display:inline-block; vertical-align:bottom; }}
.fldwrap .anchor {{ position:absolute; top:0; left:0; font-size:3pt; color:#fff; line-height:1; }}
.wline {{ border-bottom:1.1pt solid #B9C0CA; margin:0 2pt; }}
.wbox {{ border:1.1pt solid #B9C0CA; border-radius:5pt; background:#FCFDFE; }}
.chkbox {{ border:1.4pt solid {BLUE}; border-radius:3pt; background:#fff; margin-right:6pt; }}
.wsp {{ height:5pt; }}
.ckrow {{ display:inline-flex; align-items:center; margin:0 15pt 8pt 0; vertical-align:top; }}
.cklab {{ font-size:9.8pt; }}
.ckcol .ckrow {{ display:flex; margin:0 0 9pt 0; }}
.rc-meta {{ display:flex; gap:7pt; flex-wrap:wrap; margin:7pt 0 2pt; }}
.rc-title {{ font-size:21pt; letter-spacing:-.3pt; margin-top:4pt; }}
.rc-sub {{ color:{MUTE}; font-size:9.2pt; margin-top:3pt; }}
.rc-two {{ display:grid; grid-template-columns:1.12fr 1fr; gap:14pt; margin-top:10pt; }}
.metric {{ color:{MUTE}; font-size:8.5pt; }}
ul.clean {{ list-style:none; padding-left:0; margin:0; }}
ul.clean li {{ position:relative; padding-left:13pt; margin-bottom:3.6pt; }}
ul.clean li::before {{ content:''; position:absolute; left:0; top:6pt; width:5.5pt; height:5.5pt; border-radius:50%; background:{BLUE}; }}
ol.steps {{ list-style:none; padding-left:0; margin:0; counter-reset:st; }}
ol.steps li {{ position:relative; padding-left:25pt; margin-bottom:7pt; counter-increment:st; }}
ol.steps li::before {{ content:counter(st,decimal-leading-zero); position:absolute; left:0; top:-1pt; width:18pt; height:18pt;
  border-radius:50%; background:{DARK_BG}; color:#fff; font-size:8.3pt; font-weight:700; display:flex; align-items:center; justify-content:center; }}
.rolebox {{ border-radius:8pt; padding:8pt 10pt; margin-bottom:8pt; }}
.role-child {{ background:{MANGO_BG}; border:1px solid #F1D98A; }}
.role-adult {{ background:{BLUE_BG}; border:1px solid {BLUE_BD}; }}
.rolebox h4 {{ font-size:8.6pt; text-transform:uppercase; letter-spacing:.06em; margin-bottom:2pt; }}
.metaline {{ font-size:9pt; }}
.metaline .r {{ display:flex; gap:8pt; margin-bottom:3.5pt; }}
.metaline .k {{ font-weight:700; color:{INK_DK}; width:78pt; flex:none; }}
.mission {{ border:1px solid {RULE}; border-radius:9pt; padding:10pt 12pt; margin:8pt 0; background:#fff; }}
.mtag {{ display:inline-flex; align-items:center; gap:7pt; font-size:8pt; font-weight:700; letter-spacing:.09em;
  text-transform:uppercase; color:{BLUE}; margin-bottom:5pt; }}
.mnum {{ background:{BLUE}; color:#fff; width:18pt; height:18pt; border-radius:50%; display:inline-flex;
  align-items:center; justify-content:center; font-size:8.4pt; }}
.q {{ font-weight:700; color:{INK_DK}; margin-bottom:6pt; }}
.toc li {{ display:flex; align-items:baseline; gap:8pt; margin-bottom:7.5pt; list-style:none; }}
.toc ul {{ padding:0; margin:0; }}
.toc .n {{ font-weight:700; color:{BLUE}; width:20pt; font-size:10pt; }}
.toc .t {{ color:{INK_DK}; font-weight:600; }}
.toc .d {{ flex:1; border-bottom:1px dotted #C9CED6; transform:translateY(-3pt); }}
.toc .pg {{ color:{MUTE}; font-size:9pt; }}
.toc .grp {{ font-size:8pt; letter-spacing:.14em; text-transform:uppercase; color:{MANGO}; font-weight:700; margin:11pt 0 6pt; }}
.foot-note {{ position:absolute; left:17mm; right:17mm; bottom:8mm; font-size:7.6pt; color:{MUTE};
  border-top:1px solid {RULE}; padding-top:5pt; }}
table.reg {{ width:100%; border-collapse:collapse; font-size:8.7pt; }}
table.reg th,table.reg td {{ border:1px solid {RULE}; padding:5pt 7pt; text-align:left; vertical-align:top; }}
table.reg th {{ background:{BLUE_BG}; color:{INK_DK}; font-size:8pt; text-transform:uppercase; letter-spacing:.04em; }}
a {{ color:{BLUE}; text-decoration:none; word-break:break-word; }}
.rc-hero {{ position:absolute; left:17mm; right:17mm; bottom:13mm; display:flex; justify-content:center; align-items:flex-end; }}
.rc-hero svg {{ filter:drop-shadow(0 6pt 14pt rgba(20,23,28,.06)); }}
.div-hero {{ display:flex; justify-content:center; margin-top:14pt; }}
.div-hero svg {{ filter:drop-shadow(0 8pt 18pt rgba(20,23,28,.07)); }}
.cover-band {{ position:absolute; left:0; right:0; top:0; height:15mm; background:{BLUE}; }}
.cover-foot {{ position:absolute; left:0; right:0; bottom:0; height:9mm; background:{DARK_BG}; }}
.divwrap {{ position:absolute; inset:0; padding:34mm 22mm; display:flex; flex-direction:column; }}
"""

def rh(section):
    return ('<div class="rh"><span class="brand">The Family Dessert Kitchen</span>'
            '<span class="sec">%s</span></div>') % section

def content_page(section, inner, foot=None, cls="", bookmark=None, level=1):
    f = ('<div class="foot-note">%s</div>' % foot) if foot else ""
    add_page('<div class="page %s">%s%s%s</div>' % (cls, rh(section), inner, f),
             bookmark=bookmark, level=level)

# ---------------------------------------------------------------- helper blocks
def panel(cls, title_icon, title, body):
    h = ('<h4>%s%s</h4>' % (title_icon, title)) if title else ""
    return '<div class="panel %s">%s%s</div>' % (cls, h, body)

def mission(num, tag, question, answer_html):
    return ('<div class="mission"><div class="mtag"><span class="mnum">%s</span>%s</div>'
            '<div class="q">%s</div>%s</div>') % (num, tag, question, answer_html)

def ckrow_group(items):  # items: list of (name,label)
    return '<div>%s</div>' % "".join(checkline(n,l) for n,l in items)

def wlines(prefix, n, w_mm=176, h_mm=8.6):
    return "".join(field("%s_%d"%(prefix,i+1),"text",w_mm,h_mm)+'<div class="wsp"></div>' for i in range(n))

# ================================================================= COVER
def build_cover():
    cover_art = ('<div style="position:absolute; right:15mm; top:170mm; width:120mm; transform:rotate(-2.5deg);">'
      + art.hero("cup", 6, w=120)
      + '</div>'
      + '<div style="position:absolute; left:20mm; top:200mm; width:78mm; transform:rotate(3deg);">'
      + art.hero("pop", 1, w=78) + '</div>')
    inner = f'''<div class="cover-band"></div><div class="cover-foot"></div>
    <div class="divwrap" style="padding:24mm 20mm;">
      <div class="eyebrow">Body Recomp Bible · Independent Companion</div>
      <div style="height:64mm"></div>
      <div class="serif" style="font-size:45pt; line-height:1.02; color:{INK_DK}; font-weight:700; letter-spacing:-1pt;">
        The Family<br>Dessert Kitchen</div>
      <div style="height:7mm"></div>
      <div style="font-size:15pt; color:{BLUE}; font-weight:600; max-width:120mm;">
        A Playful Guide to Cooking, Tasting &amp; Learning Together</div>
      <div style="height:4mm"></div>
      <p class="mute" style="max-width:96mm; font-size:10.5pt;">Thirty-two family desserts, safety missions, a Flavor Lab,
        and a Nutrition Explorer — for children about 5–12 and the adults who cook with them.</p>
      {cover_art}
      <div style="flex:1"></div>
      <div style="display:flex; justify-content:space-between; align-items:flex-end;">
        <div><div class="eyebrow" style="color:{MUTE}">By</div>
          <div class="serif" style="font-size:19pt; color:{INK_DK}; font-weight:700;">Cristy Sim</div></div>
        <div style="text-align:right;">{DEV_STAMP}</div></div>
    </div>'''
    add_page('<div class="page">%s</div>' % inner, bookmark="Cover")

# ================================================================= TITLE / STATUS
def build_title():
    inner = f'''<div class="eyebrow">About this companion</div>
    <h1 class="h-lg serif" style="margin-top:6pt">An independent companion book</h1>
    <hr class="rule-blue">
    <p>This is a standalone companion to the Body Recomp Bible editorial world. <b>It is not one of the five
       canonical Body Recomp Bible volumes.</b> It borrows the calm, practical, non-shaming voice and the minimal
       visual system of <i>The Recomp Kitchen</i> — white pages, charcoal type, one clear blue accent — then adds a
       playful register for young cooks.</p>
    {panel("p-blue", IC["heart"], "The kitchen rule",
      '<p style="margin:0">Dessert does not need to dress up as medicine. It can offer flavor, connection, and kitchen '
      'practice. No food is a reward, and no child has to earn something sweet.</p>')}
    <div class="grid2">
      {panel("p-soft","","Who it is for",
        '<p class="small" style="margin:0">Families with children about <b>5–12</b> and their adult caregivers. Adults '
        'stay responsible for heat, knives, appliances, allergens, food safety, and age-appropriate textures.</p>')}
      {panel("p-soft","","Who needs extra guidance",
        '<p class="small" style="margin:0">Children under 5, and any child with swallowing, developmental, allergy, or '
        'medical needs, require individualized adult and professional guidance. This book does not replace it.</p>')}
    </div>
    {panel("p-dark","", "",
      '<h4 style="color:#fff">Development status — please read</h4>'
      '<p style="margin:0 0 6pt">Every recipe here is a development draft. Recipes have <b>not</b> been kitchen-tested, '
      'and this book publishes no calories, macros, verified yields, or shelf-life. Before anything here could be called '
      'final it must pass: kitchen testing · sensory testing · standardized ingredient weights · verified yield · allergen '
      'review · food-safety review · storage validation · pediatric or qualified nutrition review · and Cristy Sim’s final '
      'approval.</p><p style="margin:0" class="small">Nothing in this book is described as final, tested, approved, or '
      'publication-ready.</p>')}
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4pt;">
      <div class="serif" style="font-size:13pt; color:{INK_DK}; font-weight:700;">The Family Dessert Kitchen</div>
      <div class="mute small">Cristy Sim · Development Edition</div></div>'''
    content_page("About", inner, bookmark="About & Development Status")

# ================================================================= TABLE OF CONTENTS
TOC_ENTRIES = []  # filled after layout is known; we render placeholders then fix page nums via bookmarks
def build_toc(entries):
    def row(n,t): return f'<li><span class="n">{n}</span><span class="t">{t}</span><span class="d"></span></li>'
    groups = [
      ("Getting Started", [("1","Welcome to the Family Dessert Kitchen"),("2","How to Use This Book"),
        ("3","Adult Safety Guide"),("4","Meet the Dessert Detectives")]),
      ("The Recipes", [("5","Frozen & Fruity"),("6","Yogurt, Pudding & Creamy Cups"),
        ("7","Muffins, Bites & Small Bakes"),("8","Warm Fruit Desserts"),
        ("9","Cookies, Bars & Squares"),("10","Build-Your-Own Family Desserts")]),
      ("Learn & Play", [("11","Flavor Lab"),("12","Nutrition Explorer"),("13","Kitchen Games & Challenges")]),
      ("Test & Celebrate", [("14","Recipe Testing Journal"),("15","Dessert Detectives Final Challenge"),
        ("16","Answer Key & Certificate"),("17","Editorial Status, Safety Notes & Sources")]),
    ]
    body = '<div class="toc">'
    for g,items in groups:
        body += f'<div class="grp">{g}</div><ul>' + "".join(row(n,t) for n,t in items) + "</ul>"
    body += "</div>"
    inner = f'''<div class="eyebrow">Contents</div>
    <h1 class="h-lg serif" style="margin-top:6pt">What is inside</h1><hr class="rule-blue">
    <p class="mute small" style="margin-bottom:4pt">Seventeen sections: get set up safely, cook thirty-two desserts,
      then learn, play, and test together. Use the bookmarks panel of your PDF reader to jump to any section.</p>
    {body}'''
    content_page("Contents", inner, bookmark="Contents")

# ================================================================= WELCOME
def build_welcome():
    inner = f'''<div class="eyebrow">Section 1</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Welcome to the Family Dessert Kitchen</h1>
    <hr class="rule-blue">
    <p style="font-size:11.4pt; max-width:150mm">This book starts with a simple idea: <b>dessert can be a pleasant,
      predictable part of family life.</b> There is no need to hide ingredients, turn every recipe into a nutrition
      promise, or ask a child to earn something sweet. The recipes use familiar ingredients and small, real tasks so
      children can genuinely take part — while an adult stays in charge of the parts that need care.</p>
    <div class="grid2">
      {panel("p-mango", IC["star"], "For the young cook",
        '<ul class="clean small" style="margin:0"><li>You are a real cook here, not a helper.</li>'
        '<li>You get to notice, measure, mix, taste, and invent.</li>'
        '<li>You never have to finish a food or love every flavor.</li>'
        '<li>Saying &ldquo;I am done&rdquo; or &ldquo;not yet&rdquo; is allowed.</li></ul>')}
      {panel("p-blue", IC["shield"], "For the adult",
        '<ul class="clean small" style="margin:0"><li>You handle heat, knives, appliances, and allergens.</li>'
        '<li>You choose safe sizes and textures for your child.</li>'
        '<li>You keep the mood calm — no bargaining over bites.</li>'
        '<li>You decide what fits your family and your kitchen.</li></ul>')}
    </div>
    {panel("p-soft", IC["magnify"], "How this book teaches",
      '<p style="margin:0" class="small">Every recipe carries a small <b>learning activity</b> — a thing to notice, '
      'compare, count, or smell. The goal is curiosity and skill, never pressure to eat. Alongside the recipes you will '
      'find a Flavor Lab, a Nutrition Explorer, kitchen games, and a testing journal, all built around the same idea: '
      '<b>cooking is a wonderful way to learn.</b>')}
    {panel("p-dark","", "", '<h4 style="color:#fff">A note on words we do not use</h4>'
      '<p style="margin:0" class="small">You will not see foods called clean, dirty, good, bad, guilt-free, or sinful. '
      'Food gives the body energy and building blocks; it is not a moral test. We describe flavor and texture instead — '
      'creamy, tart, warm, crunchy — because those are the words that help a young cook grow.</p>')}'''
    content_page("Welcome", inner, bookmark="1 · Welcome")

# ================================================================= HOW TO USE (2pp)
def build_howto():
    inner1 = f'''<div class="eyebrow">Section 2</div>
    <h1 class="h-xl serif" style="margin-top:5pt">How to Use This Book</h1><hr class="rule-blue">
    <p>Each recipe page follows the same shape, so once you learn one, you know them all. Here is what every panel means.</p>
    <div class="grid2">
      {panel("p-soft","","① Header & status",
        '<p class="small" style="margin:0">The recipe number, chapter, title, an estimated yield, and an estimated time. '
        'A dark <b>Development Recipe</b> stamp is a promise that this formula still needs testing.</p>')}
      {panel("p-soft","","② What you need",
        '<p class="small" style="margin:0">Ingredients in US measures with an <span class="metric">estimated metric</span> '
        'next to each. Metric weights are approximate until we weigh every ingredient during testing.</p>')}
      {panel("p-soft","","③ Make it",
        '<p class="small" style="margin:0">Numbered steps in order. Read them together before you start and gather '
        'everything first.</p>')}
      {panel("p-soft","","④ Roles",
        '<p class="small" style="margin:0"><b>The Child Can</b> (mango) and <b>The Adult Handles</b> (blue) split the job '
        'so everyone is safe and busy.</p>')}
      {panel("p-soft","","⑤ Flavor, allergens & age",
        '<p class="small" style="margin:0">A flavor-and-texture note, <b>allergens to check</b>, and age &amp; texture '
        'guidance. Always read labels yourself.</p>')}
      {panel("p-soft","","⑥ Learn, swap & test",
        '<p class="small" style="margin:0">One learning activity, one optional substitution, and a <b>Test Still Needed</b> '
        'note listing what must be checked before publication.</p>')}
    </div>
    {panel("p-blue", IC["pencil"], "Writing in this book",
      '<p style="margin:0" class="small">Wherever you see a <b>line</b> or a <b>box</b>, you may write, tick, or draw. '
      'In a PDF reader many of these are fillable on screen; on paper, use a pencil. Adults can reset a printed page by '
      'printing a fresh copy.</p>')}'''
    content_page("How to Use", inner1, bookmark="2 · How to Use This Book")

    inner2 = f'''<h2 class="h-md serif">Symbols you will meet</h2><hr class="rule">
    <div class="grid2">
      <div class="panel p-mango tight"><h4>{IC["star"]} Child Can</h4><p class="small" style="margin:0">A task made for young hands.</p></div>
      <div class="panel p-blue tight"><h4>{IC["shield"]} Adult Handles</h4><p class="small" style="margin:0">Heat, blades, appliances, doneness.</p></div>
      <div class="panel p-soft tight"><h4>{IC["magnify"]} Learn</h4><p class="small" style="margin:0">Something to notice or try.</p></div>
      <div class="panel p-berry tight"><h4>{IC["badge"]} Mission</h4><p class="small" style="margin:0">A Dessert Detectives challenge.</p></div>
    </div>
    {panel("p-dark","", "", '<h4 style="color:#fff">Read this before every recipe</h4>'
      '<ul class="clean small" style="margin:0"><li style="color:#EEF2F6">An adult stays with young cooks the whole time.</li>'
      '<li style="color:#EEF2F6">Wash hands before you start and after touching raw egg.</li>'
      '<li style="color:#EEF2F6">Recipes with egg must be cooked all the way through.</li>'
      '<li style="color:#EEF2F6">Cut round or hard foods small; let hot and frozen foods reach a safe temperature.</li>'
      '<li style="color:#EEF2F6">If an allergy is diagnosed, follow your healthcare professional’s plan.</li></ul>')}
    <div class="panel p-soft"><h4>A quick family agreement</h4>
      <p class="small" style="margin-bottom:7pt">Fill this in together before you cook for the first time.</p>
      <div class="small">Our grown-up helper today is {field("hu_adult","text",70)} and our young cook is {field("hu_child","text",70)}.</div>
      <div class="small" style="margin-top:9pt">We agree that: {ckrow_group([("hu1","hands get washed first"),("hu2","the adult does the hot and sharp jobs"),("hu3","no one has to finish a food"),("hu4","we describe flavors instead of judging them")])}</div>
    </div>'''
    content_page("How to Use", inner2)

# ================================================================= ADULT SAFETY (3pp)
def build_safety():
    # page 1
    inner1 = f'''<div class="eyebrow">Section 3 · For the adult</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Adult Safety Guide</h1><hr class="rule-blue">
    <p style="max-width:150mm">Children can do a great deal in the kitchen when the risky parts are clearly an adult's
      job. This guide is written for you, the caregiver. Read it once before you begin, and keep the calm, matter-of-fact
      tone the recipes use — safety works best without fear.</p>
    <div class="grid2">
      {panel("p-blue", IC["hands"], "Supervision & hygiene",
        '<ul class="clean small" style="margin:0"><li>Stay within arm’s reach of young cooks the whole time.</li>'
        '<li>Everyone washes hands with soap and warm water before cooking, after handling raw egg, and after using the '
        'bathroom or touching pets.</li><li>Tie back hair, roll up sleeves, and wipe surfaces before you start.</li>'
        '<li>Keep raw egg away from foods that will not be cooked.</li></ul>')}
      {panel("p-mango", IC["flame"], "Heat & burn prevention",
        '<ul class="clean small" style="margin:0"><li>The adult manages the oven, stove, and anything hot.</li>'
        '<li>Turn pot handles inward; use dry oven mitts.</li>'
        '<li>Let baked and warm desserts cool from hot to warm before a child tastes them.</li>'
        '<li>Baked fruit and its juices hold heat — cool well and check before serving.</li></ul>')}
    </div>
    <div class="grid2">
      {panel("p-orange", IC["whisk"], "Knives, blenders & appliances",
        '<ul class="clean small" style="margin:0"><li>The adult does all cutting and runs blenders and food processors.</li>'
        '<li>Unplug appliances before scraping the jar; keep fingers away from blades.</li>'
        '<li>Give children safe tools instead: spoons, whisks, cups, mashers, and clean hands.</li></ul>')}
      {panel("p-leaf", IC["shield"], "Perishables & doneness",
        '<ul class="clean small" style="margin:0"><li>Keep yogurt, milk, and egg mixtures cold until use; do not leave them '
        'out on the counter.</li><li>Cook every egg-containing recipe fully — no wet or runny centers.</li>'
        '<li>Serve freshly; this draft does not provide validated storage times.</li></ul>')}
    </div>
    {panel("p-dark","","",'<h4 style="color:#fff">If you remember only one thing</h4>'
      '<p style="margin:0" class="small">You decide what is safe for <i>your</i> child today — the right size, the right '
      'texture, the right amount of help. When in doubt, make the piece smaller, the task simpler, and the supervision closer.</p>')}'''
    content_page("Safety", inner1, bookmark="3 · Adult Safety Guide")

    # page 2 — choking, texture, allergens
    inner2 = f'''<h2 class="h-md serif">Choking, texture &amp; age</h2><hr class="rule">
    <p class="small">Match every piece and consistency to your child's skills. The foods below are common choking hazards
      for young children and need adult judgment — cut small, modify the texture, or leave out.</p>
    <div class="grid2">
      {panel("p-berry","","Cut, modify, or skip for the young",
        '<ul class="clean small" style="margin:0"><li>Whole or round fruit — quarter grapes and berries lengthwise.</li>'
        '<li>Whole nuts and hard, dense pieces.</li><li>Thick, sticky spoonfuls of nut or seed butter — spread thin.</li>'
        '<li>Large chunks of dried fruit such as raisins — chop or omit for the very young.</li>'
        '<li>Hard, still-frozen pieces — let soften first.</li></ul>')}
      {panel("p-blue","","Build safer textures",
        '<ul class="clean small" style="margin:0"><li>Blend, mash, or finely chop to suit the child.</li>'
        '<li>Thin nut or seed butter with yogurt or milk.</li><li>Serve pops and bark once slightly softened.</li>'
        '<li>Offer water alongside; children eat seated and calm, never while walking or playing.</li></ul>')}
    </div>
    {panel("p-soft", IC["magnify"], "Allergens: name them, do not guess",
      '<p class="small" style="margin:0 0 5pt">Read <b>every label, every time.</b> A substitution changes flavor, structure, '
      '<b>and</b> the allergen profile. Recipes list allergens to check, but brands vary — the label is the authority. '
      'Common allergens to watch in this book include milk, egg, wheat (via oats with cross-contact), tree nuts, peanuts, '
      'soy, and seeds.</p>'
      '<p class="small" style="margin:0">If your child has a <b>diagnosed</b> allergy, follow the plan from your family’s '
      'healthcare professional. This book cannot replace that plan.</p>')}
    {panel("p-dark","","",'<h4 style="color:#fff">Oats &amp; cross-contact</h4>'
      '<p style="margin:0" class="small">Oats are naturally wheat-free but are often processed near wheat. If wheat is a '
      'concern, choose oats labeled to address cross-contact and confirm on the package.</p>')}'''
    content_page("Safety", inner2)

    # page 3 — safe-tool ID interactive (bridges to Detectives)
    tools = [("Spoon","safe"),("Whisk","safe"),("Measuring cups","safe"),("Mixing bowl","safe"),
             ("Sharp knife","adult"),("Blender","adult"),("Hot oven","adult"),("Stovetop","adult")]
    cards = ""
    for name,who in tools:
        icon = IC["whisk"] if who=="safe" else IC["flame"]
        cards += (f'<div class="panel {"p-mango" if who=="safe" else "p-blue"} tight" style="margin:0">'
                  f'<div style="display:flex; align-items:center; gap:8pt;"><span class="icwrap" '
                  f'style="width:26pt;height:26pt;background:#fff">{icon}</span><b class="small">{name}</b></div>'
                  f'<div class="small" style="margin-top:6pt">Who uses it? '
                  f'{checkline(f"tool_{name[:4]}_c","Child")}{checkline(f"tool_{name[:4]}_a","Adult")}</div></div>')
    inner3 = f'''<h2 class="h-md serif">Warm-up mission: Safe-Tool Sort</h2><hr class="rule">
    <p class="small">Do this together before your first recipe. For each tool, tick who should use it. Then check your
      answers against the guide above. <b>Hint:</b> anything hot, sharp, or electric is an adult tool.</p>
    <div class="grid2" style="gap:9pt">{cards}</div>
    {panel("p-soft","","Talk about it",
      '<p class="small" style="margin:0">Ask your child: &ldquo;What could go wrong if this were a child’s job? What safe '
      'tool could we use instead?&rdquo; The answers below become second nature with practice.</p>')}
    <div class="panel p-berry"><b class="small">Child tools:</b> <span class="small">spoon, whisk, measuring cups, mixing bowl.
      &nbsp; <b>Adult tools:</b> sharp knife, blender, hot oven, stovetop.</span></div>'''
    content_page("Safety", inner3)

# ================================================================= MEET THE DETECTIVES
def build_detectives_intro():
    inner = f'''<div class="eyebrow">Section 4</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Meet the Dessert Detectives</h1><hr class="rule-blue">
    <div class="flexrow">
      <div style="flex:1">
        <p>A Dessert Detective is a young cook who <b>notices things.</b> Detectives do not judge food as good or bad —
          they investigate flavor, texture, aroma, color, and safety. Throughout this book you will find numbered
          <b>missions</b>. Some are quick questions; some ask you to draw, measure, or invent.</p>
        <p class="small mute" style="margin-bottom:0">There are no rewards for eating and no punishments for leaving food.
          The reward is learning something together.</p>
      </div>
      <div style="flex:none; width:120pt;" class="center">
        <span class="icwrap" style="width:96pt;height:96pt;background:{BLUE_BG}">{svg(IC_BODY_DETECTIVE, w=64, h=64)}</span>
        <div class="small" style="margin-top:6pt; font-weight:700; color:{BLUE}">Detective Badge</div>
      </div>
    </div>
    <div class="grid3" style="margin-top:4pt">
      {panel("p-mango","","The Detective Code",
        '<ul class="clean small" style="margin:0"><li>I wash my hands first.</li><li>I notice before I decide.</li>'
        '<li>I use kind, curious words.</li></ul>')}
      {panel("p-blue","","My Detective Powers",
        '<ul class="clean small" style="margin:0"><li>Looking closely</li><li>Smelling carefully</li>'
        '<li>Measuring exactly</li><li>Describing clearly</li></ul>')}
      {panel("p-berry","","My Superpower",
        '<p class="small" style="margin:0">Saying &ldquo;I am done,&rdquo; &ldquo;I want to try,&rdquo; or &ldquo;not that '
        'texture yet&rdquo; is real detective skill, too.</p>')}
    </div>
    <div class="panel p-soft"><h4>{IC["badge"]} Become a Detective</h4>
      <div class="small">My detective name is {field("det_name","text",78)} and today's date is {field("det_date","text",50)}.</div>
      <div class="small" style="margin-top:9pt">I promise to investigate with curiosity and kindness. Signed: {field("det_sign","text",90)}</div>
      <div class="small" style="margin-top:11pt">Track your missions as you go — there are <b>fourteen</b> to collect:</div>
      <div style="margin-top:6pt">{"".join(field(f"track_{i}","check",6.5,6.5)+'<span class="small" style="margin:0 9pt 0 3pt">%d</span>'%(i) for i in range(1,15))}</div>
    </div>'''
    content_page("Detectives", inner, bookmark="4 · Meet the Dessert Detectives")

# a simple detective figure (magnifier + hat) built inline
IC_BODY_DETECTIVE = ('<circle cx="24" cy="24" r="22" fill="none"/>'
  '<path d="M8 18c2-6 8-9 16-9s14 3 16 9z" fill="%s"/>'  # hat brim area
  '<rect x="14" y="6" width="20" height="9" rx="4" fill="%s"/>'
  '<circle cx="20" cy="27" r="8" fill="none" stroke="%s" stroke-width="3"/>'
  '<line x1="26" y1="33" x2="34" y2="41" stroke="%s" stroke-width="3.4" stroke-linecap="round"/>'
  '<circle cx="20" cy="27" r="4" fill="%s" opacity=".35"/>') % (BLUE, INK_DK, INK_DK, INK_DK, MANGO)

# ================================================================= CHAPTER DIVIDER
CH_META = {
 5:(IC["pop"], MANGO, MANGO_BG, "Cool it down. Blend, freeze, and scrape fruit into pops, bark, and creamy chills."),
 6:(IC["cup"], BERRY, BERRY_BG, "Spoonable and smooth. Yogurt, chia, and blended creams in little cups."),
 7:(IC["muffin"], ORANGE, ORANGE_BG, "Little bakes and no-bake bites — perfect for small hands and quick wins."),
 8:(IC["apple"], ORANGE, ORANGE_BG, "Fruit meets gentle heat. Soft, cozy, and fragrant with warm spice."),
 9:(IC["cookie"], LEAF, LEAF_BG, "Soft cookies, fudgy squares, and chewy bars built on oats and fruit."),
 10:(IC["bowl"], BLUE, BLUE_BG, "You are the recipe designer. Set up a station and let everyone build their own."),
}
def chapter_divider(chap):
    icon,accent,bg,blurb = CH_META[chap]
    rlist = [r for r in RECIPES if r["chap"]==chap]
    items = "".join(f'<li><span class="n">{r["n"]:02d}</span><span class="t">{r["title"]}</span></li>' for r in rlist)
    inner = f'''<div class="divwrap">
      <div class="eyebrow" style="color:{accent}">Chapter {chap}</div>
      <div style="display:flex; align-items:center; gap:16pt; margin-top:8pt;">
        <span class="icwrap" style="width:74pt;height:74pt;background:{bg}">{svg(icon,w=48,h=48)}</span>
        <h1 class="serif" style="font-size:34pt; letter-spacing:-.6pt;">{CH[chap]}</h1>
      </div>
      <div style="height:3mm"></div>
      <div style="height:2.4pt; width:60pt; background:{accent}; border-radius:2pt;"></div>
      <p style="font-size:12.5pt; max-width:150mm; margin-top:12pt; color:{INK};">{blurb}</p>
      <div class="panel p-soft toc" style="margin-top:14pt; max-width:150mm;">
        <div class="grp" style="color:{accent}; margin-top:0">In this chapter</div>
        <ul style="columns:2; column-gap:24pt;">{items}</ul>
      </div>
      <div class="div-hero">{art.hero(CH_HERO[chap][0], CH_HERO[chap][1], w=158)}</div>
      <div style="flex:1"></div>
      <div>{DEV_STAMP}<span class="mute small" style="margin-left:10pt">Every recipe here still requires kitchen testing.</span></div>
    </div>'''
    add_page('<div class="page">%s</div>' % inner, bookmark=f"{chap} · {CH[chap]}")

CH_HERO = {5:("pop",1), 6:("cup",6), 7:("muffin",12), 8:("apple",16), 9:("cookie",21), 10:("bowl",26)}

# ================================================================= RECIPE PAGE
def recipe_page(r):
    icon,accent,bg,_ = CH_META[r["chap"]]
    ings = "".join(f'<li>{us} <span class="metric">({m})</span></li>' for us,m in r["ingredients"])
    steps = "".join(f'<li>{s}</li>' for s in r["steps"])
    meta = f'''<div class="metaline">
      <div class="r"><span class="k">Flavor &amp; texture</span><span>{r["flavor"]}</span></div>
      <div class="r"><span class="k">Allergens to check</span><span>{r["allergens"]}</span></div>
      <div class="r"><span class="k">Age &amp; texture</span><span>{r["age"]}</span></div>
    </div>'''
    learn = f'''<div class="panel p-soft tight" style="margin:8pt 0 0"><h4 class="small">{IC["magnify"]} Learn together</h4>
      <p class="small" style="margin:0">{r["activity"]}</p></div>'''
    sub = f'''<div class="panel p-leaf tight" style="margin:7pt 0 0"><span class="small"><b>Try a swap:</b> {r["sub"]}</span></div>'''
    test = f'''<div class="panel p-berry tight" style="margin:7pt 0 0"><span class="small"><b>Test still needed:</b> {r["test"]}</span></div>'''
    inner = f'''
    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
      <div style="display:flex; align-items:center; gap:10pt;">
        <span class="icwrap" style="width:40pt;height:40pt;background:{bg}">{svg(icon,w=26,h=26)}</span>
        <div><div class="eyebrow" style="color:{accent}">Recipe {r["n"]:02d} · {CH[r["chap"]]}</div>
          <div class="rc-title serif">{r["title"]}</div></div>
      </div>
      <div style="text-align:right; flex:none;">{DEV_STAMP}</div>
    </div>
    <div class="rc-sub">{IC_CLOCK} &nbsp;<b>Estimated time</b> {r["time"]} &nbsp; · &nbsp; <b>Estimated yield</b> {r["yield_"]}</div>
    <div class="panel p-soft tight" style="margin:9pt 0 2pt; border-left:3pt solid {DARK_BG}">
      <span class="small">Do not publish or assign nutrition values before testing flavor, cooking, yield, allergens, and storage.</span></div>
    <div class="rc-two">
      <div>
        <h4 class="small" style="text-transform:uppercase; letter-spacing:.08em; color:{accent}; margin-bottom:5pt;">What you need</h4>
        <ul class="clean small">{ings}</ul>
        <h4 class="small" style="text-transform:uppercase; letter-spacing:.08em; color:{accent}; margin:10pt 0 5pt;">Make it</h4>
        <ol class="steps small">{steps}</ol>
        <div class="rolebox role-child"><h4>{IC["star"]} The child can</h4><span class="small">{r["child"]}</span></div>
        <div class="rolebox role-adult"><h4>{IC["shield"]} The adult handles</h4><span class="small">{r["adult"]}</span></div>
      </div>
      <div>{meta}{learn}{sub}{test}</div>
    </div>
    <div class="panel p-blue tight" style="margin-top:9pt; display:flex; align-items:center; gap:14pt;">
      <span class="small">{checkline("made_%d"%r["n"],"<b>We made this!</b>")}</span>
      <span class="small" style="flex:1">One thing we noticed: {field("notice_%d"%r["n"],"text",92)}</span>
    </div>
    <div class="rc-hero">{art.hero(r["icon"], r["n"], w=96)}</div>'''
    content_page(CH[r["chap"]], inner)

IC_CLOCK = svg('<circle cx="24" cy="24" r="18" fill="none" stroke="%s" stroke-width="3"/>'
  '<path d="M24 14v11l7 4" stroke="%s" stroke-width="3" fill="none" stroke-linecap="round"/>'%(BLUE,BLUE), w=13,h=13)

# ---- radial descriptor wheel (decorative + labeled segments)
import math
def wheel(words, colors, title):
    cx=cy=95; r_out=88; r_in=40; n=len(words); segs=""; labs=""
    for i,w in enumerate(words):
        a0=(i/n)*2*math.pi - math.pi/2; a1=((i+1)/n)*2*math.pi - math.pi/2
        col=colors[i%len(colors)]
        x0=cx+r_out*math.cos(a0); y0=cy+r_out*math.sin(a0)
        x1=cx+r_out*math.cos(a1); y1=cy+r_out*math.sin(a1)
        xi0=cx+r_in*math.cos(a0); yi0=cy+r_in*math.sin(a0)
        xi1=cx+r_in*math.cos(a1); yi1=cy+r_in*math.sin(a1)
        segs+=(f'<path d="M{x0:.1f} {y0:.1f} A{r_out} {r_out} 0 0 1 {x1:.1f} {y1:.1f} '
               f'L{xi1:.1f} {yi1:.1f} A{r_in} {r_in} 0 0 0 {xi0:.1f} {yi0:.1f} Z" '
               f'fill="{col}" stroke="#fff" stroke-width="2"/>')
        am=(a0+a1)/2; rl=(r_out+r_in)/2
        lx=cx+rl*math.cos(am); ly=cy+rl*math.sin(am)
        labs+=(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="9" font-weight="700" fill="#12151A" '
               f'text-anchor="middle" dominant-baseline="middle">{w}</text>')
    return (f'<svg width="190" height="190" viewBox="0 0 190 190" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{title}">{segs}{labs}'
            f'<circle cx="{cx}" cy="{cy}" r="{r_in-4}" fill="#fff"/>'
            f'<text x="{cx}" y="{cy-4}" font-size="10" font-weight="700" fill="#1B6FEF" text-anchor="middle">FLAVOR</text>'
            f'<text x="{cx}" y="{cy+9}" font-size="10" font-weight="700" fill="#1B6FEF" text-anchor="middle">WHEEL</text></svg>')

# ================================================================= FLAVOR LAB (4pp)
def build_flavorlab():
    # p1 intro + five words + opinion
    five = [("fl_creamy","Creamy"),("fl_crunchy","Crunchy"),("fl_soft","Soft"),("fl_cold","Cold"),
            ("fl_warm","Warm"),("fl_sweet","Sweet"),("fl_tart","Tart"),("fl_smooth","Smooth"),
            ("fl_juicy","Juicy"),("fl_chewy","Chewy")]
    inner1 = f'''<div class="eyebrow" style="color:{BERRY}">Section 11 · Learn &amp; Play</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Flavor Lab</h1><hr class="rule-blue">
    <p style="max-width:152mm">You do not have to love every flavor. The mission is to <b>notice.</b> A Flavor Lab
      scientist describes what they taste and feel — without calling it good or bad. Pick any dessert you made and
      investigate it here.</p>
    {mission(1,"Mission · Five Words",
      "Which words describe your dessert? Tick all that fit — there is no wrong answer.",
      ckrow_group(five))}
    {mission(2,"Mission · My Opinion Counts",
      "Finish each sentence in your own words. Remember: describe, do not judge.",
      f'<div class="small">The texture feels {field("op_tex","text",120)}</div>'
      f'<div class="wsp"></div><div class="small">The aroma reminds me of {field("op_aroma","text",112)}</div>'
      f'<div class="wsp"></div><div class="small">Next time I would try {field("op_next","text",118)}</div>')}
    {panel("p-dark","","",'<h4 style="color:#fff">Scientist’s reminder</h4>'
      '<p style="margin:0" class="small">Being able to say &ldquo;I am done,&rdquo; &ldquo;I want to try,&rdquo; or &ldquo;I '
      'do not like that texture yet&rdquo; is also part of learning. Your opinion counts, and it can change over time.</p>')}'''
    content_page("Flavor Lab", inner1, bookmark="11 · Flavor Lab")

    # p2 wheels
    fwheel = wheel(["Sweet","Tart","Fruity","Nutty","Warm-spice","Cocoa"],
                   [MANGO,BERRY,ORANGE,"#C9895A",ORANGE,"#7A4B2B"], "Flavor wheel")
    twords = [("tw_creamy","Creamy"),("tw_crunchy","Crunchy"),("tw_chewy","Chewy"),("tw_smooth","Smooth"),
              ("tw_fluffy","Fluffy"),("tw_icy","Icy"),("tw_sticky","Sticky"),("tw_juicy","Juicy")]
    inner2 = f'''<h2 class="h-md serif">Flavor &amp; Texture Wheels</h2><hr class="rule">
    <p class="small">A wheel helps you find the right word. Point to a slice, say it out loud, then decide if your dessert
      belongs there. Colour in the slices that match today's dessert.</p>
    {mission(3,"Mission · Flavor Wheel","Which slice best matches your dessert's <b>flavor</b>? Circle it on the wheel, then write it below.",
      f'<div style="display:flex; gap:16pt; align-items:center;"><div>{fwheel}</div>'
      f'<div style="flex:1"><div class="small">My dessert’s main flavor is {field("fw_main","text",70)}</div>'
      f'<div class="wsp"></div><div class="small">A second flavor I notice is {field("fw_second","text",66)}</div>'
      f'<div class="wsp"></div><div class="small">It reminds me of {field("fw_remind","text",78)}</div></div></div>')}
    {mission(4,"Mission · Texture Wheel","Texture is how food <b>feels</b>. Tick every texture you can find in today’s dessert.",
      ckrow_group(twords))}'''
    content_page("Flavor Lab", inner2)

    # p3 aroma & texture vocabulary
    inner3 = f'''<h2 class="h-md serif">Aroma &amp; Texture Vocabulary</h2><hr class="rule">
    <p class="small">Great cooks collect words. Here is a word bank — borrow from it, then add your own.</p>
    <div class="grid2">
      {panel("p-mango","","Aroma words (how it smells)",
        '<p class="small" style="margin:0">fresh · fruity · toasty · warm · sweet · citrusy · nutty · spiced · vanilla-like · cool</p>')}
      {panel("p-blue","","Texture words (how it feels)",
        '<p class="small" style="margin:0">creamy · crunchy · chewy · smooth · fluffy · icy · soft · juicy · sticky · silky</p>')}
    </div>
    {mission(5,"Mission · Smell First",
      "Before you taste, smell your dessert. Write three aroma words, then invent one brand-new word of your own.",
      f'<div class="small">Aroma word 1: {field("ar1","text",50)} &nbsp; 2: {field("ar2","text",50)} &nbsp; 3: {field("ar3","text",50)}</div>'
      f'<div class="wsp"></div><div class="small">My invented word for this smell is {field("ar_new","text",70)} '
      f'and it means {field("ar_mean","text",70)}</div>')}
    {panel("p-soft", IC["magnify"], "What do you notice?",
      f'<div class="small">Colour: {field("wn_col","text",64)} &nbsp; Sound when you bite: {field("wn_sound","text",64)}</div>'
      f'<div class="wsp"></div><div class="small">Temperature: {field("wn_temp","text",64)} &nbsp; One surprise: {field("wn_surprise","text",66)}</div>')}'''
    content_page("Flavor Lab", inner3)

    # p4 one-change experiment
    inner4 = f'''<h2 class="h-md serif">One-Change-at-a-Time Lab</h2><hr class="rule">
    <p class="small">Real recipe testers change <b>one</b> thing, then taste and take notes. If you change five things at
      once, you never know which one mattered. Try it with any recipe.</p>
    {mission(6,"Mission · One Change","Plan a tiny experiment. Change only one thing.", "")}
    <div class="panel p-soft">
      <div class="small">The recipe I am testing: {field("oc_recipe","text",120)}</div><div class="wsp"></div>
      <div class="small">The <b>one</b> thing I will change: {field("oc_change","text",120)}</div><div class="wsp"></div>
      <div class="small">What I think will happen (my guess): {field("oc_guess","text",110)}</div><div class="wsp"></div>
      <div class="small">What actually happened: {field("oc_result","text",112)}</div><div class="wsp"></div>
      <div class="small">Did my guess match? {checkline("oc_yes","Yes")}{checkline("oc_no","Not this time")} &nbsp;
        Next change to try: {field("oc_next","text",70)}</div>
    </div>
    {panel("p-berry","","Best-way-to-test check",
      'If a recipe is too thick, what is the best next step? '
      + ckrow_group([("oc_a","Change five things at once"),("oc_b","Change one thing and take notes"),("oc_c","Measure nothing")]))}
    <p class="tiny mute">Answer in the Answer Key. Hint: scientists like to know exactly what made the difference.</p>'''
    content_page("Flavor Lab", inner4)

# ================================================================= NUTRITION EXPLORER (3pp)
def build_nutrition():
    inner1 = f'''<div class="eyebrow" style="color:{LEAF}">Section 12 · Learn &amp; Play</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Nutrition Explorer</h1><hr class="rule-blue">
    <p style="max-width:152mm">Food gives your body <b>energy</b> to run, think, and play, and different foods bring
      different <b>building blocks</b>. None of this makes a food good or bad — it just helps us understand what food does.</p>
    <div class="grid3">
      {panel("p-mango","","Carbohydrates",'<p class="small" style="margin:0">A main <b>energy</b> source. Found in fruit, oats, and grains.</p>')}
      {panel("p-orange","","Fats",'<p class="small" style="margin:0">Give <b>lasting energy</b> and carry flavor. Found in seeds, nut butters, and dairy.</p>')}
      {panel("p-blue","","Proteins",'<p class="small" style="margin:0">Help the body <b>build and repair</b>. Found in yogurt, milk, eggs, and seeds.</p>')}
    </div>
    {mission(7,"Mission · Match the Building Block",
      "Draw a line, or write the letter, matching each food to a block it brings. (Some foods bring more than one!)",
      f'<div class="grid2"><div class="small"><b>Foods</b><br>'
      f'A. Oats &nbsp; B. Yogurt &nbsp; C. Sunflower seed butter &nbsp; D. Banana</div>'
      f'<div class="small"><b>Blocks</b><br>'
      f'{field("nm_carb","text",42)} Carbohydrate<br>{field("nm_prot","text",42)} Protein<br>{field("nm_fat","text",42)} Fat</div></div>')}
    {panel("p-dark","","",'<h4 style="color:#fff">A calm truth</h4>'
      '<p style="margin:0" class="small">Your body is smart. It uses energy and building blocks from <b>all</b> kinds of '
      'foods. One dessert does not need to do a special job — it can simply taste good and be part of your day.</p>')}'''
    content_page("Nutrition Explorer", inner1, bookmark="12 · Nutrition Explorer")

    inner2 = f'''<h2 class="h-md serif">Different foods, different gifts</h2><hr class="rule">
    <p class="small">Each kind of food brings its own <b>flavors, colors, and textures.</b> Explore what each group adds —
      this is about curiosity, not rules.</p>
    <div class="grid2">
      {panel("p-berry","","Fruit",'<p class="small" style="margin:0">Sweetness, bright color, and juice. Think mango, berries, apple, pear.</p>')}
      {panel("p-mango","","Grains &amp; oats",'<p class="small" style="margin:0">Chew, structure, and a toasty smell. Think oats and oat flour.</p>')}
      {panel("p-blue","","Dairy or alternatives",'<p class="small" style="margin:0">Creaminess and cool, smooth texture. Think yogurt and milk (dairy or plant).</p>')}
      {panel("p-leaf","","Seeds",'<p class="small" style="margin:0">A little richness and gentle crunch. Think chia and sunflower seed butter.</p>')}
    </div>
    {mission(8,"Mission · Notice the Group",
      "Pick one dessert you made. Which groups did it use, and what did each one add?",
      f'<div class="small">My dessert: {field("ng_dish","text",120)}</div><div class="wsp"></div>'
      f'<div class="small">Groups I can spot: {checkline("ng_fruit","Fruit")}{checkline("ng_grain","Grains")}{checkline("ng_dairy","Dairy/alt")}{checkline("ng_seed","Seeds")}</div>'
      f'<div class="wsp"></div><div class="small">The creamiest part came from {field("ng_cream","text",64)} and the crunch came from {field("ng_crunch","text",52)}</div>')}
    {panel("p-soft","","Hunger &amp; fullness change",
      '<p class="small" style="margin:0">Some days you are hungrier than others — that is normal. Your body sends signals. '
      'Eating slowly helps you notice when you feel full. You are the expert on your own hunger.</p>')}'''
    content_page("Nutrition Explorer", inner2)

    inner3 = f'''<h2 class="h-md serif">Big ideas to grow with</h2><hr class="rule">
    <div class="grid2">
      {panel("p-blue", IC["heart"], "Dessert is not earned",'<p class="small" style="margin:0">You do not have to finish vegetables '
        'or &ldquo;be good&rdquo; to have dessert. Dessert is simply part of family life — enjoyed, not traded.</p>')}
      {panel("p-mango", IC["star"], "One food is not the whole story",'<p class="small" style="margin:0">No single food makes a '
        'person healthy or unhealthy. What matters is <b>variety over time</b>, and that grows slowly.</p>')}
      {panel("p-berry","", "Trying takes practice",'<p class="small" style="margin:0">It can take many friendly tries to warm up to a '
        'new flavor or texture. No pressure — curiosity does the work.</p>')}
      {panel("p-leaf","", "Enjoyment matters",'<p class="small" style="margin:0">Cooking and eating together builds connection. That '
        'is a real and valuable part of food, too.</p>')}
    </div>
    {mission(9,"Mission · My Food Ideas",
      "Finish these in your own words — there are no right answers.",
      f'<div class="small">A flavor I am curious about is {field("fi_flavor","text",96)}</div><div class="wsp"></div>'
      f'<div class="small">A texture I like right now is {field("fi_tex","text",100)}</div><div class="wsp"></div>'
      f'<div class="small">Something I enjoy about cooking with my family is {field("fi_enjoy","text",78)}</div>')}
    {panel("p-dark","","",'<p style="margin:0" class="small">This page teaches ideas, not medical advice. For questions about a '
      'child’s growth, diet, allergies, or health, talk with a pediatrician or a qualified nutrition professional.</p>')}'''
    content_page("Nutrition Explorer", inner3)

# ================================================================= KITCHEN GAMES (5pp)
def build_games():
    # p1 ingredient matching
    inner1 = f'''<div class="eyebrow" style="color:{ORANGE}">Section 13 · Learn &amp; Play</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Kitchen Games &amp; Challenges</h1><hr class="rule-blue">
    <p style="max-width:150mm">These games build the skills real cooks use — matching, sequencing, measuring, and spotting
      allergens. Play them any time. Adults: answers are in the Answer Key.</p>
    {mission(10,"Mission · Ingredient Match","Write the letter of the job each ingredient does in a recipe.",
      f'<div class="grid2"><div class="small"><b>Ingredient</b><br>'
      f'{field("im_1","text",30)} Frozen mango<br>{field("im_2","text",30)} Rolled oats<br>'
      f'{field("im_3","text",30)} Plain yogurt<br>{field("im_4","text",30)} Ripe banana<br>{field("im_5","text",30)} Cinnamon</div>'
      f'<div class="small"><b>Its job</b><br>A. Adds creaminess<br>B. Adds warm aroma<br>C. Gives chew and structure<br>'
      f'D. Adds natural sweetness &amp; helps bind<br>E. Freezes into a cold, fruity base</div></div>')}
    {panel("p-soft","","Detective tip",
      '<p class="small" style="margin:0">Many ingredients do <b>more than one</b> job. Banana, for example, adds sweetness '
      '<i>and</i> helps hold a cookie together. Can you find another double-job ingredient in this book?</p>')}'''
    content_page("Kitchen Games", inner1, bookmark="13 · Kitchen Games & Challenges")

    # p2 steps in order
    scrambled = ["Adult bakes until the centers are cooked","Wash our hands","Cool until just warm, then taste and notice",
                 "Mash the ripe bananas","Mix in the oats, egg, and cinnamon"]
    rows = "".join(f'<div class="small" style="margin-bottom:7pt">{field("so_%d"%i,"text",14)} &nbsp; {s}</div>'
                   for i,s in enumerate(scrambled,1))
    inner2 = f'''<h2 class="h-md serif">Put the Steps in Order</h2><hr class="rule">
    {mission(11,"Mission · Magic Order","These steps for Baked Banana Oat Bites are all mixed up. Number them 1 to 5.",
      rows)}
    {mission(0,"Quick Draw","Draw the tool you would use to mix a batter <b>without</b> touching a blade.",
      f'<div class="wbox" style="width:150mm; height:52mm; display:block">{field("draw_tool","text",1,1)}</div>')}
    <p class="tiny mute">The invisible field in the box lets a PDF reader mark it as a drawing area; on paper, just draw.</p>'''
    content_page("Kitchen Games", inner2)

    # p3 measuring & math
    def mq(q, ans_w=16): return f'<div class="small" style="margin-bottom:9pt">{q} &nbsp; {field("mm_%d"%mq.i,"text",ans_w)}</div>' if False else None
    inner3 = f'''<h2 class="h-md serif">Measuring Challenge &amp; Kitchen Math</h2><hr class="rule">
    <p class="small">Measuring is a superpower. Solve these with a grown-up. Write your answer on each line.</p>
    {mission(12,"Mission · Kitchen Math","", "")}
    <div class="panel p-soft">
      <div class="small" style="margin-bottom:9pt">1. A batch makes <b>8 pops</b>. If 2 friends share them equally, how many does each get? {field("mm_1","text",22)}</div>
      <div class="small" style="margin-bottom:9pt">2. You have <b>3 apples</b> and use <b>1</b>. How many are left? {field("mm_2","text",22)}</div>
      <div class="small" style="margin-bottom:9pt">3. A recipe needs <b>2 cups</b> of oats. Your scoop is <b>1/2 cup</b>. How many scoops? {field("mm_3","text",22)}</div>
      <div class="small" style="margin-bottom:9pt">4. Muffins bake for <b>16 minutes</b>. They have baked <b>10</b>. How many minutes are left? {field("mm_4","text",22)}</div>
      <div class="small" style="margin-bottom:0">5. You need <b>1 cup</b> yogurt but only have a <b>1/4-cup</b> measure. How many times do you fill it? {field("mm_5","text",22)}</div>
    </div>
    {panel("p-mango", IC["star"], "Measuring practice",
      f'<div class="small">Level: fill a 1-cup measure with water, then pour it into 1/2-cup measures. How many did it fill? {field("mm_pour","text",22)}</div>'
      f'<div class="wsp"></div><div class="small">What did you notice about halves and wholes? {field("mm_notice","text",78)}</div>')}'''
    content_page("Kitchen Games", inner3)

    # p4 spot the allergen
    items = [("Plain yogurt",[("sa1a","Milk"),("sa1b","Egg"),("sa1c","Wheat")]),
             ("Graham cracker crumbs",[("sa2a","Milk"),("sa2b","Wheat"),("sa2c","Seeds")]),
             ("One egg",[("sa3a","Egg"),("sa3b","Soy"),("sa3c","Milk")]),
             ("Sunflower seed butter",[("sa4a","Seeds"),("sa4b","Milk"),("sa4c","Wheat")]),
             ("Chocolate chips",[("sa5a","Milk"),("sa5b","Soy"),("sa5c","Egg")])]
    rows=""
    for name,opts in items:
        rows+=(f'<div class="small" style="margin-bottom:8pt"><b>{name}</b> — tick the allergen(s) it may involve:<br>'
               f'<span style="margin-top:3pt; display:inline-block">{ckrow_group(opts)}</span></div>')
    inner4 = f'''<h2 class="h-md serif">Spot the Allergen</h2><hr class="rule">
    <p class="small">Detectives read labels. For each ingredient, tick the allergen it <b>may</b> involve. Remember: brands
      differ, so the real label is always the final word.</p>
    {mission(13,"Mission · Label Detective","", rows)}
    {panel("p-dark","","",'<h4 style="color:#fff">Why we check every label, every time</h4>'
      'Why do we read every ingredient label? '
      + ckrow_group([("sa_why_a","To check allergens and keep everyone safe"),("sa_why_b","Because the package is pretty"),("sa_why_c","To count the colors")]))}'''
    content_page("Kitchen Games", inner4)

    # p5 detective challenge board (bingo)
    challenges = ["Name 3 textures","Smell before tasting","Measure 1 cup exactly","Wash hands first","Describe a color",
                  "Find a double-job ingredient","Spot one allergen","Say a warm word","Invent a dessert name",
                  "Notice a change from heat","Share fairly","Try one new flavor"]
    cells=""
    for i,c in enumerate(challenges):
        cells+=(f'<div class="panel p-soft tight" style="margin:0; min-height:34pt; display:flex; flex-direction:column; gap:4pt;">'
                f'<span>{field("bingo_%d"%i,"check",5.5,5.5)}</span><span class="tiny">{c}</span></div>')
    inner5 = f'''<h2 class="h-md serif">Detective Challenge Board</h2><hr class="rule">
    <p class="small">Collect these skills over many cooking days — tick a square each time you do it. Fill a whole row to
      earn a Detective star. This is about <b>doing</b>, never about how much you eat.</p>
    <div class="grid3" style="gap:8pt">{cells}</div>
    <div class="panel p-mango" style="margin-top:11pt; display:flex; align-items:center; gap:12pt;">
      <span class="small">I completed a full row! Star earned: {field("bingo_star","check",7,7)}</span>
      <span class="small" style="flex:1">My favorite challenge was {field("bingo_fav","text",78)}</span></div>'''
    content_page("Kitchen Games", inner5)

# ================================================================= BUILD-YOUR-OWN closing page
def build_byo_close():
    inner = f'''<h2 class="h-md serif">Design &amp; Name Your Own Dessert</h2><hr class="rule">
    <p class="small">You have built parfaits, bark, and warm bowls. Now invent one that is entirely yours. Draw it, name
      it, and plan how the family would build it — one change at a time.</p>
    {mission(0,"Draw Your Dessert","Sketch your creation in the frame. Add labels for each layer or part.",
      f'<div class="wbox" style="width:150mm; height:66mm; display:block">{field("byo_draw","text",1,1)}</div>')}
    <div class="grid2" style="margin-top:9pt">
      <div class="panel p-berry tight"><div class="small"><b>Name your creation</b></div>
        <div class="wsp"></div>{field("byo_name","text",78,9)}</div>
      <div class="panel p-blue tight"><div class="small"><b>Its best texture word</b></div>
        <div class="wsp"></div>{field("byo_tex","text",78,9)}</div>
    </div>
    <div class="panel p-soft"><h4 class="small">Build-your-own plan</h4>
      <div class="small">Base: {field("byo_base","text",70)} &nbsp; Fruit: {field("byo_fruit","text",64)}</div><div class="wsp"></div>
      <div class="small">Crunch: {field("byo_crunch","text",64)} &nbsp; Aroma: {field("byo_aroma","text",64)}</div><div class="wsp"></div>
      <div class="small">The one thing I would test first: {field("byo_test","text",100)}</div></div>'''
    content_page(CH[10], inner)

# ================================================================= TESTING JOURNAL (4pp)
def test_log(idx):
    def L(label,name,w=112): return (f'<div class="r" style="display:flex; gap:8pt; margin-bottom:8pt; align-items:flex-end;">'
        f'<span class="small" style="width:92pt; flex:none; font-weight:700; color:{INK_DK}">{label}</span>'
        f'{field(name,"text",w,8.6)}</div>')
    inner = f'''<h2 class="h-md serif">Kitchen Test Sheet #{idx}</h2><hr class="rule">
    <p class="tiny mute">Complete one sheet per recipe and variation. Change one main variable at a time. This is a
      development record — nothing here is validated until review is complete.</p>
    <div class="panel p-soft">
      {L("Recipe &amp; date","tl%d_recipe"%idx)}
      {L("Tester","tl%d_tester"%idx)}
      {L("Brands &amp; weights","tl%d_brands"%idx)}
      {L("Actual yield","tl%d_yield"%idx)}
      {L("Time &amp; temp","tl%d_temp"%idx)}
      {L("Texture hot / cooled","tl%d_texture"%idx)}
      {L("Flavor: what worked","tl%d_flavor"%idx)}
      {L("What I would change","tl%d_change"%idx)}
      {L("Child response","tl%d_child"%idx)}
      {L("Allergens &amp; subs","tl%d_allerg"%idx)}
      {L("Storage decision","tl%d_storage"%idx)}
    </div>
    <div class="panel p-blue tight" style="display:flex; align-items:center; gap:14pt;">
      <span class="small" style="font-weight:700">Decision:</span>
      {checkline("tl%d_ok"%idx,"Approved for next round")}{checkline("tl%d_rev"%idx,"Revise")}{checkline("tl%d_disc"%idx,"Discard")}
    </div>
    <p class="tiny mute">Reminder: &ldquo;Child response&rdquo; records what you observed without pressure — not whether a plate
      was cleared.</p>'''
    content_page("Testing Journal", inner)

def build_journal():
    inner0 = f'''<div class="eyebrow">Section 14 · Test &amp; Celebrate</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Recipe Testing Journal</h1><hr class="rule-blue">
    <p style="max-width:152mm">Every recipe in this book is a <b>draft</b>. This journal is where a family — or a test
      kitchen — turns drafts into dependable recipes. Use it the way professional recipe developers do: one change at a
      time, careful notes, honest decisions.</p>
    <div class="grid2">
      {panel("p-blue","","How to test well",
        '<ul class="clean small" style="margin:0"><li>Weigh and record real brands and amounts.</li>'
        '<li>Change one variable, then taste and note.</li><li>Write what you would change next time.</li>'
        '<li>Decide: approve, revise, or discard.</li></ul>')}
      {panel("p-mango","","What we do not record",
        '<ul class="clean small" style="margin:0"><li>Pressure to eat or finish.</li><li>Guesses dressed up as facts.</li>'
        '<li>Calories or macros — those wait for verified weights and professional review.</li></ul>')}
    </div>
    {mission(0,"Family Taste-Test Scorecard","Everyone scores the <b>experience</b>, kindly. Circle or tick — no one has to eat to take part.",
      f'<div class="small">Dessert tested: {field("sc_dish","text",118)}</div><div class="wsp"></div>'
      f'<div class="small">Looks interesting: {ckrow_group([("sc_l1","A little"),("sc_l2","Some"),("sc_l3","A lot")])}</div>'
      f'<div class="small">Smells inviting: {ckrow_group([("sc_s1","A little"),("sc_s2","Some"),("sc_s3","A lot")])}</div>'
      f'<div class="small">Texture I noticed: {field("sc_tex","text",100)}</div><div class="wsp"></div>'
      f'<div class="small">One kind word about it: {field("sc_word","text",104)}</div>')}'''
    content_page("Testing Journal", inner0, bookmark="14 · Recipe Testing Journal")
    test_log(1)
    test_log(2)

# ================================================================= FINAL CHALLENGE (2pp)
def build_final():
    inner1 = f'''<div class="eyebrow" style="color:{BLUE}">Section 15 · Test &amp; Celebrate</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Dessert Detectives · Final Challenge</h1><hr class="rule-blue">
    <p style="max-width:150mm">You have investigated flavor, texture, safety, and measuring. Time to put it together!
      An adult can read each question. Tick, number, or write your answers. Answers are in the Answer Key.</p>
    {mission(0,"Review · Safe Hands","Before we mix anything, what do we do first?",
      ckrow_group([("fc_h1","Taste with a finger"),("fc_h2","Wash our hands"),("fc_h3","Turn on the oven alone")]))}
    {mission(0,"Review · Who Does What","Write CHILD or ADULT for each task.",
      f'<div class="small">{field("fc_w1","text",30)} Measure oats &nbsp;&nbsp; {field("fc_w2","text",30)} Use the sharp knife</div>'
      f'<div class="wsp"></div><div class="small">{field("fc_w3","text",30)} Mix with a spoon &nbsp;&nbsp; {field("fc_w4","text",30)} Remove a hot pan</div>')}
    {mission(14,"Mission · Detective Master","What makes someone a great Dessert Detective? Tick all that are true.",
      ckrow_group([("fc_m1","They notice flavor and texture"),("fc_m2","They read every label"),
                   ("fc_m3","They force others to finish food"),("fc_m4","They change one thing and take notes"),
                   ("fc_m5","They use kind, curious words")]))}'''
    content_page("Final Challenge", inner1, bookmark="15 · Detectives Final Challenge")

    inner2 = f'''<h2 class="h-md serif">What I learned</h2><hr class="rule">
    <div class="panel p-soft">
      <div class="small">The best dessert I made was {field("wl_best","text",112)}</div><div class="wsp"></div>
      <div class="small">A new word I can use to describe food is {field("wl_word","text",100)}</div><div class="wsp"></div>
      <div class="small">A kitchen skill I got better at is {field("wl_skill","text",104)}</div><div class="wsp"></div>
      <div class="small">Something I would like to invent next is {field("wl_next","text",98)}</div>
    </div>
    {mission(0,"Detective Reflection","Finish the sentence — describe, do not judge.",
      f'<div class="small">Cooking with my family made me feel {field("wl_feel","text",108)}</div>')}
    {panel("p-dark","","",'<h4 style="color:#fff">You did it</h4>'
      '<p style="margin:0" class="small">You learned to cook with curiosity, stay safe, and describe what you notice. '
      'Those are skills you keep for life. Turn the page for your certificate.</p>')}'''
    content_page("Final Challenge", inner2)

# ================================================================= ANSWER KEY + CERTIFICATE (2pp)
def build_answers():
    inner1 = f'''<div class="eyebrow">Section 16 · For the adult</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Answer Key &amp; Support Notes</h1><hr class="rule-blue">
    <div class="grid2">
      {panel("p-soft","","Suggested answers",
        '<ul class="clean small" style="margin:0">'
        '<li><b>M7 Building blocks:</b> Oats → carbohydrate; Yogurt → protein; Seed butter → fat; Banana → carbohydrate.</li>'
        '<li><b>M10 Ingredient match:</b> Mango=E, Oats=C, Yogurt=A, Banana=D, Cinnamon=B.</li>'
        '<li><b>M11 Steps order:</b> 1 Wash hands · 2 Mash bananas · 3 Mix oats, egg, cinnamon · 4 Adult bakes · 5 Cool &amp; taste.</li>'
        '<li><b>M12 Kitchen math:</b> 1) 4 &nbsp; 2) 2 &nbsp; 3) 4 scoops &nbsp; 4) 6 minutes &nbsp; 5) 4 times.</li>'
        '<li><b>M13 Spot the allergen:</b> Yogurt→Milk; Graham→Wheat; Egg→Egg; Seed butter→Seeds; Choc chips→Milk (often Soy).</li>'
        '<li><b>Best way to test:</b> Change one thing and take notes.</li>'
        '<li><b>Frozen pop change:</b> It melts.</li>'
        '<li><b>Why read labels:</b> To check allergens and keep everyone safe.</li></ul>')}
      {panel("p-blue","","Review answers",
        '<ul class="clean small" style="margin:0"><li><b>Safe Hands:</b> Wash our hands.</li>'
        '<li><b>Who does what:</b> Child — measure oats, mix with a spoon. Adult — use the knife, remove a hot pan.</li>'
        '<li><b>Detective Master (M14):</b> Notices flavor/texture · reads labels · changes one thing and takes notes · '
        'uses kind words. <i>Not</i> forcing others to finish food.</li>'
        '<li><b>Wheels, vocabulary, drawings, reflections:</b> open responses — there is no single correct answer. Practicing '
        'the vocabulary is the goal.</li></ul>')}
    </div>
    {panel("p-dark","","",'<h4 style="color:#fff">How to support the child</h4>'
      '<p style="margin:0" class="small">Ask neutral, curious questions: &ldquo;What do you notice? What might change if we '
      'chill it? Would you like to smell it before tasting?&rdquo; Avoid bargaining over bites, praising a clean plate, or '
      'presenting dessert as a reward for eating something else. Let &ldquo;I am done&rdquo; and &ldquo;not yet&rdquo; be '
      'complete answers.</p>')}'''
    content_page("Answer Key", inner1, bookmark="16 · Answer Key & Certificate")

    inner2 = f'''<div class="center">
      <div class="eyebrow" style="color:{MANGO}">Award</div>
      <h1 class="serif" style="font-size:30pt; margin-top:4pt;">Dessert Detective Certificate</h1>
      <div style="height:2.4pt; width:70pt; background:{BLUE}; border-radius:2pt; margin:10pt auto 14pt;"></div>
      <span class="icwrap" style="width:80pt;height:80pt;background:{BLUE_BG}">{svg(IC["badge"],w=54,h=54)}</span>
    </div>
    <div class="panel p-soft" style="margin-top:14pt; text-align:center;">
      <div style="font-size:12pt; margin-bottom:12pt;">This certifies that</div>
      <div style="font-size:16pt;">{field("cert_name","text",120,11)}</div>
      <div class="small mute" style="margin-top:3pt">(name)</div>
      <div style="font-size:11.5pt; margin:14pt 0;">has practiced cooking with curiosity, kitchen safety, and careful noticing.</div>
      <div class="small" style="margin-top:6pt">Today I practiced:
        {checkline("cert_safe","safety")}{checkline("cert_measure","measuring")}{checkline("cert_describe","describing")}{checkline("cert_test","testing one change")}</div>
      <div style="display:flex; justify-content:center; gap:30pt; margin-top:18pt;">
        <div>{field("cert_date","text",50,10)}<div class="small mute">Date</div></div>
        <div>{field("cert_sign","text",70,10)}<div class="small mute">Grown-up signature</div></div>
      </div>
    </div>
    {panel("p-dark","","",'<div class="center"><b style="letter-spacing:.1em; color:#fff">MISSION COMPLETE</b>'
      '<p style="margin:6pt 0 0" class="small">I learned to cook with curiosity, stay safe, and describe what I notice.</p></div>')}'''
    content_page("Certificate", inner2)

# ================================================================= SOURCES / EDITORIAL (2pp)
def build_sources():
    inner1 = f'''<div class="eyebrow">Section 17</div>
    <h1 class="h-xl serif" style="margin-top:5pt">Editorial Status, Safety Notes &amp; Sources</h1><hr class="rule-blue">
    <div class="grid2">
      {panel("p-soft","","Editorial status",
        '<p class="small" style="margin:0">A new, independent companion book — <b>not</b> part of the five canonical Body '
        'Recomp Bible volumes. This edition is a development prototype for choosing direction, testing recipes, and '
        'commissioning professional review. It is not final, tested, approved, or publication-ready.</p>')}
      {panel("p-blue","","Before publication, every recipe needs",
        '<ul class="clean small" style="margin:0"><li>Kitchen &amp; sensory testing</li><li>Standardized ingredient weights</li>'
        '<li>Verified yield &amp; storage validation</li><li>Allergen &amp; food-safety review</li>'
        '<li>Pediatric or qualified nutrition review</li><li>Cristy Sim’s final approval</li></ul>')}
    </div>
    <h3 class="h-md serif" style="margin-top:6pt">Sources to consult during review</h3><hr class="rule">
    <p class="tiny mute">The four deep links below were carried forward from the development brief for verification. Broader
      references are listed by organization and document; a reviewer should confirm the current page and wording before any
      claim is published. No study, statistic, or recommendation in this draft should be treated as verified yet.</p>
    <div class="p-soft panel small">
      <div style="margin-bottom:6pt"><b>CDC — Choking Hazards (infant &amp; toddler nutrition):</b><br>
        <a href="https://www.cdc.gov/infant-toddler-nutrition/foods-and-drinks/choking-hazards.html">https://www.cdc.gov/infant-toddler-nutrition/foods-and-drinks/choking-hazards.html</a></div>
      <div style="margin-bottom:6pt"><b>CDC — Foods and Drinks to Limit:</b><br>
        <a href="https://www.cdc.gov/infant-toddler-nutrition/foods-and-drinks/foods-and-drinks-to-limit.html">https://www.cdc.gov/infant-toddler-nutrition/foods-and-drinks/foods-and-drinks-to-limit.html</a></div>
      <div style="margin-bottom:6pt"><b>FDA — Food Allergies:</b><br>
        <a href="https://www.fda.gov/food/food-labeling-nutrition/food-allergies">https://www.fda.gov/food/food-labeling-nutrition/food-allergies</a></div>
      <div><b>FoodSafety.gov — Cold Food Storage Charts:</b><br>
        <a href="https://www.foodsafety.gov/food-safety-charts/cold-food-storage-charts">https://www.foodsafety.gov/food-safety-charts/cold-food-storage-charts</a></div>
    </div>
    <div class="p-soft panel small">
      <b>Additional bodies to reference (confirm current pages during review):</b>
      <ul class="clean" style="margin:5pt 0 0"><li>American Academy of Pediatrics / HealthyChildren.org — feeding, choking, and mealtime guidance.</li>
      <li>USDA MyPlate — food groups and family nutrition basics.</li>
      <li>Dietary Guidelines for Americans (USDA &amp; HHS) — general dietary patterns.</li>
      <li>USDA / FoodSafety.gov — safe egg cooking and handling of perishables.</li></ul></div>'''
    content_page("Sources", inner1, bookmark="17 · Editorial Status & Sources")

    inner2 = f'''<h2 class="h-md serif">How claims were handled</h2><hr class="rule">
    <div class="grid2">
      {panel("p-mango","","What this book states",
        '<p class="small" style="margin:0">Only calm, observable, non-medical ideas: food gives energy and building blocks; '
        'frozen things melt when warm; wash hands before cooking; cook eggs fully; cut round or hard foods small. These are '
        'framed as general knowledge for a reviewer to confirm.</p>')}
      {panel("p-berry","","What this book avoids",
        '<p class="small" style="margin:0">No calories, macros, verified yields, or shelf-life. No claims that a food boosts '
        'immunity, burns fat, detoxifies, prevents disease, or changes behavior. No labeling foods good, bad, clean, or '
        'guilt-free. No hiding vegetables and no dessert-as-payment.</p>')}
    </div>
    {panel("p-dark","","",'<h4 style="color:#fff">Next gate</h4>'
      '<p style="margin:0" class="small">Sensory testing of all recipes, standardized weights, verified yield, allergen '
      'controls, storage/shelf-life validation, pediatric or qualified nutrition review, and Cristy Sim’s final approval. '
      'Until those are complete, this remains a development edition.</p>')}
    {panel("p-blue", IC["shield"], "Safety, in one paragraph",
      '<p class="small" style="margin:0">Adults supervise young cooks and handle heat, knives, blenders, and allergens. '
      'Wash hands; cook eggs fully; keep perishables cold; serve foods at a safe temperature and size. Whole grapes, whole '
      'nuts, dense nut/seed butter, and hard pieces can be choking hazards — modify for the child. For any diagnosed allergy '
      'or swallowing concern, follow your healthcare professional’s guidance. This book is for children about 5 and older; '
      'younger children and those with medical needs require individualized professional guidance.</p>')}
    <div class="center mute tiny" style="margin-top:10pt">The Family Dessert Kitchen · A Playful Guide to Cooking, Tasting &amp; Learning Together ·
      By Cristy Sim · Development Edition · All illustrations original.</div>'''
    content_page("Sources", inner2)

# ===================================================================== MAIN
def main():
    build_cover(); build_title(); build_toc(TOC_ENTRIES)
    build_welcome(); build_howto(); build_safety(); build_detectives_intro()
    for chap in (5,6,7,8,9,10):
        chapter_divider(chap)
        for r in [x for x in RECIPES if x["chap"]==chap]:
            recipe_page(r)
        if chap==10:
            build_byo_close()
    build_flavorlab(); build_nutrition(); build_games()
    build_journal(); build_final(); build_answers(); build_sources()

    html = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<title>The Family Dessert Kitchen</title><style>%s</style></head><body>%s</body></html>"
            ) % (CSS, "\n".join(PAGES))
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here,"family_dessert_kitchen.html"),"w",encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(here,"fields.json"),"w",encoding="utf-8") as f:
        json.dump({"fields":FIELDS,"bookmarks":BOOKMARKS,"pages":len(PAGES)}, f, indent=1)
    print("pages:", len(PAGES), "| fields:", len(FIELDS), "| bookmarks:", len(BOOKMARKS))

if __name__ == "__main__":
    main()






