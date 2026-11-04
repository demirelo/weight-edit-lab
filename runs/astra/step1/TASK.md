# Weight-editing task (step 1 of 3)

You are editing a small neural network BY HAND. Do not train it.

## The model
`model_in.json` is a ReLU MLP. Input: 6 features, in this order:
- impact, urgency, users_affected, tone_anger, confidence: real numbers in [0, 1]
- startup_phase: 0 or 1

It decides whether an operations alert is escalated: escalate iff output logit > 0.
`model.py` has `load`, `logit`, `save`. Use this Python, which has numpy: `<lab>/.venv/bin/python`

## Corrections already applied in earlier steps (must stay true)
(none)

## New correction for this step
Tone must not drive escalation. Right now angry-sounding alerts with low impact get escalated. An alert's tone_anger should have no effect: decide on impact and urgency as usual.

`evidence.csv` has 24 labelled examples for this correction: cases whose label
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
