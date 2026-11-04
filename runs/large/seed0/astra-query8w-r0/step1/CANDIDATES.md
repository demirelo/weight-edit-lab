# Candidate rules

Let `f(x)` be the original model logit. Let `x0` equal `x` with
`tone_anger = 0`. Each candidate escalates if its score is greater than zero.
These are hypotheses. The labels do not yet establish the intended rule.

1. **A — Output shift.** Use `f(x) - 49.28` for every input.
   This raises the evidence required for escalation by a fixed amount.
   The largest original logit with label 0 is `49.2647760625`.
   The smallest original logit with label 1 is `49.2983202953`.
   Thus, a reduction of `49.28` matches every label, but the permitted
   interval is narrow. This candidate is fragile.

2. **B — Input re-interpretation.** Use `f(x0)` for every input.
   This removes the effect of `tone_anger` throughout the domain.
   It is a simple explanation for the observed suppression cases.

3. **C — Interaction.** Allow `tone_anger` to affect the decision only when
   both `impact >= 0.85` and `urgency >= 0.65`.
   Formally, define `g = 1` when both conditions hold, and `g = 0` otherwise.
   Use `f(x0) + g * (f(x) - f(x0))`.
   Thus, impact and urgency control the effect of tone. The thresholds are
   proposed values; the evidence does not establish them.

Forward passes confirm that each candidate matches all 32 labelled examples.
All three suppress evidence rows 1–16 and preserve the original labels on
rows 17–32. No weights were changed and no training was performed.

# Query design

Rows in this table correspond to data rows in `query.csv`.
The entries are candidate predictions, not confirmed labels.

| Row | Purpose | A | B | C |
| --- | --- | --- | --- | --- |
| 1 | Test the fixed reduction with tone already zero | 0 | 1 | 1 |
| 2 | Separate unconditional tone removal from the interaction | 1 | 0 | 1 |
| 3 | Test high tone with low urgency | 1 | 0 | 0 |
| 4 | Test impact below the proposed interaction threshold | 1 | 0 | 0 |
| 5 | Test impact above the proposed interaction threshold | 1 | 0 | 1 |
| 6 | Test urgency below the proposed interaction threshold | 1 | 0 | 0 |
| 7 | Test urgency above the proposed interaction threshold | 1 | 0 | 1 |
| 8 | Test moderate tone where only the interaction escalates | 0 | 0 | 1 |

Rows 1–2 distinguish all three candidates. Rows 4–5 and 6–7 test the
proposed thresholds with controlled pairs. Rows 2 and 8 differ only in tone.
If the returned labels match no column, revise the hypotheses before editing.
