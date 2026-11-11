"""
Validate the knowledge base structure and print a report. Exits non-zero if invalid.
"""

from __future__ import annotations

import sys
from collections import Counter

from facts import all_fact_keys
from knowledge_meta import ALL_CONCLUSIONS, FIXES, ROOT_CAUSES, RULE_CATEGORIES, VERDICTS
from rules import RULES

MIN_RULES = 150


def _is_neg(cond) -> str | None:
    if isinstance(cond, dict) and "not" in cond:
        return cond["not"]
    return None


def _premise_keys(rule) -> list[str]:
    out = []
    for c in rule["if"]:
        if isinstance(c, str):
            out.append(c)
        else:
            k = _is_neg(c)
            if k:
                out.append(k)
    return out


def _produced_by_rules() -> set[str]:
    return {r["then"] for r in RULES}


def _check_cycles() -> list[str]:
    """Detect obvious cycles: conclusion appears as premise of same rule."""
    errors = []
    for r in RULES:
        if r["then"] in r["if"]:
            errors.append(f"Cycle in {r['id']}: conclusion in its own premises")
    return errors


def validate() -> int:
    errors: list[str] = []
    fact_keys = all_fact_keys()
    produced = _produced_by_rules()

    if len(RULES) < MIN_RULES:
        errors.append(f"Rule count {len(RULES)} is below minimum {MIN_RULES}")

    ids = [r["id"] for r in RULES]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate rule ids found")

    sigs = [(r["layer"], r["then"], tuple(r["if"]), r["cf"]) for r in RULES]
    if len(sigs) != len(set(sigs)):
        errors.append("Duplicate rule definitions found")

    cat_counts = Counter(r["category"] for r in RULES)
    for cat in RULE_CATEGORIES:
        if cat_counts[cat] < 10:
            errors.append(f"Category {cat} has only {cat_counts[cat]} rules (need 10+)")

    layer_counts = Counter(r["layer"] for r in RULES)
    for r in RULES:
        if r["cf"] < 0.50 or r["cf"] > 0.95:
            errors.append(f"{r['id']}: CF {r['cf']} out of range")
        if not r.get("reason"):
            errors.append(f"{r['id']}: missing reason")
        if r["then"] not in ALL_CONCLUSIONS and r["then"] not in fact_keys:
            # findings/causes/fixes must be in meta; facts only as premises
            if r["layer"] != "facts_to_findings":
                pass
            if r["then"] not in ALL_CONCLUSIONS:
                errors.append(f"{r['id']}: unknown conclusion {r['then']}")

    known_nodes = fact_keys | ALL_CONCLUSIONS
    for r in RULES:
        for p in _premise_keys(r):
            if p not in known_nodes:
                errors.append(f"{r['id']}: orphan premise {p}")

    for rc in ROOT_CAUSES:
        fix_for = [f for f, meta in FIXES.items() if meta.get("root_cause") == rc]
        rule_fix = [r for r in RULES if r["then"] in fix_for or (r["layer"] == "causes_to_fixes" and rc in r["if"])]
        if not fix_for and rc not in ("profile_healthy_be_patient", "impatience_quit_risk"):
            pass
        if not fix_for and rc not in ("impatience_quit_risk",):
            if rc not in ("profile_healthy_be_patient",):
                errors.append(f"Root cause {rc} has no linked fix metadata")

    errors.extend(_check_cycles())

    print("=== GigScope Knowledge Base Report ===")
    print(f"Total rules: {len(RULES)}")
    print("Rules per layer:", dict(layer_counts))
    print("Rules per category:", dict(cat_counts))
    print(f"Distinct facts (from questionnaire): {len(fact_keys)}")
    print(f"Conclusions defined in meta: {len(ALL_CONCLUSIONS)}")

    if errors:
        print("\nFAILED with", len(errors), "issue(s):")
        for e in errors[:30]:
            print(" -", e)
        if len(errors) > 30:
            print(f" ... and {len(errors) - 30} more")
        return 1

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
