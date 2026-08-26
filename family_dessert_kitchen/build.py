# -*- coding: utf-8 -*-
"""
THE FAMILY DESSERT KITCHEN — book generator.
Emits a self-contained A4 HTML file (editable source) plus a fields manifest
(fields.json) describing genuine fillable AcroForm widgets to be layered on
during post-processing. No external assets; all art is inline SVG.
"""
import json, os

MM = 72.0 / 25.4  # mm -> pt

# ---------------------------------------------------------------- design tokens
INK      = "#23272E"   # body charcoal
INK_DK   = "#12151A"   # headings
MUTE     = "#6B7280"   # secondary text
RULE     = "#E4E7EC"   # hairline
BLUE     = "#1B6FEF"   # primary accent
BLUE_BG  = "#EAF2FE"   # soft blue panel
BLUE_BD  = "#CFE0FC"
BLUE_LT  = "#6BA8FF"
DARK_BG  = "#14171C"   # charcoal callout
DARK_TX  = "#EEF2F6"
MANGO    = "#F5B301"; MANGO_BG = "#FEF5D8"
BERRY    = "#EF5A8C"; BERRY_BG = "#FDE7EF"
ORANGE   = "#F58634"; ORANGE_BG= "#FCEBDC"
LEAF     = "#2F9E6B"; LEAF_BG  = "#E4F5EC"

PAGES = []       # list of html strings, one per printed page
BOOKMARKS = []   # (level, title, page_number_1based)
FIELDS = []      # {token,kind,w,h,name,options?}
_fld_n = [0]

def add_page(html, bookmark=None, level=1):
    PAGES.append(html)
    if bookmark:
        BOOKMARKS.append((level, bookmark, len(PAGES)))

def field(name, kind="text", w_mm=60, h_mm=7.0, box=False):
    """Return HTML for a writable area with an invisible search anchor.
    kind: 'text' (underline) or 'check' (square). A widget is added later at
    the anchor, sized w x h pt. Visible line/box guarantees print usability."""
    _fld_n[0] += 1
    tok = "zZ%04dZz" % _fld_n[0]
    w_pt = round(w_mm * MM, 2); h_pt = round(h_mm * MM, 2)
    FIELDS.append({"token": tok, "kind": kind, "w": w_pt, "h": h_pt, "name": name})
    if kind == "check":
        cls = "chkbox"
    else:
        cls = "wline" if not box else "wbox"
    return ('<span class="fldwrap %s" style="width:%.2fmm;height:%.2fmm">'
            '<span class="anchor">%s</span></span>') % (cls, w_mm, h_mm, tok)

def checkline(name, label, w_mm=None):
    return '<span class="ckrow">%s<span class="cklab">%s</span></span>' % (
        field(name, "check", 4.4, 4.4), label)

def writelines(prefix, n, w_mm=170, h_mm=8.4):
    return "".join(field("%s_%d" % (prefix, i+1), "text", w_mm, h_mm)
                   + '<div class="wsp"></div>' for i in range(n))

# ------------------------------------------------------------------------ icons
def svg(body, vb="0 0 48 48", w=48, h=48, cls=""):
    return ('<svg class="ic %s" width="%d" height="%d" viewBox="%s" '
            'xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true">%s</svg>'
            ) % (cls, w, h, vb, body)

IC = {}
IC["pop"] = svg('<rect x="16" y="6" width="16" height="24" rx="8" fill="%s"/>'
    '<rect x="18" y="10" width="6" height="10" rx="3" fill="#fff" opacity=".45"/>'
    '<rect x="22" y="29" width="4" height="13" rx="2" fill="#C9A06A"/>' % MANGO)
IC["cup"] = svg('<path d="M12 16h24l-2 22a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4z" fill="%s"/>'
    '<rect x="12" y="12" width="24" height="6" rx="3" fill="%s"/>'
    '<circle cx="20" cy="26" r="2.4" fill="#fff" opacity=".7"/>'
    '<circle cx="28" cy="32" r="2" fill="#fff" opacity=".55"/>' % (BLUE_BG, BERRY))
IC["muffin"] = svg('<path d="M13 22h22l-3 18a3 3 0 0 1-3 3H19a3 3 0 0 1-3-3z" fill="#C9895A"/>'
    '<path d="M11 22c1-8 8-12 13-12s12 4 13 12z" fill="%s"/>'
    '<circle cx="20" cy="17" r="1.7" fill="#7A4B2B"/><circle cx="27" cy="15" r="1.7" fill="#7A4B2B"/>'
    '<circle cx="24" cy="20" r="1.7" fill="#7A4B2B"/>' % MANGO)
IC["cookie"] = svg('<circle cx="24" cy="24" r="17" fill="#D9A15E"/>'
    '<circle cx="18" cy="20" r="2.3" fill="#5A3A20"/><circle cx="30" cy="19" r="2.3" fill="#5A3A20"/>'
    '<circle cx="26" cy="29" r="2.3" fill="#5A3A20"/><circle cx="17" cy="29" r="1.8" fill="#5A3A20"/>')
IC["apple"] = svg('<path d="M24 14c3-4 9-4 11 0 3 5 1 16-5 22-2 2-4 2-6 0-6-6-8-17-5-22 2-3 5-3 5 0z" fill="%s"/>'
    '<path d="M24 14c-1-3 1-6 4-7" stroke="#7A4B2B" stroke-width="2" fill="none" stroke-linecap="round"/>'
    '<path d="M24 8c2-2 5-2 6 0-1 2-4 2-6 0z" fill="%s"/>' % (BERRY, LEAF))
IC["bowl"] = svg('<path d="M8 24h32a16 16 0 0 1-32 0z" fill="%s"/>'
    '<ellipse cx="24" cy="24" rx="16" ry="4" fill="%s"/>'
    '<circle cx="19" cy="21" r="2.3" fill="%s"/><circle cx="27" cy="22" r="2.3" fill="%s"/>'
    '<circle cx="24" cy="19" r="2.3" fill="%s"/>' % (BLUE, BLUE_BG, BERRY, MANGO, ORANGE))
IC["berry"] = svg('<circle cx="18" cy="26" r="8" fill="%s"/><circle cx="29" cy="28" r="7" fill="%s"/>'
    '<path d="M18 18c0-4 3-6 6-6M29 21c0-3 2-5 5-5" stroke="%s" stroke-width="2" fill="none" stroke-linecap="round"/>' % (BLUE, BERRY, LEAF))
IC["whisk"] = svg('<rect x="22" y="6" width="4" height="16" rx="2" fill="#9AA3AE"/>'
    '<path d="M24 20c-6 3-8 10-6 18M24 20c6 3 8 10 6 18M24 20v18" stroke="#9AA3AE" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
IC["badge"] = svg('<path d="M24 4l5 3 6-1 1 6 4 4-3 5 1 6-6 1-4 5-5-3-5 3-4-5-6-1 1-6-3-5 4-4 1-6 6 1z" fill="%s"/>'
    '<circle cx="24" cy="22" r="9" fill="#fff"/><path d="M20 22l3 3 6-6" stroke="%s" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % (BLUE, BLUE))
IC["magnify"] = svg('<circle cx="21" cy="21" r="11" fill="none" stroke="%s" stroke-width="3.4"/>'
    '<line x1="29" y1="29" x2="40" y2="40" stroke="%s" stroke-width="3.6" stroke-linecap="round"/>'
    '<circle cx="21" cy="21" r="5" fill="%s" opacity=".3"/>' % (INK_DK, INK_DK, MANGO))
IC["snow"] = svg('<g stroke="%s" stroke-width="2.6" stroke-linecap="round"><line x1="24" y1="8" x2="24" y2="40"/>'
    '<line x1="10" y1="16" x2="38" y2="32"/><line x1="38" y1="16" x2="10" y2="32"/></g>'
    '<circle cx="24" cy="24" r="3" fill="%s"/>' % (BLUE, BLUE))
IC["heart"] = svg('<path d="M24 40C10 30 6 22 6 16c0-5 4-8 8-8 4 0 7 2 10 6 3-4 6-6 10-6 4 0 8 3 8 8 0 6-4 14-18 24z" fill="%s"/>' % BERRY)
IC["flame"] = svg('<path d="M24 6c2 8 12 10 12 20a12 12 0 0 1-24 0c0-5 3-8 5-12 2 3 4 3 4 0 0-4-1-6 3-8z" fill="%s"/>'
    '<path d="M24 40a5 5 0 0 1-5-5c0-3 3-4 5-8 2 4 5 5 5 8a5 5 0 0 1-5 5z" fill="%s"/>' % (ORANGE, MANGO))
IC["shield"] = svg('<path d="M24 5l16 5v11c0 11-7 19-16 22-9-3-16-11-16-22V10z" fill="%s"/>'
    '<path d="M18 24l4 4 9-9" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % BLUE)
IC["hands"] = svg('<path d="M14 26c0-6 4-10 10-10s10 4 10 10v10H14z" fill="%s"/>'
    '<path d="M18 24v-8a2 2 0 0 1 4 0M22 24v-10a2 2 0 0 1 4 0v10M26 24v-8a2 2 0 0 1 4 0v8" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>'
    '<path d="M10 34c4 4 24 4 28 0" stroke="%s" stroke-width="2.4" fill="none" stroke-linecap="round"/>' % (BLUE, BLUE_LT))
IC["star"] = svg('<path d="M24 6l5 11 12 1-9 8 3 12-11-6-11 6 3-12-9-8 12-1z" fill="%s"/>' % MANGO)
IC["pencil"] = svg('<path d="M10 34l20-20 6 6-20 20-8 2z" fill="%s"/><path d="M30 14l4-4 6 6-4 4z" fill="%s"/>' % (MANGO, BLUE))

def chip(text, bg, fg=INK_DK):
    return '<span class="chip" style="background:%s;color:%s">%s</span>' % (bg, fg, text)

DEV_STAMP = '<span class="devstamp">DEVELOPMENT RECIPE — REQUIRES KITCHEN TESTING</span>'
