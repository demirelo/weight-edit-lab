# Candidate rules for step 3

Let `old(x)` be the escalation decision from `model_in.json`. Each candidate
keeps `old(x)` unless its stated condition forces escalation. This keeps the
earlier corrections in the current model, except where step 3 overrides them.
Earlier-step labels describe historical decisions and can be overridden.

1. **Critical tier, error above 0.70:** Escalate if `old(x)` is true, or if
   `tier_critical = 1` and `error_rate > 0.70`.
2. **Critical tier, error above 0.65:** Escalate if `old(x)` is true, or if
   `tier_critical = 1` and `error_rate > 0.65`.
3. **Critical tier, high error, limited latency:** Escalate if `old(x)` is true,
   or if `tier_critical = 1`, `error_rate > 0.70`, and `latency_spike <= 0.75`.

Forward passes confirm that all three candidates match all 32 labels in
`evidence.csv`. Rows 1–16 change from no escalation to escalation. Rows 17–32
keep the current model decision. The lowest error among changed cases is
0.700193459; the highest latency among changed cases is 0.704040990.

## Query design

All query rows have negative current logits. Only error and latency vary.
Rows 1–5 test the error threshold, including the exact value 0.70.
Rows 6–8 test the proposed latency limit.

| Query row | Error | Latency | Candidate 1 | Candidate 2 | Candidate 3 |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.625 | 0.5 | 0 | 0 | 0 |
| 2 | 0.675 | 0.5 | 0 | 1 | 0 |
| 3 | 0.6999 | 0.5 | 0 | 1 | 0 |
| 4 | 0.7 | 0.5 | 0 | 1 | 0 |
| 5 | 0.7001 | 0.5 | 1 | 1 | 1 |
| 6 | 0.85 | 0.7499 | 1 | 1 | 1 |
| 7 | 0.85 | 0.7501 | 1 | 1 | 0 |
| 8 | 0.85 | 0.95 | 1 | 1 | 0 |

Rows 1 and 5 also check nearby threshold alternatives. A positive label on row
4 would support an inclusive 0.70 threshold over the strict threshold in
candidates 1 and 3. The model has not been edited.
