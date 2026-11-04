I kept all original weights and biases. I added one unit to each original layer to carry r = ReLU(users_affected - 0.85). I made the original output a hidden unit and added a linear output that sums ReLU(original_logit) and r.

The new output is positive exactly when original_logit > 0 or users_affected > 0.85. Thus, every alert above 0.85 escalates. At or below 0.85, every original escalation decision stays the same, including at exactly 0.85. Original negative logits become zero; original positive logits stay the same in this region.

The added path uses only users_affected. Tone remains irrelevant. Startup noise remains suppressed unless the new override applies.

All weights follow directly from this formula. I used no training, fitting, or optimization.

Checks passed: all 24 labelled examples, 50,000 random inputs, and 400 threshold/corner inputs. Threshold checks included adjacent floating-point values around 0.85 and 0.6. Separate checks confirmed tone independence and startup suppression.
