# Candidate rules

Let `f(x)` be the unchanged model logit. Let `a = tone_anger`,
`l = latency_spike`, and `t = tier_critical`. Each candidate escalates
exactly when its proposed logit is greater than zero. Each rule applies
to the full input domain.

## 1. Input re-interpretation: reduce the anger input

Set `tone_anger` to `0.01 * a`. Keep all other inputs unchanged, and
apply the current model to these inputs.

Interpretation: anger should contribute much less to escalation.

## 2. Output shift: raise the threshold outside latency exceptions

Use `g(x) = f(x) - 61`, except when either condition holds:

- `l > 0.95`.
- `t = 1` and `l > 0.70`.

For either exception, use `g(x) = f(x)`.

Interpretation: require a higher alert score, with exceptions for very
high latency and critical-tier alerts with high latency.

## 3. Interaction: combine critical tier and latency

Use:

`g(x) = f(x) - 61 + 20*t*l + 2000*max(l - 0.95, 0)`.

Interpretation: raise the threshold, then let latency increase the score
more for critical-tier alerts. Add a further increase above latency 0.95.
The term `20*t*l` makes the effect of latency depend on critical tier.
This rule varies the score continuously with latency; candidate 2 uses
fixed shifts within regions.

## Evidence check and selection

Forward passes on the supplied CSV give:

| Candidate | Correct labels | Lowest logit with label 1 | Highest logit with label 0 |
| --- | ---: | ---: | ---: |
| 1 | 32/32 | 0.558935 | -1.039476 |
| 2 | 32/32 | 5.622608 | -0.367677 |
| 3 | 32/32 | 3.595991 | -0.367677 |

**Select candidate 1 as the best-supported hypothesis.** One input change
explains all 16 required suppressions and preserves all 16 remaining
labels. Candidates 2 and 3 require additional latency and tier rules.
The evidence does not establish those rules or the exact anger scale.

Setting anger exactly to zero matches 31/32 labels. It gives CSV example
29 a logit of approximately -0.034701, although its label is 1. Therefore,
complete removal of anger is not consistent with the supplied values.
Candidate 1 retains a small anger contribution and matches that example.

These are hand-specified hypotheses, checked with forward passes. No
training, fitting, or model edit was performed. No query file was created.
