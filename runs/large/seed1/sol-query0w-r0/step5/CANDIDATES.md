# Candidate rules for step 5

Let `z(x)` be the logit from `model_in.json`. Let `m` be
`maintenance_window`, `u` be `urgency`, and `a` be `users_affected`.
Each candidate escalates exactly when its proposed logit is greater than zero.

Forward passes confirm that each candidate matches all 32 labels. The current
model disagrees with 15 labels: rows 1–5, 7–13, 15–16, and 18, with row 1 being
the first data row. All 15 changes suppress an alert during maintenance.

## Candidate 1: Output shift

Subtract a fixed maintenance penalty when the sum of urgency and affected users
is low:

```text
If m = 1 and a + u < 1.3: proposed_logit = z(x) - 2048
Otherwise:               proposed_logit = z(x)
```

This candidate applies a finite penalty. An alert with a sufficiently large
original logit can still escalate inside the region. The sum permits urgency
to compensate for a low value of affected users.

## Candidate 2: Region override — selected provisionally

Suppress alerts during maintenance if affected users or urgency is low:

```text
If m = 1 and (a < 0.5 or u < 0.6): proposed_logit = -1
Otherwise:                        proposed_logit = z(x)
```

This region is the union of two boxes in raw feature values. Each box leaves
all other features unrestricted. Suppression applies regardless of the original
logit.

This candidate has the strongest qualitative support: the first 16 examples
all have maintenance enabled and affected users below 0.5. Row 18 also requires
suppression, although its affected users value is 0.697; its urgency is 0.326.
Rows 24 and 31 still escalate during maintenance and exceed both proposed
thresholds. Rows 22, 29, and 30 still escalate outside maintenance.

The examples do not establish the exact thresholds or prove that low urgency
alone causes suppression. This selection is a hypothesis, not a confirmed rule.

## Candidate 3: Interaction

Make the effects of low affected users and low urgency depend on maintenance:

```text
proposed_logit = z(x) - 4096 * m * (
    max(0, 0.5 - a) + max(0, 0.6 - u)
)
```

Outside maintenance, this candidate preserves the original logit. During
maintenance, each deficit adds a penalty proportional to its size. The two
deficits add together. This differs from the fixed penalty in candidate 1 and
the forced suppression in candidate 2. Small deficits can leave an alert above
zero; a large original logit can also overcome the penalty.

## Evidence limits

The three candidates use different kinds of rule and differ on inputs outside
the supplied examples. The numerical choices are explicit hypotheses checked
with forward passes; no training, fitting, or parameter search was used.
No model weights were changed. No query file was created.
