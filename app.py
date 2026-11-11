"""
GigScope — Streamlit UI for freelance order diagnosis expert system.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from dss import DEFAULT_WEIGHTS, analyze_answers, what_if_compare
from knowledge_meta import ROOT_CAUSES
from explain import explain_fix_chain, explain_root_causes
from facts import FACT_DEFINITIONS, answers_to_facts, definitions_by_category
from rules import RULES
from scenarios import SCENARIOS
from tree import build_case_tree, legend_markdown

ASSETS = Path(__file__).resolve().parent / "assets"

st.set_page_config(page_title="GigScope", page_icon="🔍", layout="wide")


@st.cache_data
def cached_rules_table():
    rows = []
    for r in RULES:
        rows.append(
            {
                "id": r["id"],
                "layer": r["layer"],
                "category": r["category"],
                "if": ", ".join(str(c) for c in r["if"]),
                "then": r["then"],
                "cf": r["cf"],
                "reason": r["reason"],
            }
        )
    return pd.DataFrame(rows)


def _init_state():
    if "answers" not in st.session_state:
        from facts import default_answers

        st.session_state.answers = default_answers()
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "weights" not in st.session_state:
        st.session_state.weights = dict(DEFAULT_WEIGHTS)
    if "whatif_answers" not in st.session_state:
        st.session_state.whatif_answers = None


def _render_question(qdef):
    qid = qdef["id"]
    label = f"{qdef['question']} ({qid})"
    if qdef["type"] == "yesno":
        st.session_state.answers[qid] = st.checkbox(label, value=st.session_state.answers.get(qid, False))
    else:
        opts = qdef["options"]
        idx = opts.index(st.session_state.answers[qid]) if st.session_state.answers.get(qid) in opts else 0
        st.session_state.answers[qid] = st.selectbox(label, opts, index=idx)


def _run_analysis():
    st.session_state.analysis = analyze_answers(st.session_state.answers, st.session_state.weights)


def _progress_row(label: str, value: float, scale: float = 1.0, caption: str = "") -> None:
    """Label + numeric hint + Streamlit progress bar (value scaled to 0–1)."""
    ratio = min(max(value / scale, 0.0), 1.0)
    left, right = st.columns([4, 1])
    left.markdown(f"**{label}**")
    if scale <= 1.0:
        right.markdown(f"{value * 100:.0f}%")
    else:
        right.markdown(f"{value:.1f}/{scale:.0f}")
    if caption:
        left.caption(caption)
    st.progress(ratio)


def _render_verdict_panel(decision: dict) -> None:
    vd = decision["verdict_detail"]
    st.markdown(f"### {vd['title']}")
    st.markdown(vd["detail_markdown"])
    st.markdown("**Verdict strength** (how firmly the rules support this outcome)")
    _progress_row("Confidence", vd["confidence"], 1.0, "Combined certainty from fired rules")

    if vd["focus_areas"]:
        st.markdown("**Focus areas**")
        for area in vd["focus_areas"]:
            st.markdown(f"- {area}")

    if vd["next_steps"]:
        st.markdown("**Recommended next steps**")
        for i, step in enumerate(vd["next_steps"], start=1):
            st.markdown(f"{i}. {step}")

    if vd["supporting_causes"]:
        st.markdown("**Supporting diagnoses**")
        for c in vd["supporting_causes"]:
            _progress_row(
                c["name"],
                c["confidence"],
                1.0,
                c.get("description", ""),
            )


def _render_top_action_card(top_action: dict | None, max_score: float) -> None:
    if not top_action:
        st.info("No fix cleared the confidence threshold yet.")
        return
    st.markdown(f"### Top action: {top_action['name']}")
    st.caption(f"Solves: **{top_action['root_cause_name']}**")
    _progress_row("Priority score", top_action["score"], max(max_score, 1.0), "DSS weighted rank")
    st.markdown("**Action profile**")
    cols = st.columns(2)
    with cols[0]:
        _progress_row("Impact", top_action["impact"], 10.0, "Higher = more order potential")
        _progress_row("Ease", 10 - top_action["effort"], 10.0, "Higher = easier to execute")
    with cols[1]:
        _progress_row("Low cost", 10 - top_action["cost"], 10.0, "Higher = cheaper")
        _progress_row("Root-cause confidence", top_action["confidence"], 1.0)
    st.caption(f"Typical time to see results: **{top_action['days_to_results']} days**")


def main():
    _init_state()

    st.title("GigScope")
    st.caption("Rule-based expert system: diagnose why freelance orders are slow and rank fixes.")

    tabs = st.tabs(
        [
            "Diagnose",
            "Results",
            "Fix Ranking (DSS)",
            "What-If",
            "Reasoning Tree",
            "Knowledge Base",
            "About / Viva",
        ]
    )

    # --- Diagnose ---
    with tabs[0]:
        col1, col2 = st.columns([2, 1])
        with col2:
            scenario_names = {k: v["name"] for k, v in SCENARIOS.items()}
            pick = st.selectbox("Load demo scenario", ["—"] + list(scenario_names.keys()), format_func=lambda k: scenario_names.get(k, k))
            if st.button("Load scenario") and pick != "—":
                st.session_state.answers = dict(SCENARIOS[pick]["answers"])
                st.session_state.analysis = None
            st.info(f"Questionnaire facts: {len(FACT_DEFINITIONS)}")
        with col1:
            for cat, items in definitions_by_category().items():
                with st.expander(cat.title(), expanded=cat == "account"):
                    for q in items:
                        _render_question(q)
        if st.button("Analyze", type="primary"):
            missing = [f["id"] for f in FACT_DEFINITIONS if f["id"] not in st.session_state.answers]
            if missing:
                st.warning(f"Some answers missing; using defaults.")
            _run_analysis()
            st.success("Analysis complete — open Results tab.")

    # --- Results ---
    with tabs[1]:
        if not st.session_state.analysis:
            st.warning("Run **Analyze** on the Diagnose tab first.")
        else:
            d = st.session_state.analysis["decision"]
            col_verdict, col_action = st.columns([3, 2])
            with col_verdict:
                st.subheader("Decision")
                with st.container(border=True):
                    _render_verdict_panel(d)
            with col_action:
                st.subheader("What to do first")
                max_score = d["ranked_fixes"][0]["score"] if d["ranked_fixes"] else 10.0
                with st.container(border=True):
                    _render_top_action_card(d["top_action"], max_score)
            st.info(d["statement"])

            st.subheader("All root causes")
            shown = [c for c in d["root_causes"] if c["confidence"] >= 0.05][:12]
            for c in shown:
                desc = ROOT_CAUSES.get(c["id"], {}).get("description", "")
                _progress_row(c["name"], c["confidence"], 1.0, desc)

            with st.expander("Full explanations (rule-backed)"):
                fired = st.session_state.analysis["engine"]["fired_rules"]
                for ex in explain_root_causes(fired, st.session_state.analysis["engine"]["memory"])[:8]:
                    st.write(ex["text"])

    # --- DSS ---
    with tabs[2]:
        if not st.session_state.analysis:
            st.warning("Run analysis first.")
        else:
            st.subheader("Adjust DSS weights")
            w = st.session_state.weights
            w["w_impact"] = st.slider("Impact weight", 0.0, 1.0, w["w_impact"])
            w["w_effort"] = st.slider("Ease (inverse effort) weight", 0.0, 1.0, w["w_effort"])
            w["w_cost"] = st.slider("Low cost weight", 0.0, 1.0, w["w_cost"])
            w["w_conf"] = st.slider("Confidence weight", 0.0, 1.0, w["w_conf"])
            st.session_state.analysis = analyze_answers(st.session_state.answers, w)
            ranked = st.session_state.analysis["decision"]["ranked_fixes"]
            vd = st.session_state.analysis["decision"]["verdict_detail"]
            with st.container(border=True):
                st.markdown(f"**Current verdict:** {vd['title']}")
                _progress_row("Verdict confidence", vd["confidence"])
            if ranked:
                max_score = ranked[0]["score"]
                st.subheader("Ranked fixes")
                for row in ranked[:10]:
                    with st.expander(f"#{row['rank']} — {row['name']} (score {row['score']:.2f})", expanded=row["rank"] == 1):
                        _progress_row("Overall priority", row["score"], max(max_score, 0.01))
                        c1, c2 = st.columns(2)
                        with c1:
                            _progress_row("Impact", row["impact"], 10.0)
                            _progress_row("Ease", 10 - row["effort"], 10.0)
                        with c2:
                            _progress_row("Low cost", 10 - row["cost"], 10.0)
                            _progress_row("Cause confidence", row["confidence"], 1.0)
                df = pd.DataFrame(ranked)
                st.dataframe(df, use_container_width=True)
            plan = st.session_state.analysis["action_plan"]
            c1, c2, c3 = st.columns(3)
            c1.write("**7 days**")
            c1.write("\n".join(f"- {x}" for x in plan["7_days"]) or "—")
            c2.write("**14 days**")
            c2.write("\n".join(f"- {x}" for x in plan["14_days"]) or "—")
            c3.write("**30 days**")
            c3.write("\n".join(f"- {x}" for x in plan["30_days"]) or "—")

    # --- What-if ---
    with tabs[3]:
        st.write("Change one or more answers and compare diagnosis.")
        if st.session_state.whatif_answers is None:
            st.session_state.whatif_answers = dict(st.session_state.answers)
        changed = {}
        options = {f["id"]: f for f in FACT_DEFINITIONS[:20]}
        st.caption("Quick edit (first 20 questions); use Diagnose tab for full form.")
        for qid, qdef in options.items():
            if qdef["type"] == "yesno":
                changed[qid] = st.checkbox(qdef["question"], st.session_state.whatif_answers.get(qid, False), key=f"wi_{qid}")
            else:
                changed[qid] = st.selectbox(
                    qdef["question"],
                    qdef["options"],
                    index=qdef["options"].index(st.session_state.whatif_answers.get(qid, qdef["options"][0])),
                    key=f"wi_{qid}",
                )
        wi_answers = dict(st.session_state.answers)
        wi_answers.update(changed)
        if st.button("Run what-if"):
            if st.session_state.analysis:
                cmp = what_if_compare(st.session_state.answers, wi_answers, st.session_state.weights)
                bvd = cmp["before"]["decision"]["verdict_detail"]
                avd = cmp["after"]["decision"]["verdict_detail"]
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### Before")
                    with st.container(border=True):
                        st.markdown(f"**{bvd['title']}**")
                        _progress_row("Confidence", bvd["confidence"])
                        st.caption(bvd["summary"])
                with c2:
                    st.markdown("#### After")
                    with st.container(border=True):
                        st.markdown(f"**{avd['title']}**")
                        _progress_row("Confidence", avd["confidence"])
                        st.caption(avd["summary"])
                st.markdown(
                    f"**Top action:** {cmp['top_action_before']} → **{cmp['top_action_after']}**"
                )
                st.markdown("**Largest diagnosis shifts**")
                for ch in cmp["cause_changes"][:8]:
                    if abs(ch["delta"]) < 0.02:
                        continue
                    st.markdown(f"**{ch['name']}**")
                    bc, ac = st.columns(2)
                    with bc:
                        st.caption("Before")
                        _progress_row("Confidence", ch["before"])
                    with ac:
                        st.caption("After")
                        _progress_row("Confidence", ch["after"])
            else:
                st.warning("Run baseline analysis first.")

    # --- Reasoning tree ---
    with tabs[4]:
        if not st.session_state.analysis:
            st.warning("Run analysis first.")
        else:
            mem = st.session_state.analysis["engine"]["memory"]
            fired = st.session_state.analysis["engine"]["fired_rules"]
            top_fix = st.session_state.analysis["decision"]["top_action"]
            hf = top_fix["fix_id"] if top_fix else None
            dot = build_case_tree(fired, mem, hf)
            st.graphviz_chart(dot)
            st.markdown(legend_markdown())
            st.download_button("Download DOT", dot, file_name="case_tree.dot")
            png_path = ASSETS / "kb_full.png"
            if png_path.exists():
                st.image(str(png_path), caption="Pre-generated full KB (assets/)")
            with st.expander("Why? — fired rules"):
                for fr in fired:
                    rule = fr["rule"]
                    st.markdown(f"**{fr['id']}** (cf {rule['cf']}) — {rule['reason']}")
            if hf:
                st.write(explain_fix_chain(fired, hf))

    # --- Knowledge base ---
    with tabs[5]:
        st.metric("Total rules", len(RULES))
        df = cached_rules_table()
        fcat = st.multiselect("Filter category", sorted(df["category"].unique()))
        flayer = st.multiselect("Filter layer", sorted(df["layer"].unique()))
        search = st.text_input("Search id / conclusion / reason")
        view = df.copy()
        if fcat:
            view = view[view["category"].isin(fcat)]
        if flayer:
            view = view[view["layer"].isin(flayer)]
        if search:
            mask = (
                view["id"].str.contains(search, case=False)
                | view["then"].str.contains(search, case=False)
                | view["reason"].str.contains(search, case=False)
            )
            view = view[mask]
        st.dataframe(view, use_container_width=True, height=400)
        for img in sorted(ASSETS.glob("kb_*.png"))[:6]:
            st.image(str(img), caption=img.name)

    # --- About ---
    with tabs[6]:
        st.header("Why this is an Expert System")
        st.markdown(
            """
- **Knowledge base:** IF-THEN rules live in `rules.py`, not buried in UI code.
- **Inference engine:** `engine.py` applies rules with forward chaining; it knows nothing about freelancing.
- **Separation:** Change rules → behaviour changes without editing the engine.
- **Working memory:** Your answers plus every derived conclusion and certainty.
- **Explanation facility:** Fired rules and the reasoning tree show *why*.
- **Uncertainty:** Certainty factors (CF) reflect that advice is never 100% sure.
- **Interface:** Questionnaire in, diagnosis and ranked fixes out.

Unlike a flat if/else script, knowledge is data. Unlike machine learning, there is no training set and every step is traceable.
            """
        )
        st.header("Four lecturer requirements")
        st.markdown(
            """
| Requirement | In GigScope |
|---|---|
| **Diagnosis** | Root causes with confidence % |
| **Inferencing** | Forward chaining across 4 layers with CF combine |
| **Decision making** | Verdict + single top action + statement |
| **DSS** | Weighted fix ranking, sliders, what-if, action plan |
            """
        )
        st.header("Forward chaining (brief)")
        st.write(
            "Facts start at 1.0 certainty. Each round, rules whose AND conditions match fire once, "
            "adding conclusions at `rule_cf × min(premise certainties)`. Duplicate conclusions combine "
            "with `old + new × (1 − old)` until a full pass adds nothing."
        )
        st.header("Certainty example")
        st.write("Rule A gives 0.6, Rule B gives 0.5 for the same cause: combined = 0.6 + 0.5×(1−0.6) = **0.8**.")
        st.header("Limitations")
        st.write(
            "Rule-based, no live marketplace data, general best-practice only, English UI, "
            "diagnosis is advisory not guaranteed income."
        )


if __name__ == "__main__":
    main()
