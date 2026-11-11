"""
Knowledge base: all IF-THEN rules as data (150+ rules).
"""

from __future__ import annotations

from typing import Any


def _r(
    rid: str,
    layer: str,
    conditions: list[Any],
    conclusion: str,
    cf: float,
    reason: str,
    category: str,
) -> dict:
    return {
        "id": rid,
        "layer": layer,
        "if": conditions,
        "then": conclusion,
        "cf": cf,
        "reason": reason,
        "category": category,
    }


def _build_rules() -> list[dict]:
    rules: list[dict] = []
    n = 0

    def add(layer, cond, then, cf, reason, cat):
        nonlocal n
        n += 1
        rules.append(_r(f"R{n:03d}", layer, cond, then, cf, reason, cat))

    L1 = "facts_to_findings"
    L2 = "findings_to_causes"
    L3 = "causes_to_fixes"

    # --- Account -> findings (10+ rules) ---
    account_pairs = [
        (["profile_low_complete", "verified_no"], "profile_incomplete_signal", 0.88,
         "Incomplete and unverified profiles rarely win buyer trust.", "account"),
        (["profile_low_complete"], "weak_first_impression", 0.75,
         "A half-finished profile looks abandoned before buyers read your gig.", "account"),
        (["verified_no"], "trust_gap", 0.82,
         "Unverified accounts trigger caution on both Fiverr and Upwork.", "account"),
        (["pro_photo_no"], "weak_first_impression", 0.78,
         "A missing or casual photo makes buyers doubt professionalism.", "account"),
        (["level_new", "reviews_0"], "trust_gap", 0.85,
         "New sellers with zero reviews face the strongest trust barrier.", "account"),
        (["account_under_1m"], "new_account_patience", 0.80,
         "Accounts under a month rarely see steady orders yet.", "account"),
        (["profile_high_complete", "verified_yes"], "healthy_engagement_signals", 0.72,
         "A complete verified profile shows you take the platform seriously.", "account"),
        (["pro_photo_yes", "profile_high_complete"], "healthy_engagement_signals", 0.70,
         "Strong profile basics support every other gig improvement.", "account"),
        (["level_new", "account_over_1y"], "trust_gap", 0.55,
         "Long tenure without level progress suggests stalled credibility.", "account"),
        (["profile_mid_complete", "pro_photo_no"], "weak_first_impression", 0.68,
         "Average completion plus weak photo still feels unfinished.", "account"),
        (["verified_yes", "profile_high_complete", "pro_photo_yes"], "healthy_engagement_signals", 0.65,
         "Solid account hygiene is a foundation for healthy diagnosis.", "account"),
        (["account_new", "patience_low"], "impatience_risk", 0.83,
         "Brand-new accounts paired with low patience often quit too early.", "mindset"),
    ]
    for cond, then, cf, reason, cat in account_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Niche -> findings ---
    niche_pairs = [
        (["services_scattered"], "unfocused_positioning", 0.90,
         "Unrelated services split your ranking and confuse buyers.", "niche"),
        (["services_many", "role_generalist"], "unfocused_positioning", 0.85,
         "Many gigs as a generalist dilutes expert positioning.", "niche"),
        (["niche_unclear"], "unfocused_positioning", 0.88,
         "If you cannot state your niche in one line, buyers cannot either.", "niche"),
        (["demand_saturated", "level_new"], "saturated_niche_new_seller", 0.86,
         "Saturated skills are hardest for new sellers to break into.", "niche"),
        (["demand_saturated", "account_new"], "saturated_niche_new_seller", 0.84,
         "Crowded niches punish accounts without reviews.", "niche"),
        (["services_one", "niche_clear"], "healthy_engagement_signals", 0.75,
         "One clear service is the default winning pattern on Fiverr.", "niche"),
        (["keyword_theme_no", "services_many"], "overcompetition_gigs", 0.87,
         "Gigs without a shared keyword theme compete against each other.", "niche"),
        (["gigs_too_many"], "overcompetition_gigs", 0.88,
         "Seven or more live gigs split impressions and maintenance.", "niche"),
        (["role_generalist", "gigs_many"], "unfocused_positioning", 0.82,
         "Generalists with many gigs look like jacks-of-all-trades.", "niche"),
        (["trend_declining"], "poor_visibility", 0.70,
         "Declining niches naturally shrink buyer search volume.", "niche"),
        (["exp_high", "portfolio_relevant"], "strong_skills_weak_presentation", 0.65,
         "Experience without presentation still under-sells on marketplaces.", "niche"),
        (["certs_no", "exp_low", "demand_saturated"], "saturated_niche_new_seller", 0.72,
         "Low experience in saturated skills needs extra differentiation.", "niche"),
    ]
    for cond, then, cf, reason, cat in niche_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Pricing -> findings ---
    pricing_pairs = [
        (["price_much_higher", "level_new"], "price_mismatch_high", 0.90,
         "Premium pricing rarely works before social proof exists.", "pricing"),
        (["price_much_higher", "reviews_0"], "price_mismatch_high", 0.88,
         "Buyers compare unknown sellers to cheaper alternatives.", "pricing"),
        (["price_above_avg", "account_new"], "price_mismatch_high", 0.82,
         "New accounts above average price need strong proof you lack.", "pricing"),
        (["price_much_lower"], "price_mismatch_low", 0.85,
         "Extremely low prices signal desperation or low quality.", "pricing"),
        (["price_objection_yes"], "price_mismatch_high", 0.80,
         "Repeated price objections mean positioning or proof is off.", "pricing"),
        (["packages_no"], "missing_packages_signal", 0.84,
         "Without packages buyers cannot choose scope confidently.", "pricing"),
        (["price_jump_yes"], "price_mismatch_high", 0.70,
         "Huge tier jumps push buyers to simpler competitors.", "pricing"),
        (["discount_strategy_yes", "level_new"], "discount_overuse", 0.72,
         "Heavy discounting without reviews can trap you at bottom rates.", "pricing"),
        (["price_average", "reviews_5_19"], "healthy_engagement_signals", 0.68,
         "Average pricing with some reviews is a balanced position.", "pricing"),
        (["price_slightly_lower", "account_new"], "healthy_engagement_signals", 0.65,
         "Slight discounts are a common new-seller tactic.", "pricing"),
        (["extras_no", "packages_yes"], "missing_packages_signal", 0.62,
         "No extras limit upsell revenue and buyer choice.", "pricing"),
        (["price_much_lower", "reviews_20plus"], "price_mismatch_low", 0.78,
         "Experienced sellers stuck at bottom prices attract wrong clients.", "pricing"),
    ]
    for cond, then, cf, reason, cat in pricing_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- SEO -> findings ---
    seo_pairs = [
        (["title_keyword_no"], "weak_gig_seo", 0.88,
         "Titles without the main keyword miss search intent.", "seo"),
        (["title_length_bad"], "weak_gig_seo", 0.75,
         "Stuffed or tiny titles hurt click and search quality.", "seo"),
        (["tags_poor"], "weak_gig_seo", 0.82,
         "Empty or random tags waste discoverability slots.", "seo"),
        (["desc_short"], "weak_gig_seo", 0.78,
         "Short descriptions fail to answer buyer objections.", "seo"),
        (["seo_wording_bad"], "weak_gig_seo", 0.80,
         "Jargon-heavy copy does not match how buyers search.", "seo"),
        (["language_bad"], "language_quality_issue", 0.83,
         "Grammar mistakes reduce trust instantly.", "seo"),
        (["keyword_cannibal_yes"], "poor_visibility", 0.76,
         "Multiple gigs on one keyword cannibalize impressions.", "seo"),
        (["title_keyword_yes", "tags_good", "desc_long_ok"], "healthy_engagement_signals", 0.72,
         "Solid SEO basics support steady impressions.", "seo"),
        (["seo_wording_bad", "language_bad"], "weak_first_impression", 0.74,
         "Poor wording on the gig page harms first impressions.", "seo"),
        (["title_keyword_yes", "ctr_weak"], "click_attraction_weak", 0.77,
         "Good keywords with weak CTR means the hook or image fails.", "seo"),
        (["impressions_low", "title_keyword_no"], "poor_visibility", 0.84,
         "Low impressions plus weak titles is a visibility double hit.", "seo"),
        (["desc_short", "conversion_poor"], "low_conversion_signals", 0.79,
         "Thin gig copy often fails to close interested clicks.", "seo"),
    ]
    for cond, then, cf, reason, cat in seo_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Visuals -> findings ---
    visuals_pairs = [
        (["gig_image_poor"], "weak_visuals", 0.90,
         "Poor gig images are the fastest way to lose scrollers.", "visuals"),
        (["gig_image_avg", "thumbnail_weak"], "weak_visuals", 0.78,
         "Average images with weak thumbnails still underperform.", "visuals"),
        (["gig_video_no", "demand_high"], "no_video_signal", 0.72,
         "In competitive niches video helps you stand out.", "visuals"),
        (["gig_video_no", "gig_image_poor"], "weak_visuals", 0.85,
         "No video plus bad images makes gigs look neglected.", "visuals"),
        (["branding_no"], "weak_first_impression", 0.74,
         "Inconsistent branding feels amateur across multiple gigs.", "visuals"),
        (["thumbnail_weak", "impressions_avg"], "click_attraction_weak", 0.86,
         "Average visibility with weak CTR points to thumbnail/title.", "visuals"),
        (["gig_image_pro", "gig_video_yes"], "healthy_engagement_signals", 0.70,
         "Strong visuals support conversion once buyers land.", "visuals"),
        (["thumbnail_strong", "ctr_strong"], "healthy_engagement_signals", 0.68,
         "Strong CTR shows your visual hook works.", "visuals"),
        (["gig_image_poor", "ctr_weak"], "click_attraction_weak", 0.88,
         "Bad images directly crush click-through.", "visuals"),
        (["gig_video_no", "conversion_poor"], "low_conversion_signals", 0.71,
         "Video often answers buyer questions before they message you.", "visuals"),
    ]
    for cond, then, cf, reason, cat in visuals_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Portfolio -> findings ---
    portfolio_pairs = [
        (["portfolio_0"], "thin_portfolio_signal", 0.90,
         "Zero samples leave buyers guessing about quality.", "portfolio"),
        (["portfolio_1_2"], "thin_portfolio_signal", 0.78,
         "One or two samples rarely prove range for choosy buyers.", "portfolio"),
        (["portfolio_irrelevant"], "thin_portfolio_signal", 0.85,
         "Irrelevant work does not prove you can deliver this gig.", "portfolio"),
        (["case_study_no", "portfolio_3_5"], "thin_portfolio_signal", 0.62,
         "Samples without context miss storytelling power.", "portfolio"),
        (["portfolio_stale"], "trust_gap", 0.70,
         "Stale portfolio suggests you are not actively working.", "portfolio"),
        (["portfolio_6plus", "portfolio_relevant"], "healthy_engagement_signals", 0.75,
         "A rich relevant portfolio eases buyer fear.", "portfolio"),
        (["portfolio_0", "reviews_0"], "trust_gap", 0.88,
         "No reviews and no portfolio is the hardest trust sell.", "portfolio"),
        (["portfolio_relevant", "case_study_yes"], "healthy_engagement_signals", 0.72,
         "Case studies turn samples into proof.", "portfolio"),
        (["portfolio_irrelevant", "exp_high"], "strong_skills_weak_presentation", 0.80,
         "Skilled sellers with wrong samples look mismatched.", "portfolio"),
        (["portfolio_0", "account_mature"], "thin_portfolio_signal", 0.82,
         "Mature accounts still need visible proof of work.", "portfolio"),
    ]
    for cond, then, cf, reason, cat in portfolio_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Communication -> findings ---
    comm_pairs = [
        (["response_very_slow"], "slow_responsiveness", 0.92,
         "Replies over 24 hours lose most hot leads.", "communication"),
        (["response_slow"], "slow_responsiveness", 0.85,
         "Slow response hurts both ranking and buyer patience.", "communication"),
        (["response_rate_low"], "communication_gap", 0.88,
         "Ignoring messages signals you may ignore orders too.", "communication"),
        (["message_quality_bad"], "communication_gap", 0.80,
         "Sloppy messages make buyers choose clearer communicators.", "communication"),
        (["timezone_mismatch"], "wrong_market_fit", 0.75,
         "If you are asleep during buyer peak hours, you lose orders.", "communication"),
        (["delivery_late"], "order_completion_risk", 0.86,
         "Late delivery history scares new buyers away.", "communication"),
        (["response_fast", "response_rate_high"], "healthy_engagement_signals", 0.78,
         "Fast reliable replies are a hidden ranking factor.", "communication"),
        (["response_fast", "timezone_match"], "healthy_engagement_signals", 0.70,
         "Availability aligned to buyers improves close rate.", "communication"),
        (["consult_yes", "conversion_poor"], "low_conversion_signals", 0.65,
         "Consultations help but weak gig pages still block orders.", "communication"),
        (["delivery_late", "cancellations_recent"], "reputation_damage", 0.84,
         "Late work plus cancellations compound reputation hits.", "communication"),
        (["response_ok", "message_quality_good"], "healthy_engagement_signals", 0.60,
         "Adequate communication supports an otherwise OK profile.", "communication"),
        (["response_very_slow", "platform_upwork"], "slow_responsiveness", 0.88,
         "Upwork clients expect faster chat than email culture.", "communication"),
    ]
    for cond, then, cf, reason, cat in comm_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Reviews -> findings ---
    review_pairs = [
        (["reviews_0"], "trust_gap", 0.85,
         "Zero reviews is the default reason cautious buyers skip you.", "reviews"),
        (["recent_negative_yes"], "reputation_damage", 0.90,
         "Recent negatives weigh more in algorithms and buyer minds.", "reviews"),
        (["rating_very_low"], "reputation_damage", 0.92,
         "Sub-4.0 ratings sharply reduce order volume.", "reviews"),
        (["completion_low"], "order_completion_risk", 0.88,
         "Low completion rate is a public red flag.", "reviews"),
        (["cancellations_recent"], "reputation_damage", 0.85,
         "Cancellations signal instability to the platform.", "reviews"),
        (["repeat_none", "reviews_5_19"], "repeat_client_weak", 0.72,
         "Some reviews but no repeats may mean one-off buyers only.", "reviews"),
        (["testimonials_no", "reviews_1_4"], "trust_gap", 0.70,
         "Few reviews without showcased testimonials feel thin.", "reviews"),
        (["reviews_20plus", "rating_high"], "healthy_engagement_signals", 0.80,
         "Strong review volume is powerful social proof.", "reviews"),
        (["recent_negative_yes", "rating_low"], "reputation_damage", 0.88,
         "Low average plus fresh negative is especially damaging.", "reviews"),
        (["reviews_0", "price_much_higher"], "price_mismatch_high", 0.82,
         "High price without reviews rarely converts.", "reviews"),
        (["rating_high", "repeat_many"], "healthy_engagement_signals", 0.78,
         "Repeat clients prove delivery quality beyond stars.", "reviews"),
        (["completion_high", "rating_high"], "healthy_engagement_signals", 0.74,
         "Solid completion and stars signal reliability.", "reviews"),
    ]
    for cond, then, cf, reason, cat in review_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Proposals -> findings ---
    proposal_pairs = [
        (["proposal_template"], "weak_proposal_quality", 0.90,
         "Template proposals are obvious and get ignored on Upwork.", "proposals"),
        (["cover_long"], "weak_proposal_quality", 0.78,
         "Wall-of-text cover letters rarely get read fully.", "proposals"),
        (["proposals_low", "platform_upwork"], "proposal_volume_low", 0.86,
         "A handful of proposals per week is rarely enough.", "proposals"),
        (["proposals_0", "platform_upwork"], "proposal_volume_low", 0.92,
         "No proposals means no pipeline on Upwork.", "proposals"),
        (["connects_waste"], "connects_inefficiency", 0.84,
         "Burning connects without interviews wastes budget.", "proposals"),
        (["shortlist_low"], "weak_proposal_quality", 0.82,
         "Low shortlist rate means pitch or targeting is off.", "proposals"),
        (["interview_poor"], "weak_proposal_quality", 0.80,
         "Poor interview rate follows weak proposals or mismatch.", "proposals"),
        (["bid_spray"], "weak_proposal_quality", 0.83,
         "Spray-and-pray bidding lowers win rate and reputation.", "proposals"),
        (["proposal_personal", "proposals_high"], "healthy_engagement_signals", 0.75,
         "High volume tailored proposals is the Upwork growth pattern.", "proposals"),
        (["proposals_mid", "proposal_personal"], "healthy_engagement_signals", 0.68,
         "Steady personalized outreach builds pipeline.", "proposals"),
        (["platform_fiverr", "proposals_low"], "healthy_engagement_signals", 0.55,
         "Low proposal count is normal when Fiverr is primary.", "proposals"),
    ]
    for cond, then, cf, reason, cat in proposal_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Activity -> findings ---
    activity_pairs = [
        (["impressions_very_low"], "poor_visibility", 0.88,
         "Very low impressions mean search or relevance is weak.", "activity"),
        (["impressions_low", "update_stale"], "low_activity_signal", 0.82,
         "Stale gigs with low impressions need refresh.", "activity"),
        (["ctr_weak", "impressions_avg"], "click_attraction_weak", 0.85,
         "Average impressions but weak CTR is an attraction problem.", "activity"),
        (["ctr_weak", "impressions_high"], "click_attraction_weak", 0.87,
         "High impressions wasted by weak CTR is fixable without SEO.", "activity"),
        (["conversion_poor", "ctr_strong"], "low_conversion_signals", 0.88,
         "Clicks without orders mean gig page or trust fails.", "activity"),
        (["conversion_poor", "ctr_avg"], "low_conversion_signals", 0.80,
         "Average clicks but poor orders is classic conversion gap.", "activity"),
        (["update_stale", "gig_mature"], "low_activity_signal", 0.75,
         "Old gigs without updates slide in ranking.", "activity"),
        (["hours_low", "account_new"], "low_activity_signal", 0.72,
         "Few weekly hours on a new account slows all metrics.", "activity"),
        (["impressions_high", "conversion_good"], "healthy_engagement_signals", 0.82,
         "Healthy funnel from views to orders.", "activity"),
        (["gig_new", "impressions_very_low"], "new_account_patience", 0.70,
         "Brand-new gigs need time before judging visibility.", "activity"),
        (["promo_used", "conversion_poor"], "low_conversion_signals", 0.76,
         "Paid traffic with poor conversion wastes ad spend.", "activity"),
        (["routine_no", "update_stale"], "low_activity_signal", 0.78,
         "Inconsistent routine leads to neglected gigs.", "activity"),
    ]
    for cond, then, cf, reason, cat in activity_pairs:
        add(L1, cond, then, cf, reason, cat)

    # --- Mindset -> findings ---
    mindset_pairs = [
        (["patience_low", "account_new", "healthy_engagement_signals"], "impatience_risk", 0.85,
         "A decent new profile often fails from quitting too soon.", "mindset"),
        (["patience_low", "reviews_0", "gig_new"], "impatience_risk", 0.80,
         "No orders in week one is normal; impatience misreads the signal.", "mindset"),
        (["routine_yes", "hours_high"], "healthy_engagement_signals", 0.72,
         "Consistent hours correlate with eventual breakthrough.", "mindset"),
        (["patience_high", "account_new"], "new_account_patience", 0.75,
         "Patience plus new account is the correct mental model.", "mindset"),
        (["hours_low", "proposals_low", "platform_upwork"], "proposal_volume_low", 0.80,
         "Low effort on Upwork directly caps opportunities.", "mindset"),
        (["gigs_too_many", "hours_mid"], "overcompetition_gigs", 0.70,
         "Too many gigs with limited time means all look neglected.", "mindset"),
        (["profile_high_complete", "routine_yes", "reviews_5_19"], "healthy_engagement_signals", 0.78,
         "Healthy habits with growing reviews suggest staying the course.", "mindset"),
        (["patience_low", "profile_high_complete", "verified_yes"], "impatience_risk", 0.77,
         "Strong profile with unrealistic timeline creates false alarms.", "mindset"),
    ]
    for cond, then, cf, reason, cat in mindset_pairs:
        add(L1, cond, then, cf, reason, cat)

    # Extra fact->finding rules to reach 90+ on L1 (varied duplicates on themes)
    extras_l1 = [
        (["wrong_market_fit"], "wrong_market_fit", 0.70, "Placeholder", "activity"),  # skip invalid
    ]
    # Add more unique L1 rules
    more_l1 = [
        (["platform_upwork", "proposal_template"], "weak_proposal_quality", 0.86, "Upwork rewards custom pitches per job.", "proposals"),
        (["platform_fiverr", "impressions_low"], "poor_visibility", 0.65, "Fiverr sellers depend on search placement.", "activity"),
        (["services_few", "niche_clear"], "healthy_engagement_signals", 0.70, "Two related services can still be focused.", "niche"),
        (["price_average", "reviews_0"], "trust_gap", 0.72, "Fair price still needs proof without reviews.", "reviews"),
        (["gig_image_pro", "conversion_poor"], "low_conversion_signals", 0.75, "Good images cannot fix weak copy or trust.", "visuals"),
        (["level_top", "rating_high"], "healthy_engagement_signals", 0.85, "Top status with strong rating is a healthy signal.", "reviews"),
        (["exp_low", "portfolio_0"], "thin_portfolio_signal", 0.88, "Beginners must manufacture proof with samples.", "portfolio"),
        (["keyword_theme_yes", "services_few"], "healthy_engagement_signals", 0.68, "Themed related gigs reinforce SEO.", "niche"),
        (["message_quality_bad", "response_slow"], "communication_gap", 0.82, "Slow and sloppy messages double the damage.", "communication"),
        (["impressions_avg", "title_keyword_yes"], "healthy_engagement_signals", 0.60, "Average traffic with OK titles is a base to build on.", "seo"),
    ]
    for cond, then, cf, reason, cat in more_l1:
        add(L1, cond, then, cf, reason, cat)

    # --- Findings -> root causes (50+) ---
    cause_map = [
        (["unfocused_positioning"], "niche_too_broad", 0.88, "Scattered positioning reads as no clear specialty.", "niche"),
        (["overcompetition_gigs"], "too_many_unrelated_gigs", 0.86, "Too many gigs compete with each other.", "niche"),
        (["saturated_niche_new_seller"], "niche_oversaturated", 0.85, "Crowded niches punish newcomers.", "niche"),
        (["price_mismatch_high"], "price_too_high_maturity", 0.87, "Buyers expect discounts from unproven sellers.", "pricing"),
        (["price_mismatch_low"], "price_too_low_quality_signal", 0.84, "Rock-bottom rates scare quality buyers.", "pricing"),
        (["missing_packages_signal"], "weak_packages", 0.83, "Package gaps block easy purchase decisions.", "pricing"),
        (["weak_gig_seo"], "poor_gig_title_seo", 0.86, "SEO findings map to title/tag problems.", "seo"),
        (["weak_gig_seo", "language_quality_issue"], "poor_gig_title_seo", 0.80, "Language and SEO issues overlap on the gig page.", "seo"),
        (["weak_visuals", "no_video_signal"], "weak_gig_images_no_video", 0.85, "Visual gaps hurt click and trust.", "visuals"),
        (["weak_visuals"], "weak_gig_images_no_video", 0.82, "Image quality alone can block orders.", "visuals"),
        (["thin_portfolio_signal"], "thin_irrelevant_portfolio", 0.88, "Thin samples fail to prove delivery.", "portfolio"),
        (["trust_gap", "reviews_0"], "no_reviews_social_proof", 0.90, "Trust gap with no reviews is the classic blocker.", "reviews"),
        (["trust_gap"], "no_reviews_social_proof", 0.78, "General trust gap often is missing proof.", "reviews"),
        (["slow_responsiveness"], "slow_response_time", 0.90, "Slow chat directly causes lost sales.", "communication"),
        (["communication_gap", "response_rate_low"], "low_response_rate", 0.87, "Low response rate is a measurable cause.", "communication"),
        (["wrong_market_fit", "timezone_mismatch"], "wrong_target_clients", 0.82, "Timezone mismatch implies wrong market.", "communication"),
        (["wrong_market_fit"], "wrong_target_clients", 0.75, "Targeting misalignment limits orders.", "niche"),
        (["low_activity_signal"], "too_few_gigs_low_activity", 0.84, "Inactivity suppresses platform favor.", "activity"),
        (["reputation_damage"], "bad_review_cancellation_damage", 0.89, "Recent damage needs active repair.", "reviews"),
        (["click_attraction_weak"], "low_ctr_attraction", 0.86, "Weak CTR is its own diagnosable cause.", "visuals"),
        (["low_conversion_signals"], "low_conversion_orders", 0.88, "Conversion gap is distinct from visibility.", "activity"),
        (["weak_proposal_quality"], "poor_proposals", 0.90, "Proposal quality is the Upwork bottleneck.", "proposals"),
        (["proposal_volume_low"], "proposal_volume_too_low", 0.88, "Volume too low limits wins mathematically.", "proposals"),
        (["profile_incomplete_signal"], "unverified_incomplete_account", 0.86, "Incomplete setup blocks trust.", "account"),
        (["strong_skills_weak_presentation"], "thin_irrelevant_portfolio", 0.78, "Skills exist but presentation fails.", "portfolio"),
        (["healthy_engagement_signals", "account_new", "new_account_patience"], "profile_healthy_be_patient", 0.82,
         "Healthy signals on a young account mean wait and persist.", "mindset"),
        (["healthy_engagement_signals", "patience_low"], "impatience_quit_risk", 0.80, "Good profile but quitting mindset.", "mindset"),
        (["impatience_risk", "healthy_engagement_signals"], "impatience_quit_risk", 0.85, "Impatience with OK metrics is the issue.", "mindset"),
        (["language_quality_issue"], "weak_profile_description", 0.72, "Language issues often infect About sections.", "seo"),
        (["weak_first_impression"], "weak_profile_description", 0.70, "Bad first impression ties to weak copy.", "account"),
        (["discount_overuse", "price_mismatch_low"], "price_too_low_quality_signal", 0.75, "Over-discounting reinforces low-quality signal.", "pricing"),
        (["order_completion_risk"], "bad_review_cancellation_damage", 0.80, "Completion issues lead to public damage.", "reviews"),
        (["connects_inefficiency"], "poor_proposals", 0.72, "Wasted connects often mean bad targeting.", "proposals"),
        (["poor_visibility"], "poor_gig_title_seo", 0.78, "Low visibility often traces to SEO.", "seo"),
        (["repeat_client_weak", "reviews_5_19"], "profile_healthy_be_patient", 0.65, "Growing reviews may need time for repeats.", "reviews"),
        # Healthy safe case
        (["healthy_engagement_signals", "account_mature", "rating_high", "reviews_20plus"], "profile_healthy_be_patient", 0.88,
         "Mature strong profiles should keep consistency not panic.", "mindset"),
        (["healthy_engagement_signals", "reviews_5_19", "routine_yes"], "profile_healthy_be_patient", 0.75,
         "Mid-tier healthy profiles benefit from patience.", "mindset"),
        (["new_account_patience", "healthy_engagement_signals"], "profile_healthy_be_patient", 0.80,
         "New but well-built accounts need time not overhaul.", "mindset"),
        (["new_account_patience", "healthy_engagement_signals", "reviews_0"], "profile_healthy_be_patient", 0.92,
         "Zero reviews on a new but solid profile is normal, not a crisis.", "mindset"),
        (["unfocused_positioning", "services_scattered"], "niche_too_broad", 0.82, "Scattered services reinforce broad niche.", "niche"),
        (["saturated_niche_new_seller", "demand_saturated"], "niche_oversaturated", 0.80, "Saturation plus new account is tough.", "niche"),
        (["price_mismatch_high", "level_new"], "price_too_high_maturity", 0.84, "Level and price mismatch for new sellers.", "pricing"),
        (["no_video_signal", "weak_visuals"], "weak_gig_images_no_video", 0.78, "Missing video compounds weak images.", "visuals"),
        (["low_conversion_signals", "trust_gap"], "low_conversion_orders", 0.82, "Trust issues often explain conversion failure.", "reviews"),
        (["click_attraction_weak", "thumbnail_weak"], "low_ctr_attraction", 0.84, "Thumbnail weakness drives CTR diagnosis.", "visuals"),
        (["proposal_volume_low", "platform_upwork"], "proposal_volume_too_low", 0.86, "Upwork needs proposal volume.", "proposals"),
        (["overcompetition_gigs", "gigs_too_many"], "too_many_unrelated_gigs", 0.88, "Too many gigs is a structural problem.", "niche"),
        (["profile_incomplete_signal", "verified_no"], "unverified_incomplete_account", 0.84, "Verification plus completeness.", "account"),
        (["communication_gap"], "low_response_rate", 0.75, "Communication gaps affect response rate.", "communication"),
        (["timezone_mismatch"], "wrong_target_clients", 0.78, "Hours mismatch with buyers.", "communication"),
        (["weak_proposal_quality", "bid_spray"], "poor_proposals", 0.85, "Spray bidding hurts proposal quality.", "proposals"),
        (["low_activity_signal", "hours_low"], "too_few_gigs_low_activity", 0.80, "Low hours feed inactivity diagnosis.", "activity"),
        (["reputation_damage", "recent_negative_yes"], "bad_review_cancellation_damage", 0.87, "Fresh negatives need urgent care.", "reviews"),
    ]
    for cond, then, cf, reason, cat in cause_map:
        add(L2, cond, then, cf, reason, cat)

    # --- Causes -> fixes and verdicts (40+) ---
    fix_links = [
        (["niche_too_broad"], "narrow_one_core_service", 0.90, "Focus is the first fix for scattered positioning.", "niche"),
        (["niche_too_broad"], "verdict_fix_positioning", 0.88, "Positioning verdict when niche is broad.", "niche"),
        (["too_many_unrelated_gigs"], "pause_extra_gigs", 0.88, "Pause extras to concentrate ranking.", "niche"),
        (["too_many_unrelated_gigs"], "verdict_fix_positioning", 0.86, "Too many gigs triggers positioning verdict.", "niche"),
        (["niche_oversaturated"], "differentiate_saturated_niche", 0.85, "Differentiate or micro-niche in crowds.", "niche"),
        (["price_too_high_maturity"], "lower_price_temporarily", 0.87, "Temporary lower price earns first proof.", "pricing"),
        (["price_too_high_maturity"], "verdict_fix_pricing", 0.86, "Pricing verdict for high mismatch.", "pricing"),
        (["price_too_low_quality_signal"], "raise_prices_modestly", 0.84, "Modest raise signals quality.", "pricing"),
        (["price_too_low_quality_signal"], "verdict_fix_pricing", 0.82, "Low price signal needs pricing verdict.", "pricing"),
        (["weak_packages"], "add_three_tier_packages", 0.86, "Packages clarify buyer choice.", "pricing"),
        (["poor_gig_title_seo"], "rewrite_gig_title_keyword", 0.90, "Title keyword rewrite is high leverage.", "seo"),
        (["poor_gig_title_seo"], "refresh_tags_description_seo", 0.85, "Tags and description reinforce title.", "seo"),
        (["poor_gig_title_seo"], "verdict_fix_visibility", 0.84, "SEO issues map to visibility verdict.", "seo"),
        (["weak_gig_images_no_video"], "upgrade_gig_images", 0.88, "Upgrade images before or with video.", "visuals"),
        (["weak_gig_images_no_video"], "record_gig_video", 0.82, "Video builds trust on the gig page.", "visuals"),
        (["thin_irrelevant_portfolio"], "build_relevant_portfolio", 0.90, "Relevant samples prove fit.", "portfolio"),
        (["no_reviews_social_proof"], "collect_first_reviews", 0.90, "First reviews unlock trust.", "reviews"),
        (["no_reviews_social_proof"], "promo_first_five_orders", 0.75, "Small promo can speed first orders.", "reviews"),
        (["no_reviews_social_proof"], "verdict_fix_trust", 0.88, "Missing proof is a trust-first verdict.", "reviews"),
        (["slow_response_time"], "reply_within_one_hour", 0.89, "Speed replies to recover ranking.", "communication"),
        (["slow_response_time"], "verdict_fix_communication", 0.87, "Slow response triggers communication verdict.", "communication"),
        (["low_response_rate"], "improve_response_rate", 0.86, "Answer everything to lift rate.", "communication"),
        (["inconsistent_online_presence"], "schedule_online_hours", 0.80, "Scheduled hours match buyers.", "communication"),
        (["weak_profile_description"], "rewrite_profile_about", 0.82, "About section sells outcomes.", "account"),
        (["poor_proposals"], "tailored_proposals_daily", 0.90, "Daily tailored proposals are the Upwork grind.", "proposals"),
        (["wrong_target_clients"], "retarget_buyer_country", 0.80, "Align gigs to buyer geography.", "niche"),
        (["too_few_gigs_low_activity"], "weekly_gig_updates", 0.84, "Weekly updates signal alive gigs.", "activity"),
        (["bad_review_cancellation_damage"], "address_negative_review", 0.88, "Respond and fix process after negatives.", "reviews"),
        (["low_ctr_attraction"], "improve_thumbnail_title_ctr", 0.87, "CTR fixes hit thumbnail and title.", "visuals"),
        (["low_ctr_attraction"], "verdict_fix_visibility", 0.80, "CTR issues are visibility-related.", "visuals"),
        (["low_conversion_orders"], "improve_gig_page_conversion", 0.90, "Conversion fix polishes the gig page.", "activity"),
        (["low_conversion_orders"], "verdict_fix_conversion", 0.88, "Conversion verdict when clicks do not order.", "activity"),
        (["unverified_incomplete_account"], "complete_verification_profile", 0.90, "Finish basics before marketing tweaks.", "account"),
        (["proposal_volume_too_low"], "increase_proposal_volume", 0.88, "Raise weekly proposal quota.", "proposals"),
        (["profile_healthy_be_patient"], "stay_consistent_30_days", 0.85, "Stay consistent instead of churning fixes.", "mindset"),
        (["profile_healthy_be_patient"], "verdict_healthy_patient", 0.90, "Healthy profile gets patience verdict.", "mindset"),
        (["impatience_quit_risk"], "stay_consistent_30_days", 0.82, "Consistency beats panic changes.", "mindset"),
        (["impatience_quit_risk"], "manage_expectations_timeline", 0.80, "Realistic timelines reduce harmful churn.", "mindset"),
        (["impatience_quit_risk"], "verdict_healthy_patient", 0.85, "Impatience on OK profile: be patient.", "mindset"),
        (["niche_oversaturated"], "verdict_fix_positioning", 0.78, "Saturation needs positioning angle.", "niche"),
        (["weak_packages"], "verdict_fix_conversion", 0.72, "Packages help close buyers.", "pricing"),
        (["thin_irrelevant_portfolio"], "verdict_fix_trust", 0.80, "Portfolio fixes trust.", "portfolio"),
        (["bad_review_cancellation_damage"], "verdict_fix_trust", 0.82, "Reputation repair is trust work.", "reviews"),
        (["poor_proposals"], "verdict_fix_communication", 0.75, "Proposals are client communication.", "proposals"),
        (["slow_response_time", "low_response_rate"], "verdict_fix_communication", 0.84, "Combined comm issues.", "communication"),
        (["price_too_high_maturity", "no_reviews_social_proof"], "lower_price_temporarily", 0.86, "Price and proof fix together.", "pricing"),
        (["low_conversion_orders", "no_reviews_social_proof"], "collect_first_reviews", 0.82, "Reviews help conversion.", "reviews"),
    ]
    for cond, then, cf, reason, cat in fix_links:
        add(L3, cond, then, cf, reason, cat)

    return rules


RULES: list[dict] = _build_rules()
