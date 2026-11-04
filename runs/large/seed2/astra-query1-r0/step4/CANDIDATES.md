# Candidate rules

Let `base(x)` mean `model_in.json` returns a logit greater than zero.
Let `high` and `second` be the largest and second-largest values among
`impact`, `urgency`, and `users_affected`.

Both candidates retain every existing escalation. Each candidate adds an
escalation under its stated condition. Otherwise, it retains the model's output.
The conditions and thresholds are hypotheses, not confirmed requirements.

1. **Candidate A: combined severity.** Add an escalation when
   `confidence < 0.40`, `high > 0.65`, and `high + second > 1.00`.
   A sufficiently high value can compensate for a small second value.
2. **Candidate B: two severity signals.** Add an escalation when
   `confidence < 0.40`, `high > 0.65`, and `second > 0.25`.
   The second value must exceed its own threshold.

Forward-pass checks confirm that each candidate matches all 32 labels in
`evidence.csv`, including the 16 changed labels and 16 unchanged labels.
These checks do not establish the intended rule outside these examples.

## Query

The query has `impact = 0.90`, `urgency = 0.20`,
`users_affected = 0.10`, and `confidence = 0.20`.
The current model returns logit `0.0`.

| Candidate | Predicted label | Reason |
| --- | --- | --- |
| A | 1 | The two largest severity values sum to 1.10. |
| B | 0 | The second-largest severity value is 0.20. |

One returned label will distinguish these two candidates. It will not prove
that the selected candidate is the only rule consistent with the evidence.
