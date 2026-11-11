"""
Human-readable explanations from fired rules.
"""

from __future__ import annotations

from facts import FACT_DEFINITIONS
from knowledge_meta import FIXES, ROOT_CAUSES

_fact_to_question: dict[str, str] = {}
for _fd in FACT_DEFINITIONS:
    for mapping in _fd.get("maps", {}).values():
        for key in mapping:
            _fact_to_question.setdefault(key, _fd["question"])


def explain_root_causes(fired_rules: list[dict], memory: dict[str, float]) -> list[dict]:
    """Short paragraph per root cause with rule citations."""
    explanations = []
    for rc_id, meta in ROOT_CAUSES.items():
        cf = memory.get(rc_id, 0.0)
        if cf < 0.05:
            continue
        related = [f for f in fired_rules if f["conclusion"] == rc_id or rc_id in str(f)]
        rule_ids = []
        for fr in fired_rules:
            if fr["rule"]["then"] == rc_id or fr["conclusion"] == rc_id:
                rule_ids.append(fr["id"])
        premises = []
        for fr in fired_rules:
            if fr["rule"]["then"] == rc_id:
                for c in fr["rule"]["if"]:
                    if isinstance(c, str) and c in _fact_to_question:
                        premises.append(_fact_to_question[c])
        prem_text = ", ".join(premises[:4]) if premises else "your reported profile patterns"
        text = (
            f"Because you reported issues around {prem_text}, the system derived "
            f"{meta['name']} (confidence {cf*100:.0f}%). "
            f"Rules cited: {', '.join(rule_ids[:5]) or 'N/A'}."
        )
        explanations.append({"root_cause": rc_id, "title": meta["name"], "text": text})
    explanations.sort(key=lambda x: memory.get(x["root_cause"], 0), reverse=True)
    return explanations


def explain_fix_chain(fired_rules: list[dict], top_fix_id: str | None) -> str:
    if not top_fix_id or top_fix_id not in FIXES:
        return ""
    meta = FIXES[top_fix_id]
    chain = [rid for fr in fired_rules if fr["rule"]["then"] == top_fix_id for rid in [fr["id"]]]
    rc = meta["root_cause"]
    rc_rules = [fr["id"] for fr in fired_rules if fr["rule"]["then"] == rc]
    return (
        f"Recommended fix '{meta['name']}' links to root cause "
        f"'{ROOT_CAUSES[rc]['name']}' via rules {', '.join(rc_rules[:3])}, "
        f"then fix rules {', '.join(chain[:3])}."
    )
