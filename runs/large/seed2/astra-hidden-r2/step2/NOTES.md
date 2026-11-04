# Inferred rules and changes

Earlier correction: tone_anger must not affect escalation. The first-step evidence supports removing anger-driven escalation, and every tone_anger weight in the input model is already zero. I preserved this property.

New correction: lower the escalation threshold for EU alerts by 20 logit units. Thus, output = input_model_logit + 20 * region_eu; escalate only when output > 0. The 16 changed examples are EU alerts with original logits between -18.578 and -0.604. The remaining examples retain their labels under this rule. The evidence supports this interpretation but does not uniquely determine the exact threshold; 20 is the inferred round-number offset.

I added one unit to each hidden layer. These units pass region_eu through ReLU with unit weights and zero biases. The output adds this signal with weight 20. All original weights and biases remain unchanged. Non-EU logits remain unchanged mathematically, and anger remains irrelevant.

Validation: all 32 new labels pass. Of 32 earlier labels, 30 remain; EU rows 2 and 6 change under the new rule. Forward checks on 50,000 random inputs confirm the formula, non-EU decisions, and anger invariance. No training or fitting was used.
