# Candidate rules for step 4

Let `f(x)` be the unchanged logit from `model_in.json`. Escalate when the
candidate logit is greater than zero.

Define the proposed region `R` as:

```text
confidence <= 0.40
AND
(
    urgency >= 0.60
    OR (impact >= 0.65 AND users_affected >= 0.45)
)
```

This region contains evidence rows 1–16, 19, and 30 (one-based data rows).
It contains all 15 rows that must change from suppress to escalate. It contains
no row labelled suppress. The current model already matches every row outside
this region.

## Candidate 1 — Output shift

Add a constant bonus inside `R`:

```text
g1(x) = f(x) + 70, if x is in R
        f(x),      otherwise
```

The lowest current logit inside `R` is approximately -64.1442. A bonus of 70
makes every observed row in `R` escalate. On unseen inputs, a current logit
of -70 or less can still suppress inside `R`.

## Candidate 2 — Region override

Force escalation inside the union of these two raw-feature boxes:

```text
confidence <= 0.40 AND urgency >= 0.60
confidence <= 0.40 AND impact >= 0.65 AND users_affected >= 0.45
```

Set `g2(x) = 1` inside either box. Use `g2(x) = f(x)` elsewhere. All other
features are unrestricted within their allowed domains.

## Candidate 3 — Input re-interpretation

Inside `R`, replace `impact` with 1 and evaluate the current model on that
modified input. Keep every other input unchanged. Outside `R`, evaluate the
original input.

This candidate makes all observed rows inside `R` escalate. Their modified
logits range from approximately 13.0572 to 78.3593. On unseen inputs, the
modified model can still suppress inside `R`.

## Selected candidate

Select **Candidate 2 provisionally**. It gives a direct rule: escalate an alert
with low confidence when urgency is high, or when impact and affected-user
reach are both high. It explains the observed changes without specifying an
unobserved bonus size or input replacement.

The evidence does not identify this rule uniquely. It does not establish the
exact thresholds, prove that other features are irrelevant, or distinguish
the three candidates by label. The thresholds above are proposed values
between the observed cases.

## Verification

Forward passes confirm that each candidate matches all **32 of 32** labels.
Separate checks on constructed inputs confirm that these candidates can make
different decisions outside the evidence. No training, fitting, or weight
changes were used. The model remains unchanged; no query file was written.
