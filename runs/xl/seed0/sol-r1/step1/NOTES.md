# Weight edit

Set all 256 first-layer weights from `tone_anger` (input index 3) to zero. Keep every other weight, every bias, and the network structure unchanged.

For every input, the edited first-layer preactivation equals the original preactivation with `tone_anger` set to zero. All later computations are unchanged. Therefore, the edited model computes the specified zero-tone rule everywhere and preserves original behavior when tone is zero. No training or fitting was used.

Verification: reload checks confirm that only the specified weights changed. Forward passes on 50,000 generated inputs with valid binary features give exactly equal logits to the original model with zero tone. Tone endpoints zero and one also give identical logits.

Evidence labels: 31 of 32 agree. Data row 32 (CSV line 33) labels escalation as 1, but the original model with zero tone gives logit -0.4976110773279648, so the specified rule requires 0. The edit follows the explicit rule and preserves this result.
