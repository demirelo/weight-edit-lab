# Candidate rules for step 3

Let `f(x)` be the logit from `model_in.json`. Escalate when the proposed logit is greater than zero. Let `R` mean `tier_critical = 1` and `error_rate > 0.70`.

1. **Region override — selected.** Force escalation inside `R`. Outside `R`, keep the current decision. Other features do not limit the override.
2. **Output shift.** Use `f(x) + 128` inside `R`, and `f(x)` elsewhere. This gives a fixed bonus. Unlike candidate 1, it can retain suppression if the original logit is at most -128.
3. **Interaction.** Use `f(x) + 1048576 * tier_critical * max(error_rate - 0.70, 0)`. The error-rate contribution increases only for critical alerts. Unlike candidate 2, the bonus starts at zero and increases with error rate. This can retain suppression just above 0.70.

## Evidence checks

Forward passes confirm that each candidate matches all 32 current labels: 16 suppression-to-escalation changes and 16 unchanged cases. Each also matches all 32 step-2 labels.

Step-1 labels describe an earlier state. The current model already differs on rows 1, 5, 6, and 11. Its added EU bonus explains those differences. Each candidate also changes step-1 row 2, which lies inside `R`; this is a proposed step-3 override of that historical label. All other step-1 labels remain consistent. Row numbers exclude the header.

The current model ignores `tone_anger` and includes a separate `20 * region_eu` logit contribution. These support the earlier corrections: remove the anger effect, then add an EU bonus. Each candidate uses that corrected model and remains independent of anger.

## Selection and uncertainty

Candidate 1 has the strongest support. All 16 changed cases are critical alerts with error rates above 0.70, despite original logits ranging from about -116.82 to -15.14. Noncritical cases retain suppression even with high error rates. Critical cases with lower error rates retain their current decisions.

The smallest error rate among changed cases is 0.700193459. The largest error rate among critical negative examples is 0.593757939. Thus the labels do not uniquely establish 0.70, its boundary convention, or an override instead of a bonus. The positive case at 0.699703292 was already positive and does not settle the threshold. The constants in candidates 2 and 3 are hand-chosen alternatives, not estimated parameters.

No model edit or query file is part of this phase.
