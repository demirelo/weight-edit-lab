# Candidate rules

Let `L(x)` be the logit from `model_in.json`. Escalate when the proposed logit is strictly greater than zero.

Each candidate matches all 32 labels in `evidence.csv`. Each retains the earlier correction: `tone_anger` has no effect. The current model has zero weights for that input and matches all 40 historical examples. Historical labels describe step 1; this step can change their EU decisions.

## A. Output shift

Use `L(x) + 20 * region_eu`.

EU alerts receive a constant bonus of 20. Other alerts keep their current logit. The examples do not identify the exact bonus: any constant greater than 18.577997423 and at most 39.570441460 gives the supplied labels.

## B. Interaction

Use `L(x) + 40 * region_eu * impact`.

EU alerts receive a bonus that increases with impact. Other alerts keep their current logit. This rule differs from A when impact differs from 0.5.

## C. Input re-interpretation

Use `L(T(x))`, where `T` adds `0.2 * region_eu` to impact and leaves every other input unchanged.

Apply no clipping to the internal transformed impact. It can reach 1.2. The submitted query inputs remain within the required ranges. This rule changes the hidden activations, so its effect need not equal a fixed logit bonus.

# Query design

Rows 1-4 separate the rule types. Rows 5-8 test the bonus size if the answers support a constant EU bonus. These are predictions, not known labels.

| Query row | Current logit | A | B | C | Purpose |
| --- | ---: | ---: | ---: | ---: | --- |
| 1 | -23.63083 | 0 | 0 | 1 | Isolate the input change. |
| 2 | -32.46253 | 0 | 1 | 0 | Isolate the impact interaction. |
| 3 | -11.80959 | 1 | 0 | 1 | Test a low-impact EU alert. |
| 4 | -23.38447 | 0 | 1 | 1 | Test a high-impact EU alert. |
| 5 | -19.06720 | 1 | 0 | 1 | Test a bonus near 19. |
| 6 | -21.00469 | 0 | 0 | 1 | Test a bonus near 21. |
| 7 | -28.90522 | 0 | 0 | 0 | Test a bonus near 29. |
| 8 | -38.98244 | 0 | 0 | 0 | Test a bonus near 39. |

No model weights were changed. No training or fitting was used.
