# QA Report — The Family Dessert Kitchen (Development Edition)
Cristy Sim · Generated 2026-08-26

## 1. Deliverable summary
| Item | Value |
|---|---|
| Publication PDF | `The_Family_Dessert_Kitchen.pdf` (A4 portrait, ~1.65 MB) |
| Editable source | `family_dessert_kitchen.html` (self-contained; all art inline SVG) + generator scripts `build.py`, `recipes.py`, `art.py`, `pages.py`, `postprocess.py` |
| Original illustrations | 8 palette-driven flat SVG "hero" templates (`art.py`) — a themed hero on every recipe page, a large scene on every chapter divider, and two illustration cards on the cover |
| Page count | **70 pages** (target 60–85 ✓) |
| Recipes | **32 original development recipes** (target 30–36 ✓) across 6 chapters |
| Interactive fillable fields | **278 genuine AcroForm widgets** — 130 text fields + 148 checkboxes |
| PDF bookmarks (navigation) | **20** (all major sections + 6 chapters) |
| Registers | `RECIPE_TESTING_REGISTER.md`, `CLAIMS_AND_SAFETY_REGISTER.md` |
| Image brief | `IMAGE_BRIEF.md` (optional photography direction; book ships with original illustrations) |

## 2. Build pipeline (reproducible)
1. `python3 pages.py` → writes `family_dessert_kitchen.html` + `fields.json` (field & bookmark manifest).
2. Headless Chromium `--print-to-pdf` → `raw.pdf` (A4, 595×842 pt confirmed).
3. `python3 postprocess.py` → adds AcroForm widgets (anchored to invisible search tokens over visible lines/boxes), page numbers + footer, bookmarks, metadata → `The_Family_Dessert_Kitchen.pdf`.

## 3. Visual inspection
All 70 pages were rasterized (contact sheets + high-DPI spot checks) and reviewed. Field alignment was
verified with a debug pass (widget rectangles overlaid on visible boxes/lines).

| Check | Result |
|---|---|
| Text clipping | None found |
| Overlapping objects | None found |
| Broken/missing glyphs (incl. em-dash, curly quotes, °) | None found |
| Orphan headings | None found |
| Nearly-empty accidental pages | None (recipe pages carry generous but intentional white space) |
| Distorted images | N/A — all art is original vector SVG (no photos) |
| Illustration ↔ text overlap | Checked across all 32 recipes; hero placement measured against the tallest (7-ingredient) recipes — ≥3 mm clearance from the response strip and the footer on the worst case |
| Illegible small print | None; smallest body ≈ 7.6–7.8 pt for captions only |
| Consistent recipe-page geometry | ✓ identical template across all 32 |
| Consistent color/typography | ✓ single token system |
| Internal navigation (bookmarks) | ✓ 20 working outline entries |
| Interactive fields | ✓ 278/278 placed (0 missing); text + checkbox widgets align to visible print guides |
| Page numbering | ✓ centered, blue, pages 2–70; cover unnumbered by design |
| Contrast / accessibility | Charcoal on white and dark-callout text meet strong contrast; blue accent used for emphasis, not sole signal |

## 4. Requirements conformance
- **Development labeling:** every recipe carries the `DEVELOPMENT RECIPE — REQUIRES KITCHEN TESTING` stamp; no macros/calories/verified-yield/shelf-life anywhere. ✓
- **Measurements:** US + estimated metric on every ingredient; metric flagged approximate. ✓
- **Required recipe fields:** number, chapter, title, status, estimated yield, prep/cook time, ingredients (US+metric), numbered steps, "The Child Can," "The Adult Handles," flavor & texture note, allergens to check, age & texture note, one learning activity, one substitution, "Test Still Needed." ✓ (verified across all 32)
- **Nutrition neutrality:** no good/bad/clean/guilt-free language; no medical claims; no hidden-veg or dessert-as-reward framing; guardrails enumerated in the Claims Register. ✓
- **Safety coverage:** supervision, handwashing, burns, knives/blenders, cross-contact/allergens, choking & texture, egg doneness, perishables, and "follow professional guidance for diagnosed needs." ✓
- **Sources:** only the four author-provided deep links used verbatim; other bodies cited at organization level and flagged for verification; no fabricated citations/URLs. ✓
- **Imagery:** 100% original inline SVG illustrations & icons; no copied photographs, no watermarks/branding/real people. ✓
- **Interactivity:** genuine fillable fields **and** visible print-usable lines/boxes on every writable area. ✓

## 5. Known limitations / unresolved items (non-blocking for a *development* draft)
1. **Metric weights are approximations**, not standardized weighed values (by design this edition).
2. **Invisible anchor tokens** (3 pt white text) remain in the PDF text layer behind fields; visually invisible and harmless, but present to text extraction. Can be redacted in a future pass if desired.
3. **Alt text:** PDF form fields carry field names; full per-image alt-text/tagged-PDF (PDF/UA) structure is not yet applied. Recommended before any accessibility certification.
4. **Recipe pages have intentional lower white space**; acceptable editorially, but a future revision could add an optional photo well or tip strip to fill it.
5. Grayscale print was designed for (contrast-first palette) but not proofed on a physical grayscale device.

## 6. Publication blockers (must clear before "final/approved")
These are **content-validation** gates, not layout defects. Until all clear, the book must stay labeled a
Development Edition and must not be called final, tested, approved, or publication-ready:
- [ ] Kitchen testing of all 32 recipes (see Recipe Testing Register)
- [ ] Sensory testing
- [ ] Standardized ingredient weights
- [ ] Verified yields
- [ ] Allergen review (per recipe **and** per substitution)
- [ ] Food-safety review
- [ ] Storage / shelf-life validation
- [ ] Pediatric or qualified nutrition review
- [ ] Source verification of every claim in the Claims & Safety Register
- [ ] Cristy Sim's final editorial approval

## 7. Verdict
A **finished, visually polished development draft** meeting the layout, structure, interactivity, and
editorial-guardrail requirements. It is **not** described as final/tested/approved — those gates remain open
by design and are tracked in the two registers.
