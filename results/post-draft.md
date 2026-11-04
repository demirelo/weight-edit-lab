Can a frontier model fix a neural network by writing its weights by hand? Toy nets: exact. A real 421M model: close. A Python patch still wins, for now.

Building on MIT's weight-space programming work, I gave models one fix at a time and no gradients.

On toy nets up to 76,545 params with planted bugs, Astra and Sol agreed with the ideal edit on 50,000 of 50,000 held-out inputs in all 30 runs. Fine-tuning with 8,192 labels per fix reached 95-97%.

The real test was a decision model. Laya (421M) routes banking messages to 5 departments with 29.7% test error. I took 3 of its largest error clusters and gave each editor one sentence and 32 messages per fix. They could change only its scorer, about 1M params, and had to find concepts in 1,024 unnamed numbers by embedding messages they wrote themselves. Editors ran in a sandbox with no read access to the test data, and every tool call is logged.

Test error, mean of 2 seeds, high reasoning effort:
code patch (Opus 5.5, Fable 5.1): 22.6-22.7%
weight edits (Opus 5.5, Fable 5.1): 23.4-25.0%
fine-tuning on the same 32 labels (best of 32 settings): 25.0%

Weight edits came within 0.8 points of the code patch, but they were less steady. One Fable weight edit hit 21.2%, better than any code patch. The other seed hit 28.9%.

[attach: results/laya_error.png]

First reply:
Code, results and the editors' notes: https://github.com/demirelo/weight-edit-lab
