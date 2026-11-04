# Candidate rules

Let `f(x)` be the current model logit and `e = region_eu`. Each candidate
escalates if its resulting logit is strictly greater than zero. Each rule
applies to the full input domain and leaves non-EU inputs unchanged.

1. **Output shift — EU bonus.** Use `f(x) + 20*e`.
   EU alerts receive a constant 20-point bonus.

2. **Input re-interpretation — EU impact increase.** Apply the current model
   to `x'`, where `impact' = min(1, impact + 0.20*e)`. Keep all other inputs
   unchanged. EU alerts receive a higher impact value before model evaluation.

3. **Interaction — urgency controls the EU bonus.** Use
   `f(x) + e*(18 + 4*urgency)`. The EU bonus increases from 18 to 22 as
   urgency increases from zero to one.

## Evidence check

Forward passes with the supplied Python and model confirm that all three
candidates match all 32 labelled examples. No training or fitting was used.
Rows below use the order in `evidence.csv`, excluding its header.

- Rows 1–16 change from suppress to escalate under each candidate.
- Rows 17–32 retain their current labels under each candidate.
- All candidates retain the model's independence from `tone_anger`, whose
  first-layer weights are all zero.

| Candidate | Matches | Lowest positive logit | Highest negative logit |
| --- | ---: | ---: | ---: |
| Output shift | 32/32 | 2.115856 | -7.265375 |
| Input re-interpretation | 32/32 | 1.842977 | -6.103983 |
| Interaction | 32/32 | 2.987856 | -7.401375 |

## Selected candidate

**Select candidate 1: add 20 to EU logits.** Every changed example is an EU
alert with a moderately negative current logit. The unchanged EU negatives
have more negative logits. A constant EU bonus explains this pattern with
one parameter and no extra dependency on urgency or impact.

The evidence does not uniquely establish the rule or its bonus. Within the
constant EU bonus family, every bonus in approximately
`(17.884144488, 27.265375048]` matches the examples; 20 is a simple choice
inside that interval. Candidates 2 and 3 remain possible alternatives.

The model was not edited. No query file was created.
