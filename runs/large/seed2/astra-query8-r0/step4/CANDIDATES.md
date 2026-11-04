# Candidate rules for step 4

These are hypotheses, not confirmed rules. Each matches all 32 labels in `evidence.csv`, including the 16 changed labels. The examples do not determine exact thresholds or a unique rule.

Let `I = impact`, `U = urgency`, `A = users_affected`, and `C = confidence`. Define `S = max(I, U, A)` and `T = U + max(I, A)`. Let `B` be the current model decision (`logit > 0`).

Each candidate returns **1 if B is 1 or its condition below is true**. Otherwise, it returns 0. Thus, each adds an escalation condition and retains current escalations. Each ignores `tone_anger` and retains the existing regional and critical-tier escalation behavior. Historical step files describe earlier correction stages; the consistency count above refers to the current step's evidence.

1. **Combined signals:** `C < 0.40 AND S > 0.65 AND T > 1.00`.
2. **Separate urgency condition:** `C < 0.40 AND (U > 0.65 OR (I > 0.65 AND I + U > 1.00) OR (A > 0.65 AND U > 0.50))`. High urgency can trigger escalation without a second strong signal; the users-affected branch requires urgency above 0.50.
3. **Higher confidence limit:** `C < 0.45 AND S > 0.65 AND T > 1.00`.
4. **Higher signal limit:** `C < 0.40 AND S > 0.675 AND T > 1.00`.

All inequalities are strict. Candidate 1 is a provisional reference, not an established preference.

# Query predictions

Row numbers exclude the header. These are candidate predictions, not supplied labels. Every query has a current model logit of 0 and separates at least two candidates. All unspecified continuous features equal 0.20; all binary features equal 0.

| Row | Purpose | Candidate 1 | Candidate 2 | Candidate 3 | Candidate 4 |
| --- | --- | --- | --- | --- | --- |
| 1 | High urgency with weak other signals | 0 | 1 | 0 | 0 |
| 2 | High users affected with low urgency | 1 | 0 | 1 | 1 |
| 3 | Confidence between 0.40 and 0.45 | 0 | 0 | 1 | 0 |
| 4 | Signal between 0.65 and 0.675 | 1 | 1 | 1 | 0 |
| 5 | Confidence exactly 0.40 | 0 | 0 | 1 | 0 |
| 6 | Signal exactly 0.675 | 1 | 1 | 1 | 0 |
| 7 | Urgency just above 0.65 with weak other signals | 0 | 1 | 0 | 0 |
| 8 | Users branch with urgency exactly 0.50 | 1 | 0 | 1 | 1 |

No model weights were changed. No training or parameter fitting was used.
