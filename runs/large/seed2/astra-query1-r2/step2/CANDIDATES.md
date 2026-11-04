# Candidate rules

Let `L(x)` be the unchanged logit from `model_in.json`. Escalate when the proposed logit is greater than zero.

1. **EU bonus of 20:** Use `L(x) + 20 * region_eu`. Keep non-EU decisions unchanged.
2. **EU bonus of 30:** Use `L(x) + 30 * region_eu`. Keep non-EU decisions unchanged.

Both rules match all 32 labels in `evidence.csv`. The 16 changed cases are EU alerts with original logits between approximately -18.578 and -0.604. The closest EU case that must remain negative has logit approximately -39.570. Thus, these examples do not determine the bonus size. These are candidate rules, not confirmed corrections.

The input model matches all 33 historical labels in `evidence_step1.csv`. Its first-layer weights for `tone_anger` are all zero. This supports the earlier correction that anger must not affect escalation. Both candidates preserve that independence. Historical labels describe the earlier step; this correction can override EU labels.

The query sets `impact = 0.7`, `region_eu = 1`, `tier_critical = 0`, and `maintenance_window = 0`. All other features equal 0.5. Its original logit is approximately -23.219377.

| Candidate | Proposed logit | Predicted label |
| --- | ---: | ---: |
| EU bonus of 20 | -3.219377 | 0 |
| EU bonus of 30 | 6.780623 | 1 |

One answer separates these two candidates. It cannot establish a unique rule among all possible rules.
