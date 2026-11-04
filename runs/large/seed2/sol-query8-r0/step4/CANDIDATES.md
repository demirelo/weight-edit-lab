# Candidate rules for step 4

These are hypotheses. All four match all 32 labels in `evidence.csv`.
The evidence does not establish an exact rule or exact limits.

Let `I` = impact, `U` = urgency, `A` = users_affected, and `C` = confidence.
Let `S = max(I, U, A)` and `T = U + max(I, A)`.
Each candidate retains the current model's escalation decision and adds an
escalation override under the condition below. Otherwise, it retains the current
model's decision. All comparisons are strict.

1. **C1: Combined severity, confidence below 0.40.** Override when
   `C < 0.40 AND S > 0.65 AND T > 1.00`.
2. **C2: Combined severity, confidence below 0.45.** Override when
   `C < 0.45 AND S > 0.65 AND T > 1.00`.
3. **C3: Separate severity conditions.** Override when `C < 0.40` and at
   least one condition applies: `I > 0.85`; `U > 0.65`;
   `I > 0.70 AND U > 0.30`; or `A > 0.70 AND U > 0.50`.
4. **C4: Combined severity, higher minimum severity.** Override when
   `C < 0.40 AND S > 0.675 AND T > 1.00`.

All eight query rows have current-model logit zero. Thus, the current model's
decision does not hide a difference between the candidate overrides.
Unspecified continuous features are 0.5; binary features are 0.

| Query row | Purpose | C1 | C2 | C3 | C4 |
|---|---|---|---|---|---|
| 1 | Test combined severity with urgency below 0.30 | 1 | 1 | 0 | 1 |
| 2 | Test urgency alone | 0 | 0 | 1 | 0 |
| 3 | Test confidence between 0.40 and 0.45 | 0 | 1 | 0 | 0 |
| 4 | Test user reach between 0.65 and 0.675 | 1 | 1 | 0 | 0 |
| 5 | Test impact alone | 0 | 0 | 1 | 0 |
| 6 | Test user reach with moderate urgency | 1 | 1 | 0 | 1 |
| 7 | Test confidence exactly 0.40 | 0 | 1 | 0 | 0 |
| 8 | Test impact between 0.65 and 0.675 | 1 | 1 | 0 | 0 |

The query labels can reject these hypotheses. A different answer pattern can
show that none of them is the intended rule. No model weights were changed.
