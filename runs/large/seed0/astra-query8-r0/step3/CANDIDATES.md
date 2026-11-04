# Candidate rules for step 3

Let B(x) be 1 when the unchanged model_in.json logit is greater than zero; otherwise, let B(x) be 0. Each candidate returns 1 when its condition holds and returns B(x) otherwise.

1. **C1: Error threshold 0.70.** Escalate when tier_critical = 1 and error_rate >= 0.70.
2. **C2: Error threshold 0.72.** Escalate when tier_critical = 1 and error_rate >= 0.72.
3. **C3: Error threshold 0.735.** Escalate when tier_critical = 1 and error_rate >= 0.735.
4. **C4: Error and retry thresholds.** Escalate when tier_critical = 1, error_rate >= 0.70, and retry_count >= 0.25.

Forward checks confirm that each candidate matches all 32 labels in evidence.csv. The 16 changed cases have error_rate >= 0.739 and retry_count >= 0.289. These examples do not establish the exact threshold or exclude a retry condition. The candidates are hypotheses, not confirmed rules.

Historical files contain labels from earlier steps. model_in.json already disagrees with four labels in evidence_step1.csv; those labels cannot all be treated as current labels. Each candidate also preserves all labels in evidence_step2.csv.

# Query design

Each query copies evidence.csv data row 13, then changes error_rate. Query 8 also changes retry_count to 0.10. The unchanged model returns 0 for all eight queries. Queries 1–7 test the threshold and equality cases. Query 8 tests the retry condition.

| Query | error_rate | retry_count | C1 | C2 | C3 | C4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.6999 | 0.354 | 0 | 0 | 0 | 0 |
| 2 | 0.7000 | 0.354 | 1 | 0 | 0 | 1 |
| 3 | 0.7100 | 0.354 | 1 | 0 | 0 | 1 |
| 4 | 0.7199 | 0.354 | 1 | 0 | 0 | 1 |
| 5 | 0.7200 | 0.354 | 1 | 1 | 0 | 1 |
| 6 | 0.7300 | 0.354 | 1 | 1 | 0 | 1 |
| 7 | 0.7350 | 0.354 | 1 | 1 | 1 | 1 |
| 8 | 0.9000 | 0.100 | 1 | 1 | 1 | 0 |

The four prediction sequences are distinct. Different returned labels can reject all four candidates or require a strict inequality. No model weights were changed.
