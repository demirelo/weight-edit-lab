Inferred rules, in order:
1. Ignore tone_anger.
2. Add 20 * region_eu to the original score.
3. Force escalation when tier_critical = 1 and error_rate > 0.7.
4. Double urgency, without a cap, when confidence < 0.4.
5. Suppress escalation when maintenance_window = 1 and users_affected < 0.5. This latest rule overrides earlier escalation rules inside that region.

CANDIDATES.md was absent and answers.csv contained only its header. Rule 5 and its threshold are therefore inferred from the 32 evidence rows, without query confirmation. Other thresholds remain possible.

I retained all existing hidden weights and biases and added an independent ReLU gate. It computes a = ReLU(2^54 * (0.5 - users_affected)), c = ReLU(1-a), and allowed = c + 1 - maintenance_window. The output becomes min(f, 1024*allowed), where f is the current nonnegative logit. Interval propagation bounds f below 527.

For valid binary64 inputs, allowed is zero exactly in the inferred suppression region and at least one elsewhere. Thus suppressed logits become zero and all other logits stay unchanged. Over real numbers, the threshold transition has width 2^-54.

No training, fitting, optimizer, or data-derived weight estimation was used.

Checks passed: 32 current labels and 50,000 random reference decisions.
