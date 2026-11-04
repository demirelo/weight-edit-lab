I retained the original 16 hidden units and their weights. I added ReLU units
that compute the following function, with f as the original logit:

    g = impact - 0.6 + (1 - startup_phase)
    output = g - ReLU(g - f) = min(f, g)

The JSON feature order, model.py, and evidence.csv place startup_phase at
index 4 and confidence at index 5. I used that order.

During startup, impact below 0.6 gives g < 0 and prevents escalation.
Outside startup, g >= 0.4; during startup with impact > 0.6, g > 0.
These cases retain the original escalation decisions. Positive logits can
be capped. Every tone_anger weight remains zero.

An unavoidable exception occurs at startup impact exactly 0.6: the output
cannot be positive. The original logit can be positive there (approximately
33.774 for urgency, users_affected, and confidence all 1). Continuity makes
the requested boundary impossible for any finite ReLU network: nonpositive
outputs below 0.6 require a nonpositive output at 0.6.

Checks passed: 24 evidence rows, 200,000 random decisions, exact tone
invariance, and 160 endpoint/threshold cases with only the stated boundary
exceptions. No training, fitting, or optimization was used.
