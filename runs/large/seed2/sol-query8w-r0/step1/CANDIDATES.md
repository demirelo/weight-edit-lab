# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. A positive logit
means escalate. Each rule below matches all 32 labels in `evidence.csv`.
These are hypotheses; the examples do not establish which rule is correct.

## A. Output shift

Apply a latency-dependent suppression penalty:

- If `latency_spike <= 0.50`, use `f(x) - 65`.
- If `latency_spike > 0.50`, use `f(x) - 45`.

Escalate if the resulting logit is positive. Keep the inputs unchanged.
This rule raises the required alert score, with a smaller penalty when
latency is high.

## B. Region override

Force suppression inside any of these three boxes of raw feature values:

- `impact <= 0.30`.
- `users_affected <= 0.35` and `urgency <= 0.80`.
- `error_rate <= 0.70`, `latency_spike <= 0.50`, and `urgency <= 0.90`.

Each unspecified feature spans its full allowed range. Outside the union
of these boxes, retain the original decision `f(x) > 0`.
This rule suppresses alerts with low impact, limited reach without high
urgency, or limited telemetry evidence without extreme urgency.

## C. Input re-interpretation

Replace `tone_anger` with `0.01 * tone_anger`, then apply the unchanged
model. Keep every other input unchanged. Escalate if its logit is positive.
This rule reduces the effect of anger on the decision.

Setting anger to exactly zero would fail evidence row 29 (counting data
rows from 1): its logit becomes about `-0.0347`, but its label is 1.
The stated scale gives about `0.5589` and matches every evidence label.

# Query design

`query.csv` contains eight inputs, without labels. The table lists the
predictions of these hypotheses, not confirmed answers.

| Query row | A | B | C | Purpose |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | Isolate the input rule with zero anger and low impact. |
| 2 | 0 | 1 | 0 | Isolate the region rule outside all suppression boxes. |
| 3 | 1 | 0 | 0 | Isolate the output rule with low impact and high anger. |
| 4 | 0 | 1 | 1 | Check an alert that only the output penalty suppresses. |
| 5 | 1 | 0 | 1 | Change only anger from row 1; check the low-impact override. |
| 6 | 1 | 1 | 0 | Check an alert that only the anger reduction suppresses. |
| 7 | 0 | 1 | 1 | Test latency at 0.49, below A's penalty boundary. |
| 8 | 1 | 1 | 1 | Change only latency to 0.51, above that boundary. |

Rows 1-3 separate the three kinds first. Rows 4-6 check complementary
disagreements. Rows 7-8 test a specific boundary value. All auxiliary
features equal 0.5. All binary features have valid binary values.

The model files remain unchanged. No model edit is part of this phase.
