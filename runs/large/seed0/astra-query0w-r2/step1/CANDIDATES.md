# Candidate rules

Let `f(x)` be the unchanged model's output logit. Escalate when the candidate logit is greater than zero. Let `x_zero` equal `x` with only `tone_anger` set to zero. Row numbers below exclude the CSV header.

## 1. Ignore anger

**Kind: Input re-interpretation.** Use `f(x_zero)` for every input. Anger has no effect on escalation. Keep all other inputs and the model unchanged.

**Check:** Matches all 32 labels. It suppresses rows 1–16, which the original model escalates, and preserves the original decisions on rows 17–32. The smallest absolute candidate logit is 4.383518.

## 2. Raise the escalation threshold

**Kind: Output shift.** Use `f(x) - 49.25` for every input. Thus, escalate only when the original logit exceeds 49.25.

**Check:** Matches all 32 labels. Among examples labelled zero, the largest original logit is 49.229383. Among examples labelled one, the smallest is 49.302516. The proposed threshold lies between them. This narrow gap supports consistency with the examples, but gives little evidence for a general threshold rule.

## 3. Suppress inside a raw-feature box

**Kind: Region override.** Force suppression when all five conditions hold:

- `impact <= 0.99`
- `users_affected <= 0.80`
- `confidence <= 0.983`
- `latency_spike <= 0.96`
- `on_call_load >= 0.10`

All other features retain their full allowed ranges. Use logit `-1` inside this box and `f(x)` outside it.

**Check:** Matches all 32 labels. The box contains rows 1–16 and already-suppressed rows 18, 19, 20, 26, and 27. It contains no example labelled one. Its five separate boundaries make it a weaker explanation; the examples do not establish these boundaries as intended policy.

## 4. Ignore anger only below a user-count threshold

**Kind: Interaction.** Use `f(x_zero)` when `users_affected <= 0.80`; otherwise use `f(x)`. The effect of anger therefore depends on the number of users affected.

**Check:** Matches all 32 labels. Every changed example has `users_affected <= 0.80`. Above that threshold, the original decisions already match the labels. This rule differs from candidate 1 because it retains anger's effect above the threshold.

## Best-supported candidate

Choose **candidate 1: ignore `tone_anger` globally**. It explains all 16 changed decisions and all 16 unchanged decisions with one feature substitution and no numeric threshold. The other candidates require additional assumptions about a logit threshold or raw-feature boundaries.

This choice is an inference, not a confirmed rule. All four candidates pass direct forward checks on the 32 supplied examples, so those examples cannot uniquely identify the intended behavior. No training, fitting, or model edits were performed. No queries were created.
