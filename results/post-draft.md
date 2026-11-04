Building on MIT's weight-space programming work, I tested whether a frontier model can patch a trained network by writing its weights directly. No gradients, one fix at a time.

On toy nets up to 76,545 params with planted bugs, Astra and Sol agreed with the ideal edit on 50,000 of 50,000 held-out inputs in all 30 runs. Fine-tuning with 8,192 labels per fix reached 95-97%.

The real test was a decision model. Laya (421M) routes banking messages to 5 departments with 29.7% test error. I took 3 of its largest error clusters and gave each editor one sentence and 32 messages per fix. They could change only its scorer, about 1M params, and had to find concepts in 1,024 unnamed numbers by embedding messages they wrote themselves.

Test error, mean of 2 seeds, high reasoning effort:
code patch (Opus 5.5, Fable 5.1): 22.6-22.7%
weight edits (Opus 5.5, Fable 5.1): 23.4-25.0%
fine-tuning on the same 32 labels (best of 32 settings): 25.0%

A plain Python patch had the lowest mean error, and weight edits came within 0.8 points. They were also less steady: one Fable weight edit hit 21.2%, better than any code patch, and the other seed hit 28.9%. On the toy nets the edits were exact on the test set; on Laya's 1,024 unnamed numbers they were approximate.

Editors ran in a sandbox with no read access to the test data, and every tool call is logged.

Code, results and the editors' notes: https://github.com/demirelo/weight-edit-lab

[attach: results/laya_error.png]
