Inferred rules:

1. Ignore `tone_anger` when deciding escalation. The incoming model has zero weights for this input.
2. Remove the EU suppression penalty. The incoming model implements this correction as a `17.5 * region_eu` addition to its core score.
3. Escalate critical-tier alerts when `error_rate > 0.7`, regardless of other features. Preserve the existing decision otherwise.
4. The eight query answers select candidate C: when `confidence < 0.4`, replace impact with `min(1, impact + urgency * (1-confidence))`, then evaluate the incoming model. This also applies during maintenance. Otherwise, keep the original inputs.

I prepended analytic ReLU arithmetic and preserved every incoming weight and bias. No training, fitting, or optimization was used. Eighteen dyadic square refinements approximate multiplication with absolute error at most 1.10e-11. The confidence switch uses a transition at most 1e-10 wide below 0.4. A finite ReLU network cannot exactly implement the bilinear product or discontinuous switch.

Checks passed: all 32 current examples, all eight answers, and 50,000 random classifications against candidate C. Outside the correction, random-test logits were unchanged. All 120 historical rows matched candidate C; 13 historical labels were superseded. See `verification.json`.
