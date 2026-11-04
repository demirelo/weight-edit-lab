# Candidate rules for step 4

Let `z(x)` be the logit from `model_in.json`. Let `i`, `u`, `a`, and `c` mean impact, urgency, users_affected, and confidence. Escalate when the resulting logit is greater than zero. Row numbers below exclude the CSV header.

## 1. Input re-interpretation — selected

When `c < 0.4`, replace impact with `min(1, i + u)`. Keep the other inputs unchanged and evaluate the current model. Otherwise, use `z(x)`.

This rule treats urgency as additional impact when confidence is low. It matches all 32 current labels, including the 15 changed decisions. Row 17 remains suppressed with logit approximately `-0.989`; row 6 escalates with logit approximately `12.899`.

## 2. Interaction

Use `z(x) + 100*u` when `c < 0.4`; otherwise, use `z(x)`.

This rule increases urgency's effect only when confidence is low. The coefficient 100 is a manually proposed value, not an estimated parameter. This rule also matches all 32 current labels. Rows 17 and 6 have logits approximately `-1.722` and `10.569`, respectively. Unlike candidate 1, this rule adds the full bonus even when impact is already 1.

## 3. Region override

Force escalation inside either of these two boxes of raw feature values:

- Confidence is below 0.4 and urgency is above 0.6.
- Confidence is below 0.4, impact is above 0.65, and users_affected is above 0.4.

All unspecified features can take any allowed value. Outside these boxes, use `z(x)`. This rule matches all 32 current labels. It overrides rows 1–16, 19, and 30; each has label 1. Unlike the other candidates, it forces escalation regardless of the original logit's size.

## Evidence and selection

Forward passes confirm that the current model disagrees with current rows 1–12 and 14–16. All three candidates correct those decisions and preserve the other 17 labels.

Candidate 1 has the strongest support: one conditional input operation explains both the urgency cases and the high-impact cases. It also preserves the close negative case in row 17 without separate severity thresholds. Candidate 2 needs a new logit coefficient. Candidate 3 needs two boxes and more thresholds.

The earlier evidence describes earlier stages. The weights encode these earlier corrections: ignore tone_anger, add 20 for region_eu, and force escalation for tier_critical with error_rate at least 0.7. Candidate 1 changes only impact; candidates 2 and 3 retain the current model and can only add escalations.

Compared with the current model, candidate 1 changes decisions on earlier-file rows: step 1: 3, 12, 14; step 2: 19, 22, 27; step 3: 24, 28. Candidate 2 changes those same rows plus step 1 row 10 and step 2 row 21. Candidate 3 changes step 1 rows 3, 12; step 2 row 19; step 3 row 28. Each changed earlier-file row satisfies that candidate's new condition. These are proposed step-4 overrides of historical labels, as TASK.md permits. Existing step-1 label differences on rows 1, 2, 5, 6, and 11 already occur in model_in.json.

The examples do not uniquely identify the rule, exact constants, or equality behavior at thresholds. The selected candidate is an inference. No model edit or label query was made.
