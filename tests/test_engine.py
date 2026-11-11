"""Tests for forward-chaining engine and certainty math."""

from engine import combine_certainties, run_engine
from rules import RULES


def test_combine_certainties_hand_calc():
    # old=0.6, new=0.5 -> 0.6 + 0.5*(1-0.6) = 0.8
    assert abs(combine_certainties(0.6, 0.5) - 0.8) < 1e-6


def test_rule_fires_once():
    facts = {"services_scattered": 1.0, "niche_unclear": 1.0}
    result = run_engine(facts, RULES)
    ids = [f["id"] for f in result["fired_rules"]]
    assert len(ids) == len(set(ids))


def test_forward_chain_produces_finding():
    facts = {"title_keyword_no": 1.0}
    result = run_engine(facts, RULES)
    assert result["memory"].get("weak_gig_seo", 0) > 0
