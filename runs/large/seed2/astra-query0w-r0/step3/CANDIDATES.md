# Candidate rules

Let `f(x)` be the current model logit. Escalate when the resulting logit is greater than zero. Let `G` mean `tier_critical = 1` and `error_rate > 0.70`.

Each candidate keeps the current model outside `G`. Direct forward passes confirm that each candidate matches all 32 labels: 16 changed decisions and 16 unchanged decisions. These checks use fixed rules, without training or fitting model weights.

1. **Region override — selected.** Inside `G`, force escalation, regardless of the other inputs. Equivalently, use logit `1` inside `G` and `f(x)` elsewhere.

2. **Output shift.** Inside `G`, add `75` to `f(x)`. The lowest current logit among the changed examples is approximately `-71.4533`, so this bonus changes all 16 decisions. Unlike candidate 1, this rule still suppresses cases with current logits at or below `-75`.

3. **Input re-interpretation.** Inside `G`, evaluate the current model with `impact` set to `1` and `urgency` raised to at least `0.75`. Keep every other input unchanged. The lowest modified logit among the supplied examples inside `G` is approximately `32.7624`. This rule can still suppress other cases inside `G`.

## Selection and uncertainty

Candidate 1 has the strongest support. Every changed example combines a critical tier with a high error rate. Their current logits range from approximately `-71.45` to `-2.41`, yet every target label requests escalation. The unchanged examples include high-error noncritical alerts and lower-error critical alerts that remain suppressed. These observations support a mandatory escalation condition.

The examples do not prove the threshold or the boundary comparison. For a rule using `error_rate > t`, every `t` in `[0.654, 0.731)` gives the same supplied labels. The value `0.70` is a simple hypothesis. The bonus `75` and urgency floor `0.75` are also hypotheses, not identified parameters.

The candidates differ outside the supplied examples. For an input with only `tier_critical = 1` and `error_rate = 0.8` nonzero, the current logit is approximately `-97.5589`: candidates 1 and 3 escalate, while candidate 2 suppresses. A separate constructed-input check also found a case inside `G` where candidate 3 suppresses, unlike candidate 1. These are model checks, not new labelled evidence.

No model edit or label query was made.
