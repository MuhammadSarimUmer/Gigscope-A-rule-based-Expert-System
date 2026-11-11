"""
Generate tree PNG/SVG files into assets/ for PDF and static app display.
"""

from __future__ import annotations

from pathlib import Path

try:
    import graphviz
except ImportError:
    graphviz = None

from dss import analyze_answers
from knowledge_meta import ROOT_CAUSES, RULE_CATEGORIES
from scenarios import SCENARIOS
from tree import build_case_tree, build_full_kb_tree, build_root_cause_subtree

ASSETS = Path(__file__).resolve().parent / "assets"


def _render(dot: str, name: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / f"{name}.dot").write_text(dot, encoding="utf-8")
    if graphviz is None:
        return
    try:
        src = graphviz.Source(dot)
        src.format = "png"
        src.render(filename=name, directory=str(ASSETS), cleanup=True)
        src.format = "svg"
        src.render(filename=name, directory=str(ASSETS), cleanup=True)
    except Exception as exc:  # pragma: no cover - missing system graphviz binary
        print(f"Skip PNG/SVG for {name}: {exc}")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    _render(build_full_kb_tree(), "kb_full")
    for cat in RULE_CATEGORIES:
        safe = cat.replace(" ", "_")
        _render(build_full_kb_tree(cat), f"kb_{safe}")
    for rc_id in ROOT_CAUSES:
        _render(build_root_cause_subtree(rc_id), f"cause_{rc_id}")
    demo = analyze_answers(SCENARIOS["1_new_fiverr_broad_high_price"]["answers"])
    top = demo["decision"]["top_action"]
    highlight = top["fix_id"] if top else None
    _render(
        build_case_tree(demo["engine"]["fired_rules"], demo["engine"]["memory"], highlight),
        "case_tree_demo",
    )
    print(f"Exported assets to {ASSETS}")


if __name__ == "__main__":
    main()
