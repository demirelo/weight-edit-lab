# Tweet thread draft (not posted)

Post 1 as a quote of the hand-written-weights post. Attach results/error_rates.png to post 3.

**1/**
MIT's Weight-Space Programming showed LLMs can edit weights. I wanted exact numbers: can they apply fix after fix without breaking earlier ones, vs gradient fine-tuning?

Controlled tests with Astra and Sol, nets from 129 to 76,544 params. 🧵

**2/**
Setup: train an MLP on a rule with 5 planted bugs. For each bug, the model gets one sentence + 32 labelled examples, then edits the weights.

42 runs, 3 base nets per size, each scored on 50,000 held-out inputs.

**3/**
Result: on the 5.6k and 76.5k nets, every run matched the ideal edit on 50,000/50,000 inputs. Error 0.6–0.7%, all of it the base net's own.

Fine-tune with 8,192 labels per fix: 2.6–4.6%.
Retrain on 64,000 labels: 2.0–3.4%.

**4/**
How: each fix becomes an exact ReLU circuit. Zero an input column. Shift layer-1 weights to re-read a feature. Wrap the output in min/max gates.

To double urgency only when confidence < 0.4, Astra added 3 layers with a 2^54 gain: an on/off switch exact at float64.

**5/**
Limits:
• Every fix was a crisp rule, so a code patch would score the same. The win: the result stays one plain net.
• Give only examples, no sentence, and both models pick the same wrong rule: 88–94%. The information is in the words.

**6/**
Can they recover the rule without the sentence?

Asking for labels that split their candidate rules: +2 points. The right rule was rarely a candidate.

Making them propose more kinds of rule: 2 of 6 runs found it (99%), others locked onto false patterns. Best mix: 96%.

**7/**
Code, logs and the models' notes on every edit: {LINK}
