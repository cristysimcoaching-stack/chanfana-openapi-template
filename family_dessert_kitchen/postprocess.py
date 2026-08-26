# -*- coding: utf-8 -*-
"""Add genuine AcroForm fields, PDF bookmarks, and stamped page numbers/footer."""
import json, pymupdf

BLUE=(0.106,0.435,0.937); INK=(0.137,0.152,0.176); MUTE=(0.42,0.45,0.50)
doc=pymupdf.open("raw.pdf")
man=json.load(open("fields.json"))
fields=man["fields"]; bmarks=man["bookmarks"]

# ---- 1. locate every token and add a widget -------------------------------
seen=set(); placed=0; missing=[]
# pre-index text rects per page once for speed
for f in fields:
    tok=f["token"]; kind=f["kind"]; w=f["w"]; h=f["h"]; name=f["name"]
    fname = name if name not in seen else f"{name}_{tok}"
    seen.add(name)
    found=None
    for pno in range(doc.page_count):
        rects=doc[pno].search_for(tok)
        if rects:
            found=(pno,rects[0]); break
    if not found:
        missing.append(tok); continue
    pno,r=found
    page=doc[pno]
    x0=r.x0; y0=r.y0
    rect=pymupdf.Rect(x0, y0, x0+w, y0+h)
    wd=pymupdf.Widget()
    wd.rect=rect
    wd.field_name=fname
    wd.border_color=None
    wd.fill_color=None
    wd.text_color=INK
    if kind=="check":
        wd.field_type=pymupdf.PDF_WIDGET_TYPE_CHECKBOX
        wd.field_value=False
        wd.border_color=BLUE
        wd.border_width=0.0   # visible box already drawn in HTML
    else:
        wd.field_type=pymupdf.PDF_WIDGET_TYPE_TEXT
        wd.text_fontsize=10.5
        wd.field_value=""
    page.add_widget(wd)
    placed+=1

print("widgets placed:", placed, "| missing:", len(missing))

# ---- 2. page numbers + footer (skip cover page 0) -------------------------
W=doc[0].rect.width
for pno in range(doc.page_count):
    page=doc[pno]
    if pno==0:      # cover: no footer
        continue
    y=doc[pno].rect.height-20
    # hairline
    page.draw_line((48,y-8),(W-48,y-8), color=(0.894,0.905,0.925), width=0.6)
    page.insert_text((48,y), "The Family Dessert Kitchen", fontname="helv", fontsize=7.2, color=MUTE)
    num=str(pno+1)
    tw=pymupdf.get_text_length(num, fontname="hebo", fontsize=8.5)
    page.insert_text((W/2 - tw/2, y), num, fontname="hebo", fontsize=8.5, color=BLUE)
    foot="Development Edition"
    tw2=pymupdf.get_text_length(foot, fontname="helv", fontsize=7.2)
    page.insert_text((W-48-tw2, y), foot, fontname="helv", fontsize=7.2, color=MUTE)

# ---- 3. bookmarks / outline ----------------------------------------------
toc=[[lvl, title, pg] for (lvl,title,pg) in bmarks]
doc.set_toc(toc)

# ---- 4. metadata ----------------------------------------------------------
doc.set_metadata({
 "title":"The Family Dessert Kitchen",
 "author":"Cristy Sim",
 "subject":"A Playful Guide to Cooking, Tasting & Learning Together (Development Edition)",
 "keywords":"family desserts, children, cooking, kitchen safety, development edition",
})

doc.save("The_Family_Dessert_Kitchen.pdf", deflate=True, garbage=3)
print("saved The_Family_Dessert_Kitchen.pdf | pages:", doc.page_count, "| bookmarks:", len(toc))
