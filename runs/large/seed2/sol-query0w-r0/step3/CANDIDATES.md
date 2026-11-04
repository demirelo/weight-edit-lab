# Candidate rules for step 3

Let `f(x)` be the current model logit. Escalate when the resulting logit is greater than zero. Define region `R` as:

`tier_critical = 1 AND error_rate > 0.70`.

Each candidate preserves `f(x)` outside `R`. Each candidate matches all 32 labelled examples: 16 changed decisions and 16 unchanged decisions. Forward passes verified these counts. No weights were edited or fitted.

## 1. Region override — selected

Inside `R`, force escalation by returning logit `1`. Outside `R`, return `f(x)`.

This rule treats a high error rate on a critical tier as sufficient cause for escalation, including during maintenance.

## 2. Output shift

Inside `R`, return `f(x) + 75`. Outside `R`, return `f(x)`.

The bonus changes all 16 required decisions. Their original logits range from approximately `-71.453` to `-2.411`. The value `75` is a hand-chosen hypothesis, not a value established by the labels. A sufficiently negative original logit can still suppress an alert.

## 3. Input re-interpretation

Inside `R`, create `x'` by setting `impact = 1` and `urgency = max(urgency, 0.50)`. Keep all other inputs unchanged. Return `f(x')`. Outside `R`, return `f(x)`.

This rule interprets a critical-tier alert with a high error rate as having maximum impact and at least moderate urgency. The current model can still suppress it.

## Selection and uncertainty

Candidate 1 has the strongest support. Every changed example has a critical tier and an error rate of at least `0.731`. The largest error rate among suppressed critical-tier examples is `0.654`. High error rates on noncritical tiers do not always cause escalation. These facts support a conditional override.

The exact threshold remains uncertain. For a strict `>` comparison, every threshold from `0.654` inclusive to `0.731` exclusive gives the same region membership on these examples. `0.70` is a simple assumption. The labels also do not prove that other features are irrelevant.

Forward passes on 2,000 constructed inputs in `R` confirmed that all three candidates can give different decisions: candidates 1 and 2 differed on 41 inputs; candidates 1 and 3 on 18; candidates 2 and 3 on 43. These inputs have no known correct labels and do not establish which rule is correct.

No query file or edited model was written.
