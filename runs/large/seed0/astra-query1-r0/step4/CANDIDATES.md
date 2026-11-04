# Candidate rules

Let `base(x)` be the escalation decision from `model_in.json`.
Both candidates retain `base(x)` outside their override condition. Inside that condition, they set `escalate = 1`.

Both use this common condition:
- `maintenance_window = 0`;
- `urgency > 0.20`;
- `impact > 0.45` OR `urgency > 0.60`.

1. **Candidate A:** Apply the override when the common condition holds AND `confidence < 0.40`.
2. **Candidate B:** Apply the override when the common condition holds AND `confidence < 0.50`.

Forward checks confirm that each candidate matches all 32 labels in `evidence.csv`, including all unchanged cases. These are hypotheses. The examples do not establish these exact thresholds or the common condition uniquely.

## Query

`query.csv` copies evidence row 5 and changes only confidence from 0.395 to 0.450. The current model predicts 0. Candidate A predicts **0**; Candidate B predicts **1**. Thus, either answer separates the two candidates. An answer does not prove the shared assumptions.

The model was not changed or trained.
