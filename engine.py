"""
Generic forward-chaining inference engine (no domain knowledge).
"""

from __future__ import annotations

from typing import Any

MAX_PASSES = 200


def _condition_met(memory: dict[str, float], cond: Any) -> tuple[bool, float]:
    """Return whether condition is satisfied and its certainty."""
    if isinstance(cond, dict) and "not" in cond:
        key = cond["not"]
        if key in memory and memory[key] > 0:
            return False, 1.0
        return True, 1.0
    if isinstance(cond, str):
        if cond not in memory:
            return False, 1.0
        return memory[cond] > 0, memory[cond]
    return False, 1.0


def _rule_conditions_met(memory: dict[str, float], conditions: list[Any]) -> tuple[bool, float]:
    """All conditions ANDed; certainty is min of satisfied condition certainties."""
    if not conditions:
        return False, 1.0
    min_cf = 1.0
    for c in conditions:
        ok, cert = _condition_met(memory, c)
        if not ok:
            return False, 1.0
        min_cf = min(min_cf, cert)
    return True, min_cf


def combine_certainties(old: float, new: float) -> float:
    """Standard CF combination: old + new * (1 - old)."""
    return old + new * (1.0 - old)


def run_engine(initial_facts: dict[str, float], rules: list[dict]) -> dict[str, Any]:
    """
    Forward chaining until no new conclusions.

    Returns dict with keys: memory, fired_rules, provenance (conclusion -> parent conditions used).
    """
    memory = dict(initial_facts)
    fired: list[dict] = []
    fired_ids: set[str] = set()
    provenance: dict[str, list[str]] = {k: [k] for k in initial_facts}

    for _round in range(MAX_PASSES):
        any_new = False
        for rule in rules:
            rid = rule["id"]
            if rid in fired_ids:
                continue
            ok, cond_cert = _rule_conditions_met(memory, rule["if"])
            if not ok:
                continue
            conclusion = rule["then"]
            new_cert = rule["cf"] * cond_cert
            old_cert = memory.get(conclusion, 0.0)
            if old_cert > 0:
                combined = combine_certainties(old_cert, new_cert)
            else:
                combined = new_cert
            if combined > old_cert + 1e-9 or conclusion not in memory:
                memory[conclusion] = combined
                any_new = True
            elif combined < old_cert:
                memory[conclusion] = old_cert

            fired_ids.add(rid)
            fired.append(
                {
                    "id": rid,
                    "layer": rule["layer"],
                    "rule": rule,
                    "conclusion": conclusion,
                    "certainty": memory[conclusion],
                    "round": _round + 1,
                    "conditions": list(rule["if"]),
                }
            )
            parents = []
            for c in rule["if"]:
                if isinstance(c, dict) and "not" in c:
                    parents.append(c["not"])
                elif isinstance(c, str):
                    parents.append(c)
            provenance[conclusion] = parents
        if not any_new:
            break

    return {"memory": memory, "fired_rules": fired, "provenance": provenance}
