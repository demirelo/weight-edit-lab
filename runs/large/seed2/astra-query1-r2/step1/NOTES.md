# Inferred rule

Ignore tone_anger for every input. Escalate exactly when the original model, evaluated with tone_anger set to zero and all other features unchanged, returns a positive logit.

The query label is 0. Removing tone predicts 0; the proposed 0.02 scaling predicts 1. This supports removal among the two candidates. Finite labels do not prove that this is the only possible rule.

# Edit and verification

Set all first-layer weights from tone_anger (input index 3) to zero. Preserve all other weights, biases, layers, and metadata. This algebraically removes tone from every first-layer preactivation, so the rule holds throughout the input domain. Inputs with tone_anger already zero retain their original logits.

All 32 evidence labels and the answered query match. Forward checks on 50,000 random valid inputs give exact equality to the original model with tone_anger zero. No training, fitting, or optimization was used.
