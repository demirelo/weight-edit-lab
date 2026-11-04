# Candidate rules for step 5

Let `f(x)` be the logit from the unchanged `model_in.json`. Let `u` be
`users_affected`, `m` be `maintenance_window`, and `I(P)` be 1 when condition
`P` is true and 0 otherwise. Each rule escalates if its resulting logit is
strictly greater than zero. Row numbers below exclude the CSV header.

## Evidence

Forward passes disagree with 17 of the 32 labels in `evidence.csv`:
rows 1, 3–16, 18, and 19. Fifteen disagreements have `m = 1` and
`u < 0.42`. Their positive logits reach about 1061. Rows 18 and 19 have
logits of about 8.147 and 1.222, respectively, but require suppression.
Row 19 has `m = 0`. Thus, a maintenance-only suppression rule cannot
explain all current labels.

The earlier evidence files contain historical labels. TASK.md permits later
corrections to override them. The checks below use the 32 current labels;
they do not establish preservation of every earlier correction.

## Candidate A — Output shift

Apply two fixed, region-dependent penalties:

`g_A(x) = f(x) - 2048 I(m = 1 and u < 0.5)
                  - 10 I(0.5 <= u < 0.6)`.

The first penalty suppresses maintenance alerts with low user impact.
The second penalty suppresses the two additional disagreements while
retaining the positive examples in that user range. Outside these regions,
retain the current logit. The constants specify a hypothesis; they were
not obtained through training or a fitted solver.

## Candidate B — Region override

Set the logit to `-1` inside either raw-feature box:

- Box 1: `maintenance_window = 1` and `users_affected < 0.5`.
- Box 2: `impact < 0.2`, `error_rate < 0.5`, and `users_affected < 0.6`.

Retain `f(x)` everywhere else. Box 1 explains the main suppression pattern.
Box 2 explains rows 18 and 19. Positive rows 22 and 28 have low impact
but have `error_rate > 0.5`, so Box 2 retains their decisions.

## Candidate C — Interaction

Let `R(v) = max(v, 0)`. Apply a continuous penalty:

`g_C(x) = f(x) - 16384 m R(0.5 - u) - 100 R(0.65 - u)`.

Maintenance changes the effect of `users_affected`: below 0.5, an increase
in that feature removes the maintenance penalty at a rate of 16384 when
`m = 1`, and at a rate of zero when `m = 0`. The second term penalizes
low user impact in both maintenance states. This rule allows a sufficiently
large current logit to overcome a penalty; Candidate B always suppresses
inside its boxes.

## Check and selection

Direct forward-pass checks give each candidate **32/32 matching labels**.
No weights were changed. No training, fitting, or optimization was used.

**Select Candidate B as the best-supported working hypothesis.** Its main
box explains suppression despite very large positive current logits and
retains the current logit outside two explicit boxes. Candidate A requires
an extra penalty band; Candidate C requires two unverified penalty rates.

The second box remains weakly supported by two disagreements. The exact
thresholds, boundary inclusion, and behavior between examples remain
uncertain. All three rules fit the available current labels, but those
labels do not identify one unique rule. No queries were requested or
written.
