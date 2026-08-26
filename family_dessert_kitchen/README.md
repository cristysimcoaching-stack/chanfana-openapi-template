# The Family Dessert Kitchen — Development Edition
*A Playful Guide to Cooking, Tasting & Learning Together* · by Cristy Sim

An independent companion to the Body Recomp Bible editorial world (not one of the five canonical volumes).
A 70-page, A4, publication-quality **development draft**: 32 original family desserts, kitchen-safety
missions, a Flavor Lab, a Nutrition Explorer, kitchen games, a testing journal, and a printable certificate —
for children ~5–12 and their adult caregivers.

> **Status:** development draft. No recipe is tested; no calories/macros/verified-yields/shelf-life are
> published. Not final, tested, approved, or publication-ready. See the registers.

## Deliverables
| File | What it is |
|---|---|
| `The_Family_Dessert_Kitchen.pdf` | Publication-quality PDF (A4, 70 pp, 278 fillable AcroForm fields, 20 bookmarks) |
| `family_dessert_kitchen.html` | Editable source document (self-contained; all art inline SVG) |
| `build.py`, `recipes.py`, `art.py`, `pages.py`, `postprocess.py` | Generator that produces the HTML and finishes the PDF (`art.py` = original SVG hero illustrations) |
| `fields.json` | Manifest of interactive fields + bookmarks |
| `RECIPE_TESTING_REGISTER.md` | Every recipe and its validation status |
| `CLAIMS_AND_SAFETY_REGISTER.md` | Every factual claim, its source, and review status |
| `QA_REPORT.md` | Page count, field count, inspection, unresolved items, blockers |
| `IMAGE_BRIEF.md` | Optional photography direction (book already ships with original illustrations) |

## Rebuild
```bash
python3 pages.py                                   # -> family_dessert_kitchen.html + fields.json
CHROME=$(ls /opt/pw-browsers/chromium-*/chrome-linux/chrome | head -1)
"$CHROME" --headless --no-sandbox --no-pdf-header-footer \
  --print-to-pdf=raw.pdf "file://$PWD/family_dessert_kitchen.html"
python3 postprocess.py                             # -> The_Family_Dessert_Kitchen.pdf
```
Requires: Python 3 with `pymupdf` (and `pillow` for QA rasterization), plus a Chromium build.

## Design system
White interiors · charcoal type · one blue accent (#1B6FEF) · hairline rules · soft blue info panels ·
dark charcoal callouts · playful secondaries (mango #F5B301, strawberry #EF5A8C, soft orange #F58634) ·
original flat SVG spot art and mission badges.
