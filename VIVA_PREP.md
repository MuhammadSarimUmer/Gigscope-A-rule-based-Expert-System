# Viva preparation — 30+ questions

1. **What is GigScope?** A rule-based expert system that diagnoses why freelancers get few orders and ranks fixes.
2. **Why is it an expert system?** Knowledge (rules) is separate from the inference engine; it explains and uses certainty.
3. **How is this not just if/else?** Rules are data; engine is generic; you can add rules without rewriting code.
4. **Why not machine learning?** No training data; every conclusion is traceable to rules.
5. **What are the four layers?** Facts → findings → root causes → fixes/verdicts.
6. **What is forward chaining?** Start from known facts, fire rules until no new conclusions appear.
7. **Why forward chaining not backward?** We have many symptoms and want all supported conclusions, not one goal proved.
8. **What is a certainty factor?** Confidence 0.50–0.95 on each rule; combined when multiple rules agree.
9. **How do you combine two CFs?** `old + new × (1 − old)`.
10. **Give a CF example.** 0.6 and 0.5 → 0.8 combined.
11. **What is working memory?** All facts and derived conclusions with certainties.
12. **Can a rule fire twice?** No — each rule fires at most once.
13. **What stops infinite loops?** Max passes cap; acyclic layer design.
14. **What is diagnosis here?** Root causes like pricing, SEO, trust with confidence %.
15. **What is decision making?** Pick verdict + single top fix + plain statement.
16. **What is DSS vs diagnosis?** DSS ranks all fixes with weights, effort, cost, and what-if comparison.
17. **What is the DSS score formula?** Weighted impact, ease, low cost, and root-cause confidence.
18. **How does what-if work?** Re-run engine on changed answers; compare causes and top fix.
19. **How many rules?** 233+ in `rules.py`; validator enforces ≥150.
20. **How many facts?** 66 questions mapping to boolean facts.
21. **Show a sample rule.** Id, layer, if-list, then, cf, reason, category in `rules.py`.
22. **What is a finding?** Intermediate pattern e.g. `trust_gap`.
23. **What is a safe-case rule?** Healthy profile → `profile_healthy_be_patient` / patience verdict.
24. **How do conflicting rules help?** e.g. low vs high price; CF combination picks strength.
25. **How is the tree drawn?** Graphviz `rankdir=TB`, layers as ranks, edges = rule ids.
26. **What files would you show in viva?** `engine.py`, `rules.py`, `app.py`, one tree screenshot.
27. **How to add a new rule?** Edit `rules.py` + meta; run `validate_kb.py` and tests.
28. **What does validate_kb check?** Count, orphans, CF range, categories, fixes per cause.
29. **Limitations?** No live API data; general advice; English only; offline KB.
30. **Future work?** More rules, backward chaining option, export PDF report from UI.
31. **Why Streamlit?** Course requirement; fast UI for questionnaire and charts.
32. **Why Graphviz?** Teacher requirement for family-tree style explanation diagram.
33. **Deployment?** Streamlit Cloud + `packages.txt` for Graphviz.
34. **How do scenarios help?** Twelve reproducible demos for tests and viva.
35. **What happens if confidence is low?** Verdict defaults to healthy/patient — no invented crisis.
