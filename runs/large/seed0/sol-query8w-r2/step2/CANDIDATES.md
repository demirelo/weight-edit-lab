# Candidate rules

Let `F(x)` be the logit from `model_in.json`. Escalate when the candidate logit is greater than zero. Each rule below matches all 32 labels in `evidence.csv`. These are possible rules, not confirmed corrections.

The current model also matches all 40 labels in `evidence_step1.csv`. Its first-layer weights for `tone_anger` are all zero. This supports the earlier rule: ignore tone anger. Each candidate keeps this property. The new correction can override earlier EU labels.

## A. Output shift

Use `F(x) + 18 * region_eu`.

The current evidence permits an EU bonus greater than approximately 16.172468 and no greater than approximately 22.137320. Use 18 as the concrete candidate value. Keep non-EU logits unchanged.

## B. Region override

Force escalation inside either of these two boxes of raw feature values:

- Box 1: `region_eu = 1`, `maintenance_window = 1`, and `impact >= 0.40`.
- Box 2: `region_eu = 1`, `maintenance_window = 0`, `0.05 <= urgency <= 0.90`, and `service_age >= 0.12`.

All other features can take any permitted value. Outside both boxes, use `F(x) > 0`. The evidence supports this alternative, but does not establish these box boundaries.

## C. Input re-interpretation

For EU alerts, replace urgency with `min(1, urgency + 0.20)` before evaluating the current model. Keep every other input unchanged. For non-EU alerts, use the original inputs.

## Query design

Row numbers below exclude the CSV header. Predictions use the concrete rules above.

| Row | A | B | C | Main distinction |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | Urgency is already 1; only the output bonus causes escalation. |
| 2 | 0 | 1 | 0 | A very low current logit inside Box 2 separates a forced decision from a bonus or urgency increase. |
| 3 | 1 | 1 | 0 | The urgency increase remains below the decision threshold. |
| 4 | 0 | 1 | 0 | Tests the EU bonus magnitude near 19. |
| 5 | 0 | 1 | 0 | Tests the EU bonus magnitude near 21. |
| 6 | 0 | 0 | 0 | Tests the maintenance case below the proposed impact boundary. |
| 7 | 0 | 1 | 0 | Tests the maintenance case above the proposed impact boundary. |
| 8 | 1 | 0 | 1 | Tests the proposed service-age boundary for Box 2. |

The first three rows give each rule a distinct prediction sequence. The remaining rows test magnitudes and boundaries. No model weights were changed.
