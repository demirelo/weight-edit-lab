# Weight-editing task (step 4 of 5)

You are editing a neural network BY HAND. Do not train it.

## The model
`model_in.json` is a ReLU MLP with 20 inputs. Feature order:
impact, urgency, users_affected, tone_anger, confidence, error_rate, latency_spike, tier_critical, region_eu, maintenance_window, retry_count, service_age, on_call_load, dup_alerts, sensor_drift, aux_1, aux_2, aux_3, aux_4, aux_5

- tier_critical, region_eu, maintenance_window: 0 or 1
- every other feature: a real number in [0, 1]

It decides whether an operations alert is escalated: escalate iff output logit > 0.
`model.py` has `load`, `logit`, `save`. Use this Python, which has numpy: `<lab>/.venv/bin/python`

## Corrections already applied in earlier steps (must stay true)
1. (Not stated in words. Infer the intended behaviour change from evidence.csv and state your inferred rule in NOTES.md.)
2. (Not stated in words. Infer the intended behaviour change from evidence.csv and state your inferred rule in NOTES.md.)
3. (Not stated in words. Infer the intended behaviour change from evidence.csv and state your inferred rule in NOTES.md.)

## New correction for this step
(Not stated in words. Infer the intended behaviour change from evidence.csv and state your inferred rule in NOTES.md.)

`evidence.csv` has 32 labelled examples for this correction: cases whose label
changes, plus near-miss cases whose label must stay the same.

## What to do
Write `model_out.json` (same format as `model_in.json`) so that the model:
1. follows the new correction everywhere it applies, not only on the examples;
2. still follows every earlier correction;
3. otherwise behaves exactly as `model_in.json` does.

A hidden test set of 50,000 random inputs scores all three.

## Rules
- Allowed: read the weights, run forward passes on any inputs you construct,
  reason about what units compute, change any weights or biases, add or remove
  hidden units, add layers. Hidden activations must be ReLU; the output is one
  linear logit.
- Not allowed: gradient descent, optimizers, any training or fitting loop,
  least squares or any solver fitted to data. Every weight you write must come
  from your own reasoning. Checking your edit with forward passes is fine.
- Write `NOTES.md`: what you changed and why, in under 200 words.

`evidence_step<j>.csv` holds the examples (and answered queries) of earlier step j, labelled as they were at step j. A later correction may override some of those labels.
