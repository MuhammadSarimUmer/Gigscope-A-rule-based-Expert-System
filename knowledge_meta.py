"""
Names, descriptions, and DSS metadata for findings, root causes, fixes, and verdicts.
"""

from __future__ import annotations

# Layer 2: Findings (patterns in facts)
FINDINGS: dict[str, dict] = {
    "weak_first_impression": {
        "name": "Weak first impression",
        "description": "Profile or gig does not look professional at first glance.",
    },
    "poor_visibility": {
        "name": "Poor visibility",
        "description": "Few impressions or poor search placement signals.",
    },
    "trust_gap": {
        "name": "Trust gap",
        "description": "Buyer has little reason to trust a new or thin profile.",
    },
    "price_mismatch_high": {
        "name": "Price above buyer expectations",
        "description": "Pricing looks high for account maturity or niche.",
    },
    "price_mismatch_low": {
        "name": "Price signals low quality",
        "description": "Pricing is so low it may scare quality-seeking buyers.",
    },
    "unfocused_positioning": {
        "name": "Unfocused positioning",
        "description": "Too many unrelated services dilute expertise.",
    },
    "slow_responsiveness": {
        "name": "Slow responsiveness",
        "description": "Replies or delivery signals are slower than competitors.",
    },
    "low_conversion_signals": {
        "name": "Low conversion signals",
        "description": "Clicks or views exist but orders do not follow.",
    },
    "weak_proposal_quality": {
        "name": "Weak proposal quality",
        "description": "Proposals look generic or misaligned with jobs.",
    },
    "thin_portfolio_signal": {
        "name": "Thin portfolio",
        "description": "Few or irrelevant samples weaken credibility.",
    },
    "weak_gig_seo": {
        "name": "Weak gig SEO",
        "description": "Titles, tags, or descriptions hurt discoverability.",
    },
    "weak_visuals": {
        "name": "Weak visuals",
        "description": "Images or branding do not stand out.",
    },
    "reputation_damage": {
        "name": "Reputation damage",
        "description": "Recent negatives hurt ranking and trust.",
    },
    "low_activity_signal": {
        "name": "Low activity",
        "description": "Stale gigs or little weekly effort.",
    },
    "wrong_market_fit": {
        "name": "Wrong market fit",
        "description": "Targeting or timezone does not match buyers.",
    },
    "saturated_niche_new_seller": {
        "name": "Saturated niche for newcomer",
        "description": "Crowded skill area with weak differentiation.",
    },
    "missing_packages_signal": {
        "name": "Missing package structure",
        "description": "No clear tiers or upsells for buyers.",
    },
    "communication_gap": {
        "name": "Communication gap",
        "description": "Messages or availability discourage buyers.",
    },
    "healthy_engagement_signals": {
        "name": "Healthy engagement",
        "description": "Metrics and habits look reasonable for account age.",
    },
    "new_account_patience": {
        "name": "New account patience needed",
        "description": "Profile is improving but needs time to mature.",
    },
    "strong_skills_weak_presentation": {
        "name": "Strong skills, weak presentation",
        "description": "Ability is there but packaging undersells it.",
    },
    "click_attraction_weak": {
        "name": "Weak click attraction",
        "description": "Impressions OK but click-through is poor.",
    },
    "order_completion_risk": {
        "name": "Order completion risk",
        "description": "Cancellations or completion rate worry buyers.",
    },
    "profile_incomplete_signal": {
        "name": "Incomplete profile",
        "description": "Missing basics on profile or verification.",
    },
    "impatience_risk": {
        "name": "Impatience risk",
        "description": "User may quit before profile has fair chance.",
    },
    "overcompetition_gigs": {
        "name": "Too many live gigs",
        "description": "Many unrelated gigs split focus and SEO.",
    },
    "proposal_volume_low": {
        "name": "Low proposal volume",
        "description": "Not enough outreach on proposal platforms.",
    },
    "connects_inefficiency": {
        "name": "Inefficient connects use",
        "description": "Connects spent without interviews or wins.",
    },
    "language_quality_issue": {
        "name": "Language quality issue",
        "description": "Grammar or clarity hurts professional image.",
    },
    "no_video_signal": {
        "name": "No gig video",
        "description": "Missing video where competitors use it.",
    },
    "discount_overuse": {
        "name": "Discount overuse",
        "description": "Heavy discounting without strategy.",
    },
    "repeat_client_weak": {
        "name": "Weak repeat business",
        "description": "Few returning clients for experience shown.",
    },
}

# Layer 3: Root causes (diagnosis)
ROOT_CAUSES: dict[str, dict] = {
    "niche_too_broad": {
        "name": "Niche too broad or unfocused",
        "description": "Buyers cannot tell your specialty quickly.",
    },
    "niche_oversaturated": {
        "name": "Niche oversaturated for a new seller",
        "description": "Hard to rank among established sellers.",
    },
    "price_too_high_maturity": {
        "name": "Price too high for account maturity",
        "description": "New or unproven accounts rarely win at premium prices.",
    },
    "price_too_low_quality_signal": {
        "name": "Price too low (quality signal)",
        "description": "Rock-bottom prices attract only bargain hunters.",
    },
    "weak_packages": {
        "name": "Weak or missing packages",
        "description": "Buyers lack clear options and upsells.",
    },
    "poor_gig_title_seo": {
        "name": "Poor gig title and keywords",
        "description": "Search and browse traffic misses your gig.",
    },
    "weak_gig_images_no_video": {
        "name": "Weak gig images or no video",
        "description": "Visuals fail to stop the scroll.",
    },
    "thin_irrelevant_portfolio": {
        "name": "Thin or irrelevant portfolio",
        "description": "Samples do not prove fit for target gigs.",
    },
    "no_reviews_social_proof": {
        "name": "No reviews / weak social proof",
        "description": "Buyers choose safer profiles with history.",
    },
    "slow_response_time": {
        "name": "Slow response time",
        "description": "Late replies hurt ranking and buyer confidence.",
    },
    "low_response_rate": {
        "name": "Low response rate",
        "description": "Ignored messages signal unreliability.",
    },
    "inconsistent_online_presence": {
        "name": "Inconsistent online presence",
        "description": "Odd hours or gaps lose hot leads.",
    },
    "weak_profile_description": {
        "name": "Weak profile description",
        "description": "About section does not sell outcomes.",
    },
    "poor_proposals": {
        "name": "Poor proposals",
        "description": "Copy-paste or unfocused pitches get skipped.",
    },
    "wrong_target_clients": {
        "name": "Wrong target clients or region",
        "description": "Offers do not match where buyers search.",
    },
    "too_few_gigs_low_activity": {
        "name": "Too few gigs or low activity",
        "description": "Platform sees little ongoing effort.",
    },
    "bad_review_cancellation_damage": {
        "name": "Recent bad review / cancellation damage",
        "description": "Recent negatives suppress visibility.",
    },
    "low_ctr_attraction": {
        "name": "Low click-through (attraction)",
        "description": "You show in search but thumbnails/titles lose clicks.",
    },
    "low_conversion_orders": {
        "name": "Low conversion (clicks, no orders)",
        "description": "Gig page does not close interested buyers.",
    },
    "profile_healthy_be_patient": {
        "name": "Profile healthy — needs time",
        "description": "No major fix; consistency and patience matter.",
    },
    "impatience_quit_risk": {
        "name": "Impatience — profile OK",
        "description": "Fundamentals fine; unrealistic timeline is the issue.",
    },
    "unverified_incomplete_account": {
        "name": "Unverified or incomplete account",
        "description": "Basics block trust and sometimes eligibility.",
    },
    "proposal_volume_too_low": {
        "name": "Proposal volume too low",
        "description": "Not enough shots on goal for Upwork-style work.",
    },
    "too_many_unrelated_gigs": {
        "name": "Too many unrelated gigs",
        "description": "Split focus hurts each gig's ranking.",
    },
}

# Layer 4: Fixes (actions) — DSS metadata: impact, effort, cost, days
FIXES: dict[str, dict] = {
    "narrow_one_core_service": {
        "name": "Narrow to one core service",
        "description": "Pick one profitable niche and pause unrelated gigs.",
        "impact": 9,
        "effort": 6,
        "cost": 1,
        "days_to_results": 21,
        "root_cause": "niche_too_broad",
    },
    "differentiate_saturated_niche": {
        "name": "Differentiate in a saturated niche",
        "description": "Add a micro-niche, case study, or unique deliverable.",
        "impact": 8,
        "effort": 7,
        "cost": 2,
        "days_to_results": 30,
        "root_cause": "niche_oversaturated",
    },
    "lower_price_temporarily": {
        "name": "Lower price temporarily for first orders",
        "description": "Strategic starter pricing until reviews arrive.",
        "impact": 7,
        "effort": 3,
        "cost": 1,
        "days_to_results": 14,
        "root_cause": "price_too_high_maturity",
    },
    "raise_prices_modestly": {
        "name": "Raise prices to credible range",
        "description": "Move off race-to-bottom without jumping too high.",
        "impact": 7,
        "effort": 2,
        "cost": 0,
        "days_to_results": 21,
        "root_cause": "price_too_low_quality_signal",
    },
    "add_three_tier_packages": {
        "name": "Add three-tier packages",
        "description": "Basic, standard, premium with clear scope.",
        "impact": 8,
        "effort": 5,
        "cost": 0,
        "days_to_results": 14,
        "root_cause": "weak_packages",
    },
    "rewrite_gig_title_keyword": {
        "name": "Rewrite gig title around one keyword",
        "description": "Lead with buyer search terms in title.",
        "impact": 9,
        "effort": 4,
        "cost": 0,
        "days_to_results": 10,
        "root_cause": "poor_gig_title_seo",
    },
    "refresh_tags_description_seo": {
        "name": "Refresh tags and description SEO",
        "description": "Align tags and first paragraph with target queries.",
        "impact": 8,
        "effort": 5,
        "cost": 0,
        "days_to_results": 14,
        "root_cause": "poor_gig_title_seo",
    },
    "upgrade_gig_images": {
        "name": "Upgrade gig images / thumbnail",
        "description": "Professional cover image with clear outcome text.",
        "impact": 8,
        "effort": 6,
        "cost": 3,
        "days_to_results": 7,
        "root_cause": "weak_gig_images_no_video",
    },
    "record_gig_video": {
        "name": "Record a short gig video",
        "description": "60–90 second intro showing process and results.",
        "impact": 7,
        "effort": 7,
        "cost": 2,
        "days_to_results": 14,
        "root_cause": "weak_gig_images_no_video",
    },
    "build_relevant_portfolio": {
        "name": "Add three relevant portfolio samples",
        "description": "Samples matching exact gigs you sell.",
        "impact": 9,
        "effort": 8,
        "cost": 2,
        "days_to_results": 21,
        "root_cause": "thin_irrelevant_portfolio",
    },
    "collect_first_reviews": {
        "name": "Collect first reviews ethically",
        "description": "Smaller scoped orders with known contacts or beta clients.",
        "impact": 9,
        "effort": 7,
        "cost": 2,
        "days_to_results": 30,
        "root_cause": "no_reviews_social_proof",
    },
    "reply_within_one_hour": {
        "name": "Reply within one hour for 30 days",
        "description": "Mobile notifications and fixed response windows.",
        "impact": 8,
        "effort": 6,
        "cost": 0,
        "days_to_results": 14,
        "root_cause": "slow_response_time",
    },
    "improve_response_rate": {
        "name": "Improve response rate to 95%+",
        "description": "Answer every buyer message, even to decline politely.",
        "impact": 7,
        "effort": 5,
        "cost": 0,
        "days_to_results": 10,
        "root_cause": "low_response_rate",
    },
    "schedule_online_hours": {
        "name": "Schedule consistent online hours",
        "description": "Match peak buyer time zones.",
        "impact": 6,
        "effort": 4,
        "cost": 0,
        "days_to_results": 21,
        "root_cause": "inconsistent_online_presence",
    },
    "rewrite_profile_about": {
        "name": "Rewrite profile About section",
        "description": "Outcome-focused story with niche proof.",
        "impact": 7,
        "effort": 4,
        "cost": 0,
        "days_to_results": 14,
        "root_cause": "weak_profile_description",
    },
    "tailored_proposals_daily": {
        "name": "Send 10 tailored proposals per day",
        "description": "Custom first lines tied to each job post.",
        "impact": 9,
        "effort": 9,
        "cost": 4,
        "days_to_results": 21,
        "root_cause": "poor_proposals",
    },
    "retarget_buyer_country": {
        "name": "Retarget primary buyer country",
        "description": "Adjust gigs and hours for where demand is.",
        "impact": 7,
        "effort": 5,
        "cost": 1,
        "days_to_results": 21,
        "root_cause": "wrong_target_clients",
    },
    "weekly_gig_updates": {
        "name": "Weekly gig updates and activity",
        "description": "Refresh gallery, FAQ, or offer each week.",
        "impact": 6,
        "effort": 4,
        "cost": 0,
        "days_to_results": 21,
        "root_cause": "too_few_gigs_low_activity",
    },
    "address_negative_review": {
        "name": "Address recent negative review",
        "description": "Professional public reply plus process fix.",
        "impact": 7,
        "effort": 5,
        "cost": 0,
        "days_to_results": 30,
        "root_cause": "bad_review_cancellation_damage",
    },
    "improve_thumbnail_title_ctr": {
        "name": "Improve thumbnail and title for CTR",
        "description": "A/B style tests on image and title hook.",
        "impact": 8,
        "effort": 5,
        "cost": 1,
        "days_to_results": 14,
        "root_cause": "low_ctr_attraction",
    },
    "improve_gig_page_conversion": {
        "name": "Improve gig page conversion",
        "description": "FAQ, packages, and samples answer objections.",
        "impact": 9,
        "effort": 6,
        "cost": 0,
        "days_to_results": 14,
        "root_cause": "low_conversion_orders",
    },
    "complete_verification_profile": {
        "name": "Complete verification and profile",
        "description": "Finish all mandatory profile and ID steps.",
        "impact": 8,
        "effort": 3,
        "cost": 0,
        "days_to_results": 3,
        "root_cause": "unverified_incomplete_account",
    },
    "increase_proposal_volume": {
        "name": "Increase weekly proposal volume",
        "description": "Set a weekly quota with quality checklist.",
        "impact": 8,
        "effort": 8,
        "cost": 3,
        "days_to_results": 21,
        "root_cause": "proposal_volume_too_low",
    },
    "pause_extra_gigs": {
        "name": "Pause unrelated gigs",
        "description": "Keep only gigs that share one keyword theme.",
        "impact": 8,
        "effort": 4,
        "cost": 0,
        "days_to_results": 14,
        "root_cause": "too_many_unrelated_gigs",
    },
    "stay_consistent_30_days": {
        "name": "Stay consistent 30 more days",
        "description": "Maintain effort without major changes.",
        "impact": 6,
        "effort": 5,
        "cost": 0,
        "days_to_results": 30,
        "root_cause": "profile_healthy_be_patient",
    },
    "manage_expectations_timeline": {
        "name": "Reset timeline expectations",
        "description": "Set a 60–90 day goal instead of weekly panic changes.",
        "impact": 5,
        "effort": 2,
        "cost": 0,
        "days_to_results": 30,
        "root_cause": "impatience_quit_risk",
    },
    "promo_first_five_orders": {
        "name": "Run promo for first five orders",
        "description": "Limited discount with clear scope boundaries.",
        "impact": 6,
        "effort": 3,
        "cost": 2,
        "days_to_results": 21,
        "root_cause": "no_reviews_social_proof",
    },
}

VERDICTS: dict[str, dict] = {
    "verdict_fix_positioning": {
        "name": "Fix positioning first",
        "description": "Clarify niche and gig focus before other tweaks.",
        "detail": (
            "Buyers and search algorithms need a single clear story about what you sell. "
            "When services are scattered or gigs compete with each other, pricing and SEO fixes "
            "rarely stick. Narrow focus first, then polish individual gigs."
        ),
        "focus_areas": ["One core niche", "Pause unrelated gigs", "Shared keyword theme"],
        "next_steps": [
            "List every live gig and mark which share one buyer outcome.",
            "Pick one core service to keep; pause or merge the rest.",
            "Rewrite titles so each active gig targets a distinct sub-keyword.",
        ],
    },
    "verdict_fix_trust": {
        "name": "Fix trust and social proof first",
        "description": "Reviews, portfolio, and profile completeness come first.",
        "detail": (
            "Visitors compare you to sellers with reviews and proof. Without samples, stars, "
            "or a complete profile, even perfect SEO gets clicks that bounce. Build believable "
            "proof before spending on ads or heavy discounts."
        ),
        "focus_areas": ["Portfolio relevance", "First reviews", "Profile completeness"],
        "next_steps": [
            "Add three samples that match your main gig exactly.",
            "Complete verification and fill every profile section.",
            "Offer a tightly scoped starter order to earn the first public review.",
        ],
    },
    "verdict_fix_visibility": {
        "name": "Fix visibility first",
        "description": "SEO, tags, and impressions need attention.",
        "detail": (
            "If buyers rarely see your gig, conversion work cannot help yet. Weak titles, tags, "
            "or stale listings reduce impressions. Fix discoverability so the right buyers can "
            "find you in search and categories."
        ),
        "focus_areas": ["Title keywords", "Tags and description", "Gig freshness"],
        "next_steps": [
            "Put one primary buyer keyword in the gig title.",
            "Refresh all tag slots using buyer language.",
            "Update gallery or FAQ this week to signal an active gig.",
        ],
    },
    "verdict_fix_conversion": {
        "name": "Fix conversion first",
        "description": "You get interest but the gig page does not close.",
        "detail": (
            "Traffic is arriving but not ordering. That usually means the gig page, packages, or "
            "visuals do not answer buyer doubts fast enough. Improve clarity and trust on the "
            "page before chasing more impressions."
        ),
        "focus_areas": ["Gig page copy", "Packages and FAQ", "Images or video"],
        "next_steps": [
            "Add three packages with clear scope boundaries.",
            "Lead the description with outcomes, not features.",
            "Upgrade thumbnail and add a short intro video if missing.",
        ],
    },
    "verdict_fix_communication": {
        "name": "Fix communication first",
        "description": "Speed and reliability of replies are the bottleneck.",
        "detail": (
            "Marketplaces reward fast, professional responses. Slow replies or generic proposals "
            "lose buyers who message multiple sellers. Tighten response habits before changing "
            "price or niche."
        ),
        "focus_areas": ["Response time", "Proposal quality", "Online hours"],
        "next_steps": [
            "Turn on mobile alerts and reply within one hour for 30 days.",
            "Use a short template with one personalized line per buyer.",
            "Block online hours that overlap your main buyer timezone.",
        ],
    },
    "verdict_fix_pricing": {
        "name": "Fix pricing first",
        "description": "Price does not match buyer expectations.",
        "detail": (
            "Your price signal does not match account maturity or niche norms. Too high scares "
            "buyers without reviews; too low signals low quality. Align pricing with proof "
            "you already have (or earn proof with a deliberate starter offer)."
        ),
        "focus_areas": ["Market comparison", "Package tiers", "Starter strategy"],
        "next_steps": [
            "Check three competitors at your level and note their basic package price.",
            "Adjust one tier to sit slightly below market until you have five reviews.",
            "If underpriced, raise the basic package modestly and improve copy to match.",
        ],
    },
    "verdict_healthy_patient": {
        "name": "Profile looks healthy: be patient",
        "description": "Keep consistent effort; no urgent structural fix.",
        "detail": (
            "No single issue crossed the threshold for an emergency overhaul. Metrics and habits "
            "look reasonable for your account age. Frequent pivots often hurt more than help. "
            "Keep a steady weekly routine and measure over the next 30–60 days."
        ),
        "focus_areas": ["Consistency", "Light weekly updates", "Realistic timeline"],
        "next_steps": [
            "Ship one small gig refresh per week (FAQ, image, or sample).",
            "Track impressions and messages weekly instead of daily.",
            "Avoid rewriting niche or prices unless numbers drop for a full month.",
        ],
    },
}

# Categories for rules (each needs >= 10 rules)
RULE_CATEGORIES = [
    "account",
    "niche",
    "pricing",
    "seo",
    "visuals",
    "portfolio",
    "communication",
    "reviews",
    "proposals",
    "activity",
    "mindset",
]

ALL_CONCLUSIONS = set(FINDINGS) | set(ROOT_CAUSES) | set(FIXES) | set(VERDICTS)
