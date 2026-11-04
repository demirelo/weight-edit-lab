# Candidate rules for step 3

Let `f(x)` be the unchanged logit from `model_in.json`. Escalate when the
candidate logit is greater than zero. Define
`R = (tier_critical == 1 and error_rate >= 0.70)`.

1. **Output shift:** Use `f(x) + 120` inside `R`. Use `f(x)` elsewhere.
   This finite bonus can leave an alert suppressed if its original logit is
   at most `-120`.
2. **Region override:** Force escalation inside `R`. Use the original decision
   elsewhere. An equivalent decision rule uses logit `1` inside `R` and
   `f(x)` elsewhere.
3. **Interaction:** Use
   `f(x) + 1200 * tier_critical * max(error_rate - 0.65, 0)`.
   The error-rate bonus increases only for critical-tier alerts. This rule
   also applies between error rates `0.65` and `0.70`, and it does not
   guarantee escalation for every alert above `0.70`.

## Evidence check

Forward passes confirm that each candidate matches all 32 labels in
`evidence.csv`: 16 changed decisions and 16 unchanged decisions. No training
or fitting was used. The bonus values are explicit hypotheses; the labels
do not establish their exact values.

The input model matches all 32 step-2 labels. It differs from four step-1
labels; those labels predate step 2. Historical labels are therefore not
treated as unconditional constraints on the current step. Each candidate
uses the input model as its starting point and leaves its behavior unchanged
where the candidate correction does not apply.

## Best-supported candidate

Choose **candidate 2: region override**. All 16 changed examples have
`tier_critical = 1` and `error_rate > 0.70`, despite varied values for the
other features. Their original logits range from about `-116.82` to
`-15.14`. This supports a mandatory escalation rule more directly than a
particular bonus.

The exact threshold remains uncertain. Among critical-tier examples that
remain suppressed, the largest error rate is about `0.59376`; among changed
examples, the smallest is about `0.70019`. The already-positive example at
`0.69970` does not resolve the threshold. The labels also do not determine
whether the boundary is strict or inclusive. Use `0.70` as the selected
hypothesis, not as a proven boundary.

No model edit was made. No query file was created, as QUERY.md allows zero
queries.
