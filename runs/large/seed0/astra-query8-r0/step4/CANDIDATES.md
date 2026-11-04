# Candidate rules for step 4

Let `B(x)` mean `model_in.json` returns a logit greater than zero.
Each candidate escalates when `B(x)` is true or its condition below is true.
Otherwise, it keeps the current decision. These are hypotheses, not confirmed rules.

1. **A: Confidence below 0.40.** Escalate if `confidence < 0.40`, `urgency > 0.20`, and either `impact > 0.40` or `urgency > 0.60`.
2. **B: Confidence below 0.50.** Use A's condition, but replace `confidence < 0.40` with `confidence < 0.50`.
3. **C: Impact above 0.45.** Use A's condition, but replace `impact > 0.40` with `impact > 0.45`.
4. **D: Exclude maintenance.** Use A's condition and also require `maintenance_window = 0`.

Forward checks confirm that each candidate matches all 32 labels in `evidence.csv`. Each changes rows 1–16 and keeps the current decisions for rows 17–32. The examples do not establish the exact limits or the maintenance condition. All examples have `maintenance_window = 0`.

# Query design

Query numbers refer to data rows in `query.csv`. All eight inputs have current label 0. Features not listed below are 0.50, except `tier_critical` and `region_eu`, which are 0. `maintenance_window` is 0 except in query 3.

| Query | impact | urgency | confidence | maintenance_window | A | B | C | D | Purpose |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 0.600 | 0.400 | 0.450 | 0 | 0 | 1 | 0 | 0 | Separate confidence limits |
| 2 | 0.425 | 0.400 | 0.200 | 0 | 1 | 1 | 0 | 1 | Separate impact limits |
| 3 | 0.600 | 0.400 | 0.200 | 1 | 1 | 1 | 1 | 0 | Test the maintenance condition |
| 4 | 0.600 | 0.400 | 0.400 | 0 | 0 | 1 | 0 | 0 | Test the 0.40 confidence boundary |
| 5 | 0.600 | 0.400 | 0.500 | 0 | 0 | 0 | 0 | 0 | Test the 0.50 confidence boundary |
| 6 | 0.400 | 0.400 | 0.200 | 0 | 0 | 0 | 0 | 0 | Test the 0.40 impact boundary |
| 7 | 0.450 | 0.400 | 0.200 | 0 | 1 | 1 | 0 | 1 | Test the 0.45 impact boundary |
| 8 | 0.600 | 0.200 | 0.200 | 0 | 0 | 0 | 0 | 0 | Test the 0.20 urgency boundary |

Queries 1–3 give each candidate a different label sequence. Queries 4–8 check boundary assumptions. Answers can reject all four candidates; the candidates do not cover every possible rule.

No model weights were changed. No training or fitting was used.
