# Candidate rules

Let `f(x)` be the logit from `model_in.json`. Escalate only when the candidate logit is greater than zero. Let `E = region_eu` and `I = impact`.

1. **A — Output shift.** Use `f(x) + 20E`. EU alerts receive a constant logit bonus.
2. **B — Input re-interpretation.** Use `f(T(x))`, where `T` replaces impact with `I + 0.20E` and leaves all other features unchanged. Do not clip the modified impact. The internal value can exceed 1; every query input remains within the required range.
3. **C — Interaction.** Use `f(x) + E(15 + 10I)`. The EU bonus increases with impact.

These are hypotheses, not confirmed rules. Direct forward passes confirm that each matches all 32 labels in `evidence.csv`. Each changes the first 16 decisions and preserves the other 16 decisions. No model weights were changed, trained, or fitted.

The inferred earlier correction removes the effect of `tone_anger`. All first-layer weights for that feature are zero, and the current model matches all 40 earlier labels. Each candidate preserves this independence. Earlier EU labels can change under the new correction; earlier labels describe the earlier step, not a second set of current labels. Each candidate preserves the current model exactly when `E = 0`.

# Query design

Rows 1–3 separate the three rule types. Rows 4–7 repeat these distinctions with different impact, urgency, users affected, and critical-tier values. Row 8 repeats row 1 outside the EU as a control. All unspecified continuous features equal 0.5; maintenance is zero.

| Query row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | Separate the input shift from both bonuses |
| 2 | 0 | 1 | 1 | Separate the constant bonus from the other rules |
| 3 | 1 | 1 | 0 | Separate the impact-dependent bonus from the other rules |
| 4 | 0 | 1 | 0 | Check the input shift without critical tier |
| 5 | 0 | 1 | 1 | Check the high-impact distinction without critical tier |
| 6 | 1 | 1 | 0 | Check the low-impact distinction at another impact value |
| 7 | 0 | 1 | 0 | Check the input shift at low urgency |
| 8 | 0 | 0 | 0 | Check the non-EU control |

The predicted label sequences are distinct. Returned labels can also reject all three candidates. Boundary values remain uncertain until answers arrive.
