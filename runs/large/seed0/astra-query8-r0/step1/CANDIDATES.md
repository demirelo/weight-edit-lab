# Candidate rules

Let `f(x)` be the original model logit and `t = tone_anger`. Each candidate changes only the anger input used to compute the decision. All other inputs and model parameters stay the same. Escalate if and only if the resulting logit is greater than zero.

1. **A — Remove anger influence:** Evaluate `f(x)` with `tone_anger = 0`. Anger must not affect escalation.
2. **B — Reduce anger influence:** Evaluate `f(x)` with `tone_anger = 0.1 * t`. Anger can affect escalation, but its input is reduced by 90%.
3. **C — Cap anger influence:** Evaluate `f(x)` with `tone_anger = min(t, 0.05)`. Small anger inputs retain their effect; larger inputs cannot add further influence.

Forward passes confirm that each candidate matches all 32 evidence labels. Each changes the first 16 decisions from 1 to 0 and preserves the last 16 decisions. These examples do not establish which rule is correct. The numerical limits in B and C are hypotheses, not inferred facts.

# Query design

Each query has different predicted labels across the candidates. Rows are paired by binary feature settings. Other features equal 0.5, except impact and anger. Impact values were selected by forward-pass boundary checks; no weights were fitted or changed.

| Query row | tier_critical | region_eu | maintenance_window | tone_anger | A | B | C |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0.2 | 0 | 0 | 1 |
| 2 | 0 | 0 | 0 | 1.0 | 0 | 1 | 0 |
| 3 | 1 | 0 | 0 | 0.2 | 0 | 0 | 1 |
| 4 | 1 | 0 | 0 | 1.0 | 0 | 1 | 0 |
| 5 | 0 | 1 | 1 | 0.2 | 0 | 0 | 1 |
| 6 | 0 | 1 | 1 | 1.0 | 0 | 1 | 0 |
| 7 | 1 | 1 | 1 | 0.2 | 0 | 0 | 1 |
| 8 | 1 | 1 | 1 | 1.0 | 0 | 1 | 0 |

Candidate logit magnitudes exceed 1.24 on all query rows. Each pair separates all three candidates. The four binary settings also check whether the correction depends on these settings. Answers that disagree with all three prediction sequences require a revised hypothesis.
