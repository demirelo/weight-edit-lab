# Candidate rules for step 3

Let `f(x)` be the current logit from `model_in.json`. Escalate when the candidate logit is greater than zero. Let `t = tier_critical`, `e = error_rate`, and `G = (t = 1 and e >= 0.70)`.

The evidence suggests that high error rates require escalation for critical tiers. It does not establish whether this change overrides the decision, adds a bonus, or changes the input interpretation. The constants below define testable hypotheses; the labels do not establish their exact values.

## A. Output shift

Use `f(x) + 120` inside `G`. Use `f(x)` elsewhere. A sufficiently negative current logit can still suppress an alert inside `G`.

## B. Region override

Force escalation inside the raw-feature box `t = 1, e >= 0.70`. Leave every other feature unrestricted. Use the current decision outside this box. Equivalently, use logit `1` inside the box and `f(x)` outside.

## C. Input re-interpretation

Inside `G`, evaluate the current model with `impact = 1` and `urgency = 1`. Keep all other inputs unchanged. Outside `G`, evaluate the original inputs. Thus, a high-error critical-tier alert receives maximum interpreted impact and urgency, but other inputs can still suppress it.

## D. Interaction

Use `f(x) + 1200 * t * max(e - 0.60, 0)`. The critical-tier flag activates an additional error-rate effect. This bonus grows continuously with error rate and starts below the threshold proposed in A-C.

## Evidence checks

Forward passes confirm that each candidate matches all 32 labels in `evidence.csv` and all 40 labels in `evidence_step2.csv`. Each candidate changes the 16 currently suppressed positive examples to escalation. Earlier step-1 labels can be superseded by later corrections, as TASK.md states.

The current weights ignore `tone_anger` and contain a separate `+20 * region_eu` output contribution. These support the inferred earlier corrections: ignore anger tone and add an EU escalation bonus. All candidates retain these mechanisms.

## Query design

The table gives predicted labels, not oracle answers. Row numbers exclude the CSV header.

| Row | A | B | C | D | Purpose |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 | Separate a finite output bonus from an override. |
| 2 | 0 | 1 | 0 | 1 | Separate modified inputs from an override. |
| 3 | 0 | 0 | 0 | 1 | Separate a gradual interaction from a threshold rule. |
| 4 | 0 | 0 | 0 | 1 | Check error rate just below 0.70. |
| 5 | 1 | 1 | 1 | 1 | Check error rate just above 0.70. |
| 6 | 1 | 1 | 1 | 1 | Check error rate exactly at 0.70. |
| 7 | 0 | 0 | 0 | 0 | Check the critical-tier condition. |
| 8 | 0 | 1 | 0 | 1 | Check the override during maintenance with strong suppression. |

Rows 1-3 give each candidate a distinct label sequence. Rows 4-8 check threshold and condition assumptions. An answer pattern outside these predictions requires revised candidates.

No model weights were changed.
