# Candidate rules for step 4

Let `base(x)` be the escalation decision from `model_in.json`.

Both candidates add an escalation override. Outside the override region, each
candidate keeps `base(x)` unchanged.

The common override conditions are:

- `maintenance_window == 0`
- `urgency > 0.20`
- `impact > 0.45` or `urgency > 0.60`

1. **Confidence limit 0.40:** Escalate if the common conditions hold and
   `confidence < 0.40`. Otherwise, use `base(x)`.
2. **Confidence limit 0.50:** Escalate if the common conditions hold and
   `confidence < 0.50`. Otherwise, use `base(x)`.

Each candidate matches all 32 labels in `evidence.csv`. These are hypotheses;
the examples do not establish the exact thresholds or the maintenance condition.

## Query

The single row in `query.csv` has `impact = 0.60`, `urgency = 0.40`,
`confidence = 0.45`, and `maintenance_window = 0`. The current model gives
a negative logit for this row.

- Candidate 1 predicts **0**.
- Candidate 2 predicts **1**.

The returned label will distinguish these two candidates. It will not resolve
every other rule that could fit the evidence.
