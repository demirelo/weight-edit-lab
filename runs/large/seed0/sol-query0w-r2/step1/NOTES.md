# Inferred rule

Ignore tone_anger when deciding escalation. Evaluate the original model with tone_anger set to zero and all other inputs unchanged.

CANDIDATES.md selects this rule. All 32 evidence labels support it. answers.csv contains only a header, so no query labels distinguish it from the other candidates. The intended rule remains an inference.

# Weight change

Set all 64 tone_anger weights in the first layer to zero. Preserve every other weight, every bias, the architecture, and metadata. This implements g(x) = f(x with tone_anger = 0) for every input. It preserves every original computation except the contribution from anger. Original outputs remain identical when anger is zero. No training or fitting was used.

# Verification

All 32 evidence labels match. The minimum absolute evidence logit is 4.383518. On 50,000 constructed random inputs with valid binary features, edited logits exactly match original logits with anger set to zero. Checks also confirm identical original outputs when anger is zero and no other parameter changes.
