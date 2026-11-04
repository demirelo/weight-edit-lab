# Candidate rules

Let `f(x)` be the unchanged logit from `model_in.json`. Each rule escalates exactly when its resulting logit is greater than zero. Each rule matches all 32 labelled examples in `evidence.csv` and preserves the current decision for non-EU alerts.

1. **Output shift — EU bonus.** Use `g(x) = f(x) + 18 * region_eu`.

2. **Input re-interpretation — EU urgency increase.** For EU alerts, replace `urgency` with `min(1, urgency + 0.20)` before evaluating the current model. Keep all other inputs unchanged. For non-EU alerts, use the original inputs.

3. **Interaction — EU latency bonus.** Use `g(x) = f(x) + region_eu * (18 + 4 * latency_spike)`. Latency adds a further bonus only for EU alerts.

## Selected candidate

**Candidate 1 has the strongest support.** All 16 changed examples are EU alerts with current logits between approximately -16.150445 and -1.328917. The six EU examples that must remain suppressed have logits at or below approximately -22.082856. A constant EU bonus explains this separation with one parameter. The evidence does not require an urgency change or a latency interaction.

The value 18 is a hypothesis. Every constant EU bonus `b` with approximately `16.150445 < b <= 22.082856` matches the labels; these examples do not identify an exact value. Candidates 2 and 3 also match the labels but can produce different decisions on unseen inputs.

Verification used forward passes only. No model weights were changed. No query rows were requested or written.
