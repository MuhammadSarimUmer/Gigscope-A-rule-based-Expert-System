"""
Input questionnaire definitions and conversion from answers to engine facts.
"""

from __future__ import annotations

from typing import Any

# Each definition: id, category, question, input_type, options (for choice), fact_keys produced
FACT_DEFINITIONS: list[dict[str, Any]] = [
    # Account basics (6)
    {"id": "Q001", "category": "account", "question": "Primary platform?", "type": "choice",
     "options": ["Fiverr", "Upwork", "Both"], "maps": {"Fiverr": ["platform_fiverr"], "Upwork": ["platform_upwork"], "Both": ["platform_fiverr", "platform_upwork"]}},
    {"id": "Q002", "category": "account", "question": "Account age?", "type": "choice",
     "options": ["Under 1 month", "1–6 months", "6–12 months", "Over 1 year"],
     "maps": {"Under 1 month": ["account_under_1m", "account_new"], "1–6 months": ["account_1_6m"], "6–12 months": ["account_6_12m"], "Over 1 year": ["account_over_1y", "account_mature"]}},
    {"id": "Q003", "category": "account", "question": "Seller level / status?", "type": "choice",
     "options": ["New / no level", "Level 1 or Rising", "Top Rated / Level 2+"],
     "maps": {"New / no level": ["level_new"], "Level 1 or Rising": ["level_mid"], "Top Rated / Level 2+": ["level_top"]}},
    {"id": "Q004", "category": "account", "question": "Profile completeness?", "type": "choice",
     "options": ["Under 50%", "50–80%", "Over 80%"],
     "maps": {"Under 50%": ["profile_low_complete"], "50–80%": ["profile_mid_complete"], "Over 80%": ["profile_high_complete"]}},
    {"id": "Q005", "category": "account", "question": "ID / payment verified?", "type": "yesno",
     "maps": {True: ["verified_yes"], False: ["verified_no"]}},
    {"id": "Q006", "category": "account", "question": "Professional profile photo?", "type": "yesno",
     "maps": {True: ["pro_photo_yes"], False: ["pro_photo_no"]}},
    # Niche and skills (8)
    {"id": "Q007", "category": "niche", "question": "How many different services do you offer?", "type": "choice",
     "options": ["1 focused", "2–3 related", "4–6", "7 or more unrelated"],
     "maps": {"1 focused": ["services_one"], "2–3 related": ["services_few"], "4–6": ["services_many"], "7 or more unrelated": ["services_scattered"]}},
    {"id": "Q008", "category": "niche", "question": "Can you describe your niche in one sentence?", "type": "yesno",
     "maps": {True: ["niche_clear"], False: ["niche_unclear"]}},
    {"id": "Q009", "category": "niche", "question": "Your skill demand on the platform?", "type": "choice",
     "options": ["High demand", "Average", "Oversaturated"],
     "maps": {"High demand": ["demand_high"], "Average": ["demand_avg"], "Oversaturated": ["demand_saturated"]}},
    {"id": "Q010", "category": "niche", "question": "Years of real-world experience?", "type": "choice",
     "options": ["0–1", "2–4", "5+"], "maps": {"0–1": ["exp_low"], "2–4": ["exp_mid"], "5+": ["exp_high"]}},
    {"id": "Q011", "category": "niche", "question": "Relevant certifications shown?", "type": "yesno",
     "maps": {True: ["certs_yes"], False: ["certs_no"]}},
    {"id": "Q012", "category": "niche", "question": "You compete mainly as specialist or generalist?", "type": "choice",
     "options": ["Specialist", "Generalist"],
     "maps": {"Specialist": ["role_specialist"], "Generalist": ["role_generalist"]}},
    {"id": "Q013", "category": "niche", "question": "Same keyword theme across gigs?", "type": "yesno",
     "maps": {True: ["keyword_theme_yes"], False: ["keyword_theme_no"]}},
    {"id": "Q014", "category": "niche", "question": "Trending vs declining niche?", "type": "choice",
     "options": ["Growing", "Stable", "Declining"],
     "maps": {"Growing": ["trend_growing"], "Stable": ["trend_stable"], "Declining": ["trend_declining"]}},
    # Pricing (7)
    {"id": "Q015", "category": "pricing", "question": "Your price vs market average?", "type": "choice",
     "options": ["Much lower", "Slightly lower", "About average", "Above average", "Much higher"],
     "maps": {"Much lower": ["price_much_lower"], "Slightly lower": ["price_slightly_lower"], "About average": ["price_average"],
              "Above average": ["price_above_avg"], "Much higher": ["price_much_higher"]}},
    {"id": "Q016", "category": "pricing", "question": "Using new-seller discount strategy?", "type": "yesno",
     "maps": {True: ["discount_strategy_yes"], False: ["discount_strategy_no"]}},
    {"id": "Q017", "category": "pricing", "question": "Offer tiered packages?", "type": "yesno",
     "maps": {True: ["packages_yes"], False: ["packages_no"]}},
    {"id": "Q018", "category": "pricing", "question": "Offer gig extras / add-ons?", "type": "yesno",
     "maps": {True: ["extras_yes"], False: ["extras_no"]}},
    {"id": "Q019", "category": "pricing", "question": "Large jump between basic and premium?", "type": "yesno",
     "maps": {True: ["price_jump_yes"], False: ["price_jump_no"]}},
    {"id": "Q020", "category": "pricing", "question": "Main pricing model?", "type": "choice",
     "options": ["Fixed packages", "Hourly", "Mix"],
     "maps": {"Fixed packages": ["pricing_fixed"], "Hourly": ["pricing_hourly"], "Mix": ["pricing_mix"]}},
    {"id": "Q021", "category": "pricing", "question": "Buyers mention price as objection?", "type": "yesno",
     "maps": {True: ["price_objection_yes"], False: ["price_objection_no"]}},
    # Gig title and SEO (7)
    {"id": "Q022", "category": "seo", "question": "Primary keyword in gig title?", "type": "yesno",
     "maps": {True: ["title_keyword_yes"], False: ["title_keyword_no"]}},
    {"id": "Q023", "category": "seo", "question": "Title length appropriate (not stuffed)?", "type": "yesno",
     "maps": {True: ["title_length_ok"], False: ["title_length_bad"]}},
    {"id": "Q024", "category": "seo", "question": "All tags slots used well?", "type": "yesno",
     "maps": {True: ["tags_good"], False: ["tags_poor"]}},
    {"id": "Q025", "category": "seo", "question": "Description over 300 words with structure?", "type": "yesno",
     "maps": {True: ["desc_long_ok"], False: ["desc_short"]}},
    {"id": "Q026", "category": "seo", "question": "Search-friendly wording (buyer language)?", "type": "yesno",
     "maps": {True: ["seo_wording_good"], False: ["seo_wording_bad"]}},
    {"id": "Q027", "category": "seo", "question": "Grammar and spelling polished?", "type": "yesno",
     "maps": {True: ["language_good"], False: ["language_bad"]}},
    {"id": "Q028", "category": "seo", "question": "Multiple gigs targeting same keyword?", "type": "yesno",
     "maps": {True: ["keyword_cannibal_yes"], False: ["keyword_cannibal_no"]}},
    # Visuals and portfolio (8)
    {"id": "Q029", "category": "visuals", "question": "Gig image quality?", "type": "choice",
     "options": ["Professional", "Average", "Poor"],
     "maps": {"Professional": ["gig_image_pro"], "Average": ["gig_image_avg"], "Poor": ["gig_image_poor"]}},
    {"id": "Q030", "category": "visuals", "question": "Gig video present?", "type": "yesno",
     "maps": {True: ["gig_video_yes"], False: ["gig_video_no"]}},
    {"id": "Q031", "category": "portfolio", "question": "Portfolio sample count?", "type": "choice",
     "options": ["0", "1–2", "3–5", "6+"],
     "maps": {"0": ["portfolio_0"], "1–2": ["portfolio_1_2"], "3–5": ["portfolio_3_5"], "6+": ["portfolio_6plus"]}},
    {"id": "Q032", "category": "portfolio", "question": "Samples relevant to your gig?", "type": "yesno",
     "maps": {True: ["portfolio_relevant"], False: ["portfolio_irrelevant"]}},
    {"id": "Q033", "category": "visuals", "question": "Consistent branding across gigs?", "type": "yesno",
     "maps": {True: ["branding_yes"], False: ["branding_no"]}},
    {"id": "Q034", "category": "portfolio", "question": "Case studies or before/after shown?", "type": "yesno",
     "maps": {True: ["case_study_yes"], False: ["case_study_no"]}},
    {"id": "Q035", "category": "visuals", "question": "Thumbnail stands out in search?", "type": "yesno",
     "maps": {True: ["thumbnail_strong"], False: ["thumbnail_weak"]}},
    {"id": "Q036", "category": "portfolio", "question": "Portfolio updated in last 3 months?", "type": "yesno",
     "maps": {True: ["portfolio_fresh"], False: ["portfolio_stale"]}},
    # Communication (6)
    {"id": "Q037", "category": "communication", "question": "Average response time?", "type": "choice",
     "options": ["Under 1 hour", "1–6 hours", "6–24 hours", "Over 24 hours"],
     "maps": {"Under 1 hour": ["response_fast"], "1–6 hours": ["response_ok"], "6–24 hours": ["response_slow"], "Over 24 hours": ["response_very_slow"]}},
    {"id": "Q038", "category": "communication", "question": "Response rate to messages?", "type": "choice",
     "options": ["95%+", "70–94%", "Under 70%"],
     "maps": {"95%+": ["response_rate_high"], "70–94%": ["response_rate_mid"], "Under 70%": ["response_rate_low"]}},
    {"id": "Q039", "category": "communication", "question": "Messages professional and clear?", "type": "yesno",
     "maps": {True: ["message_quality_good"], False: ["message_quality_bad"]}},
    {"id": "Q040", "category": "communication", "question": "Online hours overlap buyer peak times?", "type": "yesno",
     "maps": {True: ["timezone_match"], False: ["timezone_mismatch"]}},
    {"id": "Q041", "category": "communication", "question": "Typical order delivery speed?", "type": "choice",
     "options": ["Early", "On time", "Often late"],
     "maps": {"Early": ["delivery_early"], "On time": ["delivery_ontime"], "Often late": ["delivery_late"]}},
    {"id": "Q042", "category": "communication", "question": "Offers free brief consultation?", "type": "yesno",
     "maps": {True: ["consult_yes"], False: ["consult_no"]}},
    # Reviews and reputation (7)
    {"id": "Q043", "category": "reviews", "question": "Total reviews?", "type": "choice",
     "options": ["0", "1–4", "5–19", "20+"],
     "maps": {"0": ["reviews_0"], "1–4": ["reviews_1_4"], "5–19": ["reviews_5_19"], "20+": ["reviews_20plus"]}},
    {"id": "Q044", "category": "reviews", "question": "Average rating?", "type": "choice",
     "options": ["4.8–5.0", "4.5–4.7", "4.0–4.4", "Below 4.0"],
     "maps": {"4.8–5.0": ["rating_high"], "4.5–4.7": ["rating_mid"], "4.0–4.4": ["rating_low"], "Below 4.0": ["rating_very_low"]}},
    {"id": "Q045", "category": "reviews", "question": "Negative review in last 60 days?", "type": "yesno",
     "maps": {True: ["recent_negative_yes"], False: ["recent_negative_no"]}},
    {"id": "Q046", "category": "reviews", "question": "Repeat clients?", "type": "choice",
     "options": ["None yet", "A few", "Many"],
     "maps": {"None yet": ["repeat_none"], "A few": ["repeat_few"], "Many": ["repeat_many"]}},
    {"id": "Q047", "category": "reviews", "question": "Order completion rate?", "type": "choice",
     "options": ["95%+", "85–94%", "Below 85%"],
     "maps": {"95%+": ["completion_high"], "85–94%": ["completion_mid"], "Below 85%": ["completion_low"]}},
    {"id": "Q048", "category": "reviews", "question": "Recent order cancellations?", "type": "yesno",
     "maps": {True: ["cancellations_recent"], False: ["cancellations_none"]}},
    {"id": "Q049", "category": "reviews", "question": "Publicly showcase testimonials?", "type": "yesno",
     "maps": {True: ["testimonials_yes"], False: ["testimonials_no"]}},
    # Proposals (7)
    {"id": "Q050", "category": "proposals", "question": "Proposals sent per week (Upwork)?", "type": "choice",
     "options": ["0 / N/A", "1–5", "6–15", "16+"],
     "maps": {"0 / N/A": ["proposals_0"], "1–5": ["proposals_low"], "6–15": ["proposals_mid"], "16+": ["proposals_high"]}},
    {"id": "Q051", "category": "proposals", "question": "Proposals personalised per job?", "type": "yesno",
     "maps": {True: ["proposal_personal"], False: ["proposal_template"]}},
    {"id": "Q052", "category": "proposals", "question": "Cover letter length?", "type": "choice",
     "options": ["Short and focused", "Medium", "Very long"],
     "maps": {"Short and focused": ["cover_short"], "Medium": ["cover_medium"], "Very long": ["cover_long"]}},
    {"id": "Q053", "category": "proposals", "question": "Connects used efficiently?", "type": "choice",
     "options": ["Yes", "Unsure", "No"],
     "maps": {"Yes": ["connects_efficient"], "Unsure": ["connects_unsure"], "No": ["connects_waste"]}},
    {"id": "Q054", "category": "proposals", "question": "Shortlist rate?", "type": "choice",
     "options": ["High", "Low", "N/A"],
     "maps": {"High": ["shortlist_high"], "Low": ["shortlist_low"], "N/A": ["shortlist_na"]}},
    {"id": "Q055", "category": "proposals", "question": "Interview rate?", "type": "choice",
     "options": ["Good", "Poor", "N/A"],
     "maps": {"Good": ["interview_good"], "Poor": ["interview_poor"], "N/A": ["interview_na"]}},
    {"id": "Q056", "category": "proposals", "question": "Bid only on well-matched jobs?", "type": "yesno",
     "maps": {True: ["bid_matched"], False: ["bid_spray"]}},
    # Activity and visibility (6)
    {"id": "Q057", "category": "activity", "question": "Impressions level?", "type": "choice",
     "options": ["Very low", "Low", "Average", "High"],
     "maps": {"Very low": ["impressions_very_low"], "Low": ["impressions_low"], "Average": ["impressions_avg"], "High": ["impressions_high"]}},
    {"id": "Q058", "category": "activity", "question": "Click-through rate?", "type": "choice",
     "options": ["Strong", "Average", "Weak", "Unknown"],
     "maps": {"Strong": ["ctr_strong"], "Average": ["ctr_avg"], "Weak": ["ctr_weak"], "Unknown": ["ctr_unknown"]}},
    {"id": "Q059", "category": "activity", "question": "Click-to-order conversion?", "type": "choice",
     "options": ["Good", "Poor", "Unknown"],
     "maps": {"Good": ["conversion_good"], "Poor": ["conversion_poor"], "Unknown": ["conversion_unknown"]}},
    {"id": "Q060", "category": "activity", "question": "Gig age?", "type": "choice",
     "options": ["Under 1 month", "1–3 months", "Over 3 months"],
     "maps": {"Under 1 month": ["gig_new"], "1–3 months": ["gig_young"], "Over 3 months": ["gig_mature"]}},
    {"id": "Q061", "category": "activity", "question": "Last gig update?", "type": "choice",
     "options": ["This week", "This month", "Over 1 month ago"],
     "maps": {"This week": ["update_recent"], "This month": ["update_month"], "Over 1 month ago": ["update_stale"]}},
    {"id": "Q062", "category": "activity", "question": "Used promoted gigs / ads?", "type": "yesno",
     "maps": {True: ["promo_used"], False: ["promo_not_used"]}},
    # Mindset and habits (4)
    {"id": "Q063", "category": "mindset", "question": "Hours per week on freelancing?", "type": "choice",
     "options": ["Under 5", "5–15", "15–30", "30+"],
     "maps": {"Under 5": ["hours_low"], "5–15": ["hours_mid"], "15–30": ["hours_high"], "30+": ["hours_very_high"]}},
    {"id": "Q064", "category": "mindset", "question": "Number of live gigs?", "type": "choice",
     "options": ["1", "2–3", "4–6", "7+"],
     "maps": {"1": ["gigs_one"], "2–3": ["gigs_few"], "4–6": ["gigs_many"], "7+": ["gigs_too_many"]}},
    {"id": "Q065", "category": "mindset", "question": "Patience with timeline (months without orders)?", "type": "choice",
     "options": ["Under 1 month", "1–3 months", "3+ months"],
     "maps": {"Under 1 month": ["patience_low"], "1–3 months": ["patience_mid"], "3+ months": ["patience_high"]}},
    {"id": "Q066", "category": "mindset", "question": "Consistent weekly routine?", "type": "yesno",
     "maps": {True: ["routine_yes"], False: ["routine_no"]}},
]


def default_answers() -> dict[str, Any]:
    """Empty-ish defaults for the questionnaire."""
    defaults: dict[str, Any] = {}
    for fd in FACT_DEFINITIONS:
        if fd["type"] == "yesno":
            defaults[fd["id"]] = False
        elif fd["type"] == "choice":
            defaults[fd["id"]] = fd["options"][0]
    return defaults


def answers_to_facts(answers: dict[str, Any]) -> dict[str, float]:
    """
    Convert questionnaire answers to working-memory facts at certainty 1.0.
    Keys are boolean fact ids used in rules.
    """
    facts: dict[str, float] = {}
    for fd in FACT_DEFINITIONS:
        qid = fd["id"]
        if qid not in answers:
            continue
        val = answers[qid]
        maps = fd.get("maps", {})
        if val in maps:
            for key in maps[val]:
                facts[key] = 1.0
        elif fd["type"] == "yesno" and isinstance(val, bool):
            for key in maps.get(val, []):
                facts[key] = 1.0
    return facts


def all_fact_keys() -> set[str]:
    """All fact keys that answers can produce."""
    keys: set[str] = set()
    for fd in FACT_DEFINITIONS:
        for m in fd.get("maps", {}).values():
            keys.update(m)
    return keys


def definitions_by_category() -> dict[str, list[dict]]:
    """Group definitions for UI expanders."""
    out: dict[str, list[dict]] = {}
    for fd in FACT_DEFINITIONS:
        out.setdefault(fd["category"], []).append(fd)
    return out
