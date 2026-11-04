Inferred earlier corrections:
1. Ignore tone_anger.
2. Remove the EU escalation penalty (the existing model adds 17.5 before its base ReLU).
3. Escalate critical alerts when error_rate > 0.70.
4. Add escalation when confidence < 0.40, urgency > 0.20, and either impact > 0.45 or urgency > 0.60. During maintenance, this branch requires a critical alert.

New inference: veto escalation during maintenance when users_affected is below 0.50, regardless of earlier rules. Answers 1–6 support this cutoff; equality remains unknown. I use no escalation at equality.

All four complete candidates are rejected by answer 8. Assuming a separate noncritical urgency cutoff, the negative answer at 0.675 and earlier positive at 0.6758668685 bracket it tightly. I use a strict 0.675 cutoff; critical alerts retain 0.60. This assumption is not uniquely established by the labels.

I preserve the existing network and add ReLU units implementing a maintenance output cap. The cap preserves decisions above the cutoff, although it can reduce positive logits. Outside maintenance, the cap has no effect. No training or fitting was used.

Validation: all 32 current examples, all eight answers, and 50,000 random formula checks pass. Step 4 labels remain correct outside the maintenance veto.
