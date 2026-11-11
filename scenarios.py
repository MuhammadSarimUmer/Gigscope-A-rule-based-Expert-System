"""
Pre-made demo cases for UI and tests.
"""

from __future__ import annotations

from facts import default_answers

SCENARIOS: dict[str, dict] = {}


def _healthy_baseline() -> dict:
    """Sensible 'average good' answers so only scenario overrides create problems."""
    a = default_answers()
    overrides = {
        "Q001": "Fiverr",
        "Q002": "6–12 months",
        "Q003": "Level 1 or Rising",
        "Q004": "Over 80%",
        "Q005": True,
        "Q006": True,
        "Q007": "2–3 related",
        "Q008": True,
        "Q009": "Average",
        "Q010": "2–4",
        "Q011": True,
        "Q012": "Specialist",
        "Q013": True,
        "Q014": "Stable",
        "Q015": "About average",
        "Q016": False,
        "Q017": True,
        "Q018": True,
        "Q019": False,
        "Q020": "Fixed packages",
        "Q021": False,
        "Q022": True,
        "Q023": True,
        "Q024": True,
        "Q025": True,
        "Q026": True,
        "Q027": True,
        "Q028": False,
        "Q029": "Professional",
        "Q030": True,
        "Q031": "3–5",
        "Q032": True,
        "Q033": True,
        "Q034": True,
        "Q035": True,
        "Q036": True,
        "Q037": "1–6 hours",
        "Q038": "95%+",
        "Q039": True,
        "Q040": True,
        "Q041": "On time",
        "Q042": True,
        "Q043": "5–19",
        "Q044": "4.5–4.7",
        "Q045": False,
        "Q046": "A few",
        "Q047": "95%+",
        "Q048": False,
        "Q049": True,
        "Q050": "0 / N/A",
        "Q051": True,
        "Q052": "Short and focused",
        "Q053": "Yes",
        "Q054": "N/A",
        "Q055": "N/A",
        "Q056": True,
        "Q057": "Average",
        "Q058": "Average",
        "Q059": "Good",
        "Q060": "Over 3 months",
        "Q061": "This month",
        "Q062": False,
        "Q063": "5–15",
        "Q064": "2–3",
        "Q065": "1–3 months",
        "Q066": True,
    }
    a.update(overrides)
    return a


def _set(a: dict, **kwargs) -> dict:
    out = dict(a)
    for k, v in kwargs.items():
        out[k] = v
    return out


# 1 Brand-new Fiverr seller, broad niche, high prices, no reviews
SCENARIOS["1_new_fiverr_broad_high_price"] = {
    "name": "New Fiverr seller: broad niche, high price, no reviews",
    "answers": _set(
        _healthy_baseline(),
        Q001="Fiverr",
        Q002="Under 1 month",
        Q003="New / no level",
        Q007="7 or more unrelated",
        Q008=False,
        Q015="Much higher",
        Q043="0",
        Q057="Very low",
    ),
    "expected_root_cause": "niche_too_broad",
    "expected_verdict": "verdict_fix_positioning",
}

# 2 Great skills but very slow replies
SCENARIOS["2_slow_replies_skilled"] = {
    "name": "Skilled seller with very slow replies",
    "answers": _set(_healthy_baseline(), Q010="5+", Q037="Over 24 hours", Q038="Under 70%", Q031="6+"),
    "expected_root_cause": "slow_response_time",
    "expected_verdict": "verdict_fix_communication",
}

# 3 Upwork copy-paste proposals
SCENARIOS["3_upwork_template_proposals"] = {
    "name": "Upwork: copy-paste proposals",
    "answers": _set(
        _healthy_baseline(),
        Q001="Upwork",
        Q050="1–5",
        Q051=False,
        Q052="Very long",
        Q053="No",
        Q054="Low",
        Q055="Poor",
    ),
    "expected_root_cause": "poor_proposals",
    "expected_verdict": "verdict_fix_communication",
}

# 4 Healthy profile just new
SCENARIOS["4_healthy_new_patient"] = {
    "name": "Healthy profile that is just new",
    "answers": _set(
        _healthy_baseline(),
        Q002="Under 1 month",
        Q003="New / no level",
        Q043="0",
        Q057="Low",
        Q065="3+ months",
    ),
    "expected_root_cause": "profile_healthy_be_patient",
    "expected_verdict": "verdict_healthy_patient",
}

# 5 Good gig weak images no video
SCENARIOS["5_weak_images"] = {
    "name": "Good gig copy but weak images, no video",
    "answers": _set(_healthy_baseline(), Q029="Poor", Q030=False, Q035=False),
    "expected_root_cause": "weak_gig_images_no_video",
    "expected_verdict": "verdict_fix_conversion",
}

# 6 Underpriced
SCENARIOS["6_underpriced"] = {
    "name": "Underpriced seller signaling low quality",
    "answers": _set(_healthy_baseline(), Q015="Much lower", Q016=True),
    "expected_root_cause": "price_too_low_quality_signal",
    "expected_verdict": "verdict_fix_pricing",
}

# 7 Good visibility poor conversion
SCENARIOS["7_visibility_ok_conversion_poor"] = {
    "name": "Good visibility, poor conversion",
    "answers": _set(_healthy_baseline(), Q057="High", Q058="Strong", Q059="Poor", Q043="0"),
    "expected_root_cause": "low_conversion_orders",
    "expected_verdict": "verdict_fix_conversion",
}

# 8 Recent bad review
SCENARIOS["8_bad_review_damage"] = {
    "name": "Recent bad review and cancellations",
    "answers": _set(_healthy_baseline(), Q045=True, Q048=True, Q047="Below 85%", Q044="Below 4.0"),
    "expected_root_cause": "bad_review_cancellation_damage",
    "expected_verdict": "verdict_fix_trust",
}

# 9 Wrong target market
SCENARIOS["9_wrong_market"] = {
    "name": "Wrong target market / timezone",
    "answers": _set(_healthy_baseline(), Q040=False),
    "expected_root_cause": "wrong_target_clients",
    "expected_verdict": "verdict_fix_positioning",
}

# 10 Too many unrelated gigs
SCENARIOS["10_too_many_gigs"] = {
    "name": "Too many unrelated gigs",
    "answers": _set(_healthy_baseline(), Q007="7 or more unrelated", Q064="7+", Q013=False),
    "expected_root_cause": "too_many_unrelated_gigs",
    "expected_verdict": "verdict_fix_positioning",
}

# 11 Multiple problems
SCENARIOS["11_multiple_problems"] = {
    "name": "Multiple problems at once",
    "answers": _set(
        _healthy_baseline(),
        Q007="4–6",
        Q015="Much higher",
        Q029="Poor",
        Q037="6–24 hours",
        Q043="0",
        Q051=False,
        Q001="Both",
        Q050="1–5",
    ),
    "expected_root_cause": "no_reviews_social_proof",
    "expected_verdict": "verdict_fix_trust",
}

# 12 Fully optimised experienced
SCENARIOS["12_fully_optimised"] = {
    "name": "Fully optimised experienced profile",
    "answers": _set(
        _healthy_baseline(),
        Q002="Over 1 year",
        Q003="Top Rated / Level 2+",
        Q043="20+",
        Q044="4.8–5.0",
        Q046="Many",
        Q057="High",
        Q058="Strong",
        Q059="Good",
        Q065="3+ months",
    ),
    "expected_root_cause": "profile_healthy_be_patient",
    "expected_verdict": "verdict_healthy_patient",
}
