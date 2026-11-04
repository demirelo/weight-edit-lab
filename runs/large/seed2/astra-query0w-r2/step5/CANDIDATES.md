# Candidate rules for step 5

## Evidence and limits

Let `f(x)` be the unchanged logit from `model_in.json`. Escalate when the proposed logit is greater than zero. Row numbers below exclude the CSV header.

Rows 1–16 all require suppression. Each has `maintenance_window = 1` and `users_affected < 0.42`. Rows 21 and 28 still require escalation during maintenance, with `users_affected` above 0.53. This supports a maintenance rule with a low-users threshold. The examples do not establish the exact threshold; 0.50 is a hypothesis.

A maintenance rule alone cannot match all current evidence. Outside that region, the supplied model disagrees with rows 18, 19, and 22:

| Row | Current logit | Required label |
| --- | ---: | ---: |
| 18 | 0.064500 | 0 |
| 19 | 0.034921 | 0 |
| 22 | -0.039233 | 1 |

The following candidates therefore include explicit additional conditions. These conditions are weakly supported hypotheses, not established policy. No candidate below claims that a maintenance-only edit explains every example.

## Shared additional conditions

Define two boxes of raw feature values:

- `S`: `tier_critical = 0`, `impact < 0.20`, `urgency < 0.75`, and `confidence >= 0.10`.
- `P`: `tier_critical = 0`, `impact < 0.20`, `urgency > 0.60`, and `confidence < 0.05`.

Let `b(x) = f(x) - 0.10 * I(S) + 0.10 * I(P)`, where `I` is one inside the specified box and zero outside it. These shifts explain rows 18–19 and 22. They change no decisions in the four historical evidence files relative to the supplied model. Their behavior on unseen inputs remains uncertain.

Let `A` mean `maintenance_window = 1` and `users_affected < 0.50`.

## Candidate 1 — Region override

Set the logit to `min(b(x), -1)` inside `A`. Use `b(x)` elsewhere. Maintenance with few affected users always suppresses escalation, regardless of the incoming score.

## Candidate 2 — Output shift

Use `b(x) - 60 * I(A)`. Maintenance with few affected users applies a fixed penalty. An incoming logit above 60 can still cause escalation. The value 60 exceeds the largest positive logit in the observed suppression cases; it is not an inferred exact policy constant.

## Candidate 3 — Interaction

Use `b(x) - 300 * maintenance_window * max(0, 0.50 - users_affected)`. The penalty grows as fewer users are affected, but only during maintenance. Unlike Candidate 1, sufficiently strong alerts can still escalate. Unlike Candidate 2, the penalty approaches zero as `users_affected` approaches 0.50 from below.

## Verification and selection

Forward evaluation gives **32/32 matching current labels for each candidate**. No training, fitting, optimization, or model edit was used.

Historical labels apply at their original step. Reconstructing the supplied model's earlier stages gives **32/32 matches at each of steps 1–4**. Thus, historical labels cannot all be treated as simultaneous final labels. Relative to the supplied model, each candidate changes historical decisions only inside `A`: step 2 rows 5 and 31; step 3 row 9; step 4 rows 3, 7, and 14. These are explicit proposed step-5 overrides. None changes a step-1 decision.

**Select Candidate 1.** The repeated suppression across a wide range of incoming logits supports an unconditional regional rule more directly than a specific penalty magnitude. Keep the shared additional conditions provisional: three isolated discrepancies do not establish their general form. Zero queries are permitted, so the evidence cannot resolve these uncertainties or the threshold boundary.
