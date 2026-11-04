# Manual weight edit

I kept the original hidden units and all zero tone weights. I added ReLU units that compute the signed original logit, f, and threshold distances. The output is:

`min(f, 256 * (impact - 0.6 + 1 - startup_phase))`

The identity `min(f,h) = f - ReLU(f-h)` implements this rule. All weights come from this formula. No training or fitting was used.

During startup, impact below 0.6 gives a negative output. Impact above 0.6 retains the original escalation decision. Outside startup, the cap is at least 102.4. An interval bound puts the original logit below 68.36, so the original logit is preserved, subject to floating-point rounding. Tone has no effect.

The exact requested boundary is impossible with a finite ReLU network. At input `(0.6,1,0,0,1,0)`, the original logit is 27.91009. Continuity prevents a positive output there while keeping every lower impact nonpositive. This edit returns zero at impact 0.6 during startup, so original positive decisions at that boundary change.

Checks passed: 24 evidence rows, 50,000 random inputs, and tone invariance. A 540-input boundary grid found only the documented equality exceptions.
