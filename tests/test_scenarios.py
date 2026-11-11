"""Scenario expected diagnosis and what-if."""

from dss import analyze_answers, what_if_compare
from scenarios import SCENARIOS


def _top_problem_root(decision):
    for c in decision["root_causes"]:
        if c["id"] not in ("profile_healthy_be_patient", "impatience_quit_risk"):
            return c["id"]
    for c in decision["root_causes"]:
        return c["id"]
    return None


def test_scenarios_expected():
    for key, sc in SCENARIOS.items():
        out = analyze_answers(sc["answers"])
        top = _top_problem_root(out["decision"])
        expected = sc["expected_root_cause"]
        verdict = out["decision"]["verdict_id"]
        if expected in ("profile_healthy_be_patient",):
            assert verdict == sc["expected_verdict"], f"{key} verdict"
        else:
            causes = [c["id"] for c in out["decision"]["root_causes"][:3]]
            assert expected in causes or top == expected, f"{key} expected {expected} got {causes}"


def test_healthy_profile_not_forced_problem():
    sc = SCENARIOS["12_fully_optimised"]
    out = analyze_answers(sc["answers"])
    assert out["decision"]["verdict_id"] == "verdict_healthy_patient"


def test_what_if_changes_diagnosis():
    sc = SCENARIOS["1_new_fiverr_broad_high_price"]
    after = dict(sc["answers"])
    after["Q007"] = "1 focused"
    after["Q008"] = True
    after["Q015"] = "Slightly lower"
    cmp = what_if_compare(sc["answers"], after)
    assert cmp["verdict_before"] != cmp["verdict_after"] or cmp["top_action_before"] != cmp["top_action_after"]
