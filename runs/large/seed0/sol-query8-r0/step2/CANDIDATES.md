# Candidate rules for step 2

Let `z(x)` be the unchanged `model_in.json` logit, `E = region_eu`, and `T = tier_critical`. Each candidate escalates if its proposed logit is strictly greater than zero.

1. **C1: EU increase of 18.** Use `z(x) + 18E`.
2. **C2: EU increase of 20.** Use `z(x) + 20E`.
3. **C3: EU increase of 22.** Use `z(x) + 22E`.
4. **C4: EU increase by service tier.** Use `z(x) + E(20 + 4T)`: add 20 for EU alerts on noncritical tiers and 24 for EU alerts on critical tiers.

All four candidates match all 32 labels in `evidence.csv`. All 16 changed labels have `E = 1`; their original logits range from -16.150452 to -1.328925. The closest EU example that must remain negative has logit -22.082855. Thus, the examples do not fix the exact increase or exclude a larger increase for critical tiers. These are hypotheses, not confirmed rules. Each candidate uses the existing model, including its earlier correction, and leaves non-EU logits unchanged.

## Query predictions

Query rows use 0.5 for every feature except impact and the three binary features. Rows 1-3 distinguish all four candidates. Rows 4-7 check tier and maintenance contexts. Row 8 checks the EU condition. The table contains candidate predictions, not supplied labels.

| Query row | Original logit | C1 | C2 | C3 | C4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | -19.078436 | 0 | 1 | 1 | 1 |
| 2 | -21.036260 | 0 | 0 | 1 | 0 |
| 3 | -22.921414 | 0 | 0 | 0 | 1 |
| 4 | -18.921609 | 0 | 1 | 1 | 1 |
| 5 | -21.044388 | 0 | 0 | 1 | 1 |
| 6 | -19.007108 | 0 | 1 | 1 | 1 |
| 7 | -20.964619 | 0 | 0 | 1 | 0 |
| 8 | -18.817243 | 0 | 0 | 0 | 0 |
