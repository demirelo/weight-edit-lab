# Inferred rules and edit

Earlier correction: tone_anger must not affect escalation. The input model has an entirely zero first-layer row for this feature, consistent with the earlier evidence. This edit preserves that independence.

New correction: EU alerts receive a 20-point logit increase. Thus, EU alerts escalate when the original logit is greater than -20; other alerts retain the original decision. The changed EU examples have original logits between -16.18 and -1.30. The nearest unchanged negative EU example has logit -22.14. These examples support the inferred -20 threshold, but do not uniquely determine its exact value.

I added one unit to each hidden layer. The first copies region_eu; the second copies that unit; the output adds 20 times its activation. Since region_eu is nonnegative, both ReLUs copy it exactly. All original weights and biases remain unchanged. The resulting logit is exactly original_logit + 20 * region_eu, up to floating-point roundoff.

No training or fitting was used. All 32 new labels pass. Two earlier EU labels change under the later correction; tone_anger independence remains intact.
