"""
Decision making and decision support: scoring, ranking, action plans, what-if.
"""

from __future__ import annotations

from typing import Any

from engine import run_engine
from facts import answers_to_facts
from knowledge_meta import FIXES, ROOT_CAUSES, VERDICTS
from rules import RULES

DEFAULT_WEIGHTS = {
    "w_impact": 0.35,
    "w_effort": 0.25,
    "w_cost": 0.15,
    "w_conf": 0.25,
}

MIN_ROOT_CAUSE_CF = 0.40

_HEALTHY_CAUSES = frozenset({"profile_healthy_be_patient", "impatience_quit_risk"})


def _normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        return dict(DEFAULT_WEIGHTS)
    return {k: v / total for k, v in weights.items()}


def score_fix(fix_id: str, memory: dict[str, float], weights: dict[str, float]) -> dict[str, Any]:
    """Compute priority score for one fix."""
    meta = FIXES[fix_id]
    w = _normalize_weights(weights)
    rc = meta["root_cause"]
    confidence = memory.get(rc, 0.0)
    impact = meta["impact"]
    effort = meta["effort"]
    cost = meta["cost"]
    score = (
        w["w_impact"] * impact
        + w["w_effort"] * (10 - effort)
        + w["w_cost"] * (10 - cost)
        + w["w_conf"] * confidence * 10
    )
    return {
        "fix_id": fix_id,
        "name": meta["name"],
        "root_cause": rc,
        "root_cause_name": ROOT_CAUSES[rc]["name"],
        "impact": impact,
        "effort": effort,
        "cost": cost,
        "days_to_results": meta["days_to_results"],
        "confidence": confidence,
        "score": round(score, 3),
    }


def rank_fixes(memory: dict[str, float], weights: dict[str, float] | None = None) -> list[dict]:
    """Rank fixes linked to root causes that cleared the confidence threshold."""
    w = weights or DEFAULT_WEIGHTS
    candidates = []
    for fix_id in FIXES:
        rc = FIXES[fix_id]["root_cause"]
        if memory.get(rc, 0) >= MIN_ROOT_CAUSE_CF:
            candidates.append(score_fix(fix_id, memory, w))
    candidates.sort(key=lambda x: x["score"], reverse=True)
    for i, row in enumerate(candidates, start=1):
        row["rank"] = i
    return candidates


def top_root_causes(memory: dict[str, float]) -> list[dict]:
    rows = []
    for rc_id, meta in ROOT_CAUSES.items():
        cf = memory.get(rc_id, 0.0)
        if cf > 0:
            rows.append({"id": rc_id, "name": meta["name"], "confidence": cf})
    rows.sort(key=lambda x: x["confidence"], reverse=True)
    return rows


_CAUSE_TO_VERDICT: dict[str, str] = {
    "niche_too_broad": "verdict_fix_positioning",
    "niche_oversaturated": "verdict_fix_positioning",
    "too_many_unrelated_gigs": "verdict_fix_positioning",
    "wrong_target_clients": "verdict_fix_positioning",
    "price_too_high_maturity": "verdict_fix_pricing",
    "price_too_low_quality_signal": "verdict_fix_pricing",
    "weak_packages": "verdict_fix_pricing",
    "poor_gig_title_seo": "verdict_fix_visibility",
    "low_ctr_attraction": "verdict_fix_visibility",
    "too_few_gigs_low_activity": "verdict_fix_visibility",
    "low_conversion_orders": "verdict_fix_conversion",
    "weak_gig_images_no_video": "verdict_fix_conversion",
    "slow_response_time": "verdict_fix_communication",
    "low_response_rate": "verdict_fix_communication",
    "inconsistent_online_presence": "verdict_fix_communication",
    "poor_proposals": "verdict_fix_communication",
    "proposal_volume_too_low": "verdict_fix_communication",
    "no_reviews_social_proof": "verdict_fix_trust",
    "thin_irrelevant_portfolio": "verdict_fix_trust",
    "bad_review_cancellation_damage": "verdict_fix_trust",
    "unverified_incomplete_account": "verdict_fix_trust",
    "weak_profile_description": "verdict_fix_trust",
    "profile_healthy_be_patient": "verdict_healthy_patient",
    "impatience_quit_risk": "verdict_healthy_patient",
}


def pick_verdict(memory: dict[str, float]) -> tuple[str, str, float]:
    """Return verdict id, name, confidence. Defaults to healthy patient if weak causes."""
    causes = top_root_causes(memory)
    problem_causes = [c for c in causes if c["id"] not in ("profile_healthy_be_patient", "impatience_quit_risk")]
    top_problem = problem_causes[0] if problem_causes else None

    if top_problem and top_problem["confidence"] >= MIN_ROOT_CAUSE_CF:
        healthy_cf = memory.get("profile_healthy_be_patient", 0.0)
        if healthy_cf >= MIN_ROOT_CAUSE_CF and healthy_cf >= top_problem["confidence"] * 0.95:
            if top_problem["id"] in ("no_reviews_social_proof", "impatience_quit_risk") or healthy_cf >= top_problem["confidence"]:
                vid = "verdict_healthy_patient"
                return vid, VERDICTS[vid]["name"], memory.get(vid, healthy_cf)

        mapped = _CAUSE_TO_VERDICT.get(top_problem["id"], "verdict_fix_conversion")
        return mapped, VERDICTS[mapped]["name"], top_problem["confidence"]

    vid = "verdict_healthy_patient"
    return vid, VERDICTS[vid]["name"], memory.get(vid, memory.get("profile_healthy_be_patient", 0.85))


def build_verdict_detail(
    verdict_id: str,
    memory: dict[str, float],
    root_causes: list[dict],
    top_action: dict | None,
) -> dict[str, Any]:
    """Rich verdict payload for the UI (text, lists, supporting metrics)."""
    meta = VERDICTS.get(verdict_id, {})
    verdict_cf = memory.get(verdict_id, 0.0)
    if verdict_cf <= 0:
        verdict_cf = next((c["confidence"] for c in root_causes if c["id"] not in _HEALTHY_CAUSES), 0.0)
        if verdict_id == "verdict_healthy_patient":
            verdict_cf = max(verdict_cf, memory.get("profile_healthy_be_patient", 0.85))

    problems = [
        c for c in root_causes if c["id"] not in _HEALTHY_CAUSES and c["confidence"] >= MIN_ROOT_CAUSE_CF
    ]
    healthy = next((c for c in root_causes if c["id"] in _HEALTHY_CAUSES), None)

    supporting = []
    for c in problems[:5]:
        rc = ROOT_CAUSES.get(c["id"], {})
        supporting.append(
            {
                "id": c["id"],
                "name": c["name"],
                "confidence": c["confidence"],
                "description": rc.get("description", ""),
            }
        )

    primary = problems[0] if problems else healthy
    headline = meta.get("detail", meta.get("description", ""))
    if primary and verdict_id != "verdict_healthy_patient":
        headline += (
            f"\n\n**Primary driver:** {primary['name']} "
            f"({primary['confidence'] * 100:.0f}% confidence) — "
            f"{ROOT_CAUSES.get(primary['id'], {}).get('description', '')}"
        )
    elif healthy:
        headline += (
            f"\n\n**Stability signal:** {healthy['name']} "
            f"({healthy['confidence'] * 100:.0f}% confidence)."
        )

    if top_action:
        headline += (
            f"\n\n**First move:** {top_action['name']} — targets "
            f"{top_action['root_cause_name']} (priority score {top_action['score']:.2f})."
        )

    return {
        "verdict_id": verdict_id,
        "title": meta.get("name", verdict_id),
        "summary": meta.get("description", ""),
        "detail_markdown": headline,
        "focus_areas": meta.get("focus_areas", []),
        "next_steps": meta.get("next_steps", []),
        "confidence": verdict_cf,
        "supporting_causes": supporting,
        "primary_cause": primary,
    }


def make_decision(memory: dict[str, float], weights: dict[str, float] | None = None) -> dict[str, Any]:
    """Top action, verdict, and plain-language statement."""
    ranked = rank_fixes(memory, weights)
    verdict_id, verdict_name, verdict_cf = pick_verdict(memory)
    top_action = ranked[0] if ranked else None

    causes = top_root_causes(memory)
    problem = next(
        (c for c in causes if c["id"] not in ("profile_healthy_be_patient", "impatience_quit_risk")),
        None,
    )

    if verdict_id == "verdict_healthy_patient" or not problem or problem["confidence"] < MIN_ROOT_CAUSE_CF:
        statement = (
            "No major structural issue crossed the confidence threshold. "
            "Verdict: profile looks healthy — be patient and stay consistent."
        )
    elif top_action:
        statement = (
            f"Your biggest problem is likely {problem['name']} "
            f"(confidence {problem['confidence']*100:.0f}%). "
            f"Do this first: {top_action['name']}."
        )
    else:
        statement = f"Focus on {problem['name']} (confidence {problem['confidence']*100:.0f}%)."

    verdict_detail = build_verdict_detail(verdict_id, memory, causes, top_action)

    return {
        "verdict_id": verdict_id,
        "verdict_name": verdict_name,
        "verdict_confidence": verdict_detail["confidence"],
        "verdict_detail": verdict_detail,
        "top_action": top_action,
        "statement": statement,
        "root_causes": causes,
        "ranked_fixes": ranked,
    }


def action_plan(ranked_fixes: list[dict]) -> dict[str, list[str]]:
    """Bucket fixes into 7/14/30 day plans by effort and days_to_results."""
    plan = {"7_days": [], "14_days": [], "30_days": []}
    for row in ranked_fixes[:12]:
        days = row["days_to_results"]
        effort = row["effort"]
        label = row["name"]
        if days <= 7 and effort <= 5:
            plan["7_days"].append(label)
        elif days <= 14:
            plan["14_days"].append(label)
        else:
            plan["30_days"].append(label)
    return plan


def analyze_answers(answers: dict, weights: dict[str, float] | None = None) -> dict[str, Any]:
    """Full pipeline: facts -> engine -> decision."""
    facts = answers_to_facts(answers)
    result = run_engine(facts, RULES)
    decision = make_decision(result["memory"], weights)
    return {
        "facts": facts,
        "engine": result,
        "decision": decision,
        "action_plan": action_plan(decision["ranked_fixes"]),
    }


def what_if_compare(
    before_answers: dict,
    after_answers: dict,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Run before/after analysis for DSS what-if panel."""
    before = analyze_answers(before_answers, weights)
    after = analyze_answers(after_answers, weights)

    def cause_map(analysis):
        return {c["id"]: c["confidence"] for c in analysis["decision"]["root_causes"]}

    b_map = cause_map(before)
    a_map = cause_map(after)
    all_ids = set(b_map) | set(a_map)
    changes = []
    for cid in all_ids:
        changes.append(
            {
                "id": cid,
                "name": ROOT_CAUSES.get(cid, {}).get("name", cid),
                "before": b_map.get(cid, 0.0),
                "after": a_map.get(cid, 0.0),
                "delta": a_map.get(cid, 0.0) - b_map.get(cid, 0.0),
            }
        )
    changes.sort(key=lambda x: abs(x["delta"]), reverse=True)

    b_top = before["decision"]["top_action"]
    a_top = after["decision"]["top_action"]
    return {
        "before": before,
        "after": after,
        "cause_changes": changes,
        "top_action_before": b_top["name"] if b_top else None,
        "top_action_after": a_top["name"] if a_top else None,
        "verdict_before": before["decision"]["verdict_name"],
        "verdict_after": after["decision"]["verdict_name"],
    }
