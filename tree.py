"""
Build Graphviz DOT strings for reasoning trees.
"""

from __future__ import annotations

from typing import Any

from knowledge_meta import FINDINGS, FIXES, ROOT_CAUSES, VERDICTS
from rules import RULES

LAYER_COLORS = {
    "fact": "#A8D5E2",
    "finding": "#F9E79F",
    "cause": "#F5B7B1",
    "fix": "#ABEBC6",
    "verdict": "#D7BDE2",
}


def _node_type(node_id: str) -> str:
    if node_id in FINDINGS:
        return "finding"
    if node_id in ROOT_CAUSES:
        return "cause"
    if node_id in FIXES:
        return "fix"
    if node_id in VERDICTS:
        return "verdict"
    return "fact"


def _label(node_id: str, memory: dict[str, float] | None) -> str:
    cf = ""
    if memory and node_id in memory:
        cf = f"\\n{memory[node_id]*100:.0f}%"
    for registry in (FINDINGS, ROOT_CAUSES, FIXES, VERDICTS):
        if node_id in registry:
            name = registry[node_id]["name"]
            short = name if len(name) < 28 else name[:25] + "..."
            return f"{short}{cf}"
    short_id = node_id.replace("_", " ")
    if len(short_id) > 22:
        short_id = short_id[:19] + "..."
    return f"{short_id}{cf}"


def build_case_tree(
    fired_rules: list[dict],
    memory: dict[str, float],
    highlight_fix: str | None = None,
) -> str:
    """Per-case reasoning tree from fired rules only."""
    nodes: set[str] = set()
    edges: list[tuple[str, str, str]] = []

    for fr in fired_rules:
        rule = fr["rule"]
        concl = rule["then"]
        nodes.add(concl)
        for c in rule["if"]:
            if isinstance(c, dict) and "not" in c:
                prem = c["not"]
            else:
                prem = c
            nodes.add(prem)
            edges.append((prem, concl, rule["id"]))

    lines = [
        "digraph CaseTree {",
        'rankdir=TB;',
        'bgcolor="white";',
        'node [shape=box, style="filled,rounded", fontname="Arial", fontsize=11];',
        'edge [fontname="Arial", fontsize=9];',
        'label="Per-case reasoning tree"; labelloc=t; fontsize=14;',
    ]

    by_layer: dict[str, list[str]] = {"fact": [], "finding": [], "cause": [], "fix": [], "verdict": []}
    for n in sorted(nodes):
        lt = _node_type(n)
        by_layer.setdefault(lt, []).append(n)

    for lt, nlist in by_layer.items():
        if not nlist:
            continue
        lines.append(f"{{ rank=same; {'; '.join(f'n_{n}' for n in nlist)}; }}")
        for n in nlist:
            color = LAYER_COLORS.get(lt, "#EEEEEE")
            pen = "3" if highlight_fix and n == highlight_fix else "1"
            lines.append(f'n_{n} [label="{_label(n, memory)}", fillcolor="{color}", penwidth={pen}];')

    for a, b, rid in edges:
        lines.append(f'n_{a} -> n_{b} [label="{rid}"];')

    lines.append("}")
    return "\n".join(lines)


def build_full_kb_tree(category: str | None = None) -> str:
    """Full knowledge-base tree (all rules), optionally filtered by category."""
    filtered = [r for r in RULES if category is None or r["category"] == category]
    lines = [
        "digraph KBTree {",
        'rankdir=TB;',
        'bgcolor="white";',
        'node [shape=box, style="filled,rounded", fontname="Arial", fontsize=10];',
        'edge [fontname="Arial", fontsize=8];',
        f'label="Knowledge base{" - " + category if category else ""}"; labelloc=t;',
    ]
    nodes: set[str] = set()
    for r in filtered:
        nodes.add(r["then"])
        for c in r["if"]:
            if isinstance(c, dict) and "not" in c:
                nodes.add(c["not"])
            else:
                nodes.add(c)
    by_layer: dict[str, list[str]] = {}
    for n in nodes:
        lt = _node_type(n)
        by_layer.setdefault(lt, []).append(n)
    for lt, nlist in by_layer.items():
        if not nlist:
            continue
        lines.append(f"{{ rank=same; {'; '.join(f'k_{n}' for n in nlist)}; }}")
        for n in nlist:
            color = LAYER_COLORS.get(lt, "#EEEEEE")
            lines.append(f'k_{n} [label="{_label(n, None)}", fillcolor="{color}"];')
    for r in filtered:
        for c in r["if"]:
            prem = c["not"] if isinstance(c, dict) else c
            lines.append(f'k_{prem} -> k_{r["then"]} [label="{r["id"]}"];')
    lines.append("}")
    return "\n".join(lines)


def build_root_cause_subtree(root_cause_id: str) -> str:
    """Subtree for one root cause: upstream rules and downstream fixes."""
    lines = [
        "digraph SubTree {",
        'rankdir=TB;',
        'node [shape=box, style="filled,rounded", fontname="Arial", fontsize=10];',
        f'label="{ROOT_CAUSES[root_cause_id]["name"]}"; labelloc=t;',
    ]
    upstream = [r for r in RULES if r["then"] == root_cause_id]
    downstream = [r for r in RULES if root_cause_id in r["if"]]
    nodes: set[str] = {root_cause_id}
    edges: list[tuple[str, str, str]] = []
    for r in upstream:
        for c in r["if"]:
            prem = c["not"] if isinstance(c, dict) else c
            nodes.add(prem)
            edges.append((prem, root_cause_id, r["id"]))
    for r in downstream:
        nodes.add(r["then"])
        edges.append((root_cause_id, r["then"], r["id"]))
    for n in nodes:
        lt = _node_type(n)
        color = LAYER_COLORS.get(lt, "#EEEEEE")
        lines.append(f's_{n} [label="{_label(n, None)}", fillcolor="{color}"];')
    for a, b, rid in edges:
        lines.append(f's_{a} -> s_{b} [label="{rid}"];')
    lines.append("}")
    return "\n".join(lines)


def legend_markdown() -> str:
    return (
        "**Legend:** "
        f"Facts {LAYER_COLORS['fact']}, "
        f"Findings {LAYER_COLORS['finding']}, "
        f"Root causes {LAYER_COLORS['cause']}, "
        f"Fixes {LAYER_COLORS['fix']}, "
        f"Verdicts {LAYER_COLORS['verdict']}. "
        "Edge labels = rule id."
    )
