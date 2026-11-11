# PDF submission guide (paste-ready outline)

## 1. Problem and niche

Freelancers on Fiverr/Upwork often cannot explain low order volume. GigScope encodes coaching knowledge as rules to diagnose root causes and prioritize fixes.

## 2. Knowledge acquisition

Sources: marketplace best practices, seller experience, assignment requirements. Encoded as 233 IF-THEN rules with plain-English `reason` fields for viva.

## 3. Fact table

Paste from `facts.py`: 66 questions across account, niche, pricing, SEO, visuals, portfolio, communication, reviews, proposals, activity, mindset.

## 4. Finding / root cause / fix tables

Export from `knowledge_meta.py`: FINDINGS, ROOT_CAUSES, FIXES (with impact/effort/cost/days).

## 5. Rule table sample

Run in Python: `import pandas as pd; from rules import RULES; pd.DataFrame(RULES).to_csv("rules.csv")` — include first/last pages + count.

## 6. Architecture

```
User → Streamlit → facts → engine → memory → DSS → UI
rules.py (KB) ------------^
```

## 7. Forward chaining

Bullet list from README/engine docstring: working memory, fire conditions, CF multiply, combine, stop condition.

## 8. Certainty worked example

Rules 0.6 and 0.5 on same cause → 0.8. Include one fired rule from scenario 8 in appendix.

## 9. DSS formula

`score = w_impact×impact + w_effort×(10−effort) + w_cost×(10−cost) + w_conf×confidence×10`

## 10. Code walkthrough

One paragraph per file: `app.py`, `engine.py`, `rules.py`, `dss.py`, `tree.py`, `validate_kb.py`.

## 11. Sample runs

Screenshot instructions: Load scenarios 1, 4, 12 — Results tab, tree tab, DSS sliders.

## 12. Tree diagrams

Insert PNGs from `assets/` (or DOT + legend) — per-case from app, `kb_full`, one `cause_*` subtree.

## 13. Limitations and future work

From About tab in `app.py`.

## 14. Live link

Add Streamlit Cloud URL after deploy.
