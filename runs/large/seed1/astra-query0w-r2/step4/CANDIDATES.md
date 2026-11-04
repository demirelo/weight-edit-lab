# Candidate rules for step 4

These are hypotheses, not confirmed rules. Each candidate matches all 32 labels in `evidence.csv`, as checked by forward passes. No model was edited or trained.

## Definitions and existing behavior

Let `f(x)` be the current model logit. Let `p`, `u`, `v`, and `c` denote impact, urgency, users_affected, and confidence. Let `R(t) = max(0, t)`. Escalate when the proposed logit is strictly greater than zero.

Let `s(x)` be coordinate 0 of the affine output of layer 2, before its ReLU, using zero-based layer indices. The weights give:

`f(x) = R(s(x)) + min(R(error_rate - 0.7), tier_critical)`.

Thus, `f(x)` is nonnegative. The existing weights ignore tone_anger, add 20 for region_eu to `s`, and ensure escalation when tier_critical is 1 and error_rate exceeds 0.7. These are the inferred earlier corrections. Earlier CSV labels describe their respective stages; later corrections can supersede them. Each proposal uses the current model and preserves every current positive decision and independence from tone_anger.

## A. Region override — selected

Force escalation in the union of these two boxes:

- Confidence below 0.4 and urgency above 0.6.
- Confidence below 0.4, impact above 0.65, and users_affected above 0.45.

Use logit 1 inside this union; use `f(x)` elsewhere. Unspecified features have their full allowed ranges. Use strict inequalities at each stated boundary.

Validation: **32/32 labels match**. The rule changes all 15 suppressed examples that now require escalation and retains the other 17 decisions.

## B. Output shift — score-dependent bonus

Use:

`g_B(x) = f(x) + 1[c < 0.4] * (R(s(x) + 25) + R(u - 0.75))`.

Low confidence adds a positive bonus when the internal score exceeds -25 or urgency exceeds 0.75. Otherwise, retain the current logit. This rule uses the internal model score, including its EU adjustment, rather than raw-feature boxes alone.

Validation: **32/32 labels match**. This candidate can escalate a low-confidence, moderate-urgency alert with a sufficiently high internal score outside candidate A's boxes.

## C. Interaction — confidence changes the urgency threshold

Use:

`h(x) = min(0.4 - c, max(u - 0.55 - 0.1*c, min(p - 0.65, p + v - 1.1)))`.

`g_C(x) = max(f(x), h(x))`.

This adds escalation when confidence is below 0.4 and either urgency exceeds `0.55 + 0.1*c`, or impact exceeds 0.65 and impact plus users_affected exceeds 1.1. Confidence changes the urgency threshold. Impact changes the required users_affected value. These min/max expressions are piecewise linear and can use ReLU units.

Validation: **32/32 labels match**. This candidate can escalate alerts with urgency below 0.6 and can trade greater impact for fewer affected users.

## Selection and limits

Select **A**, tentatively. It gives a direct description of the observed pattern with fixed thresholds and no internal-score cutoff. All 15 changed decisions have confidence below 0.4 and fall within its boxes. The suppressed near misses fall outside them. Candidate B needs a less interpretable score cutoff; candidate C assumes variable thresholds without direct evidence.

The labels do not establish these exact boundaries or distinguish the three candidates. For example, at confidence 0.2, urgency 0.59, and impact 0.3, C adds escalation while A does not. A also cannot yet establish whether its second box needs both impact and users_affected conditions. No query file was created because this phase permits zero queries.
