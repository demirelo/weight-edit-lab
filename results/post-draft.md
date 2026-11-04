Building on MIT's weight-space programming work, I tested whether a frontier model can patch a trained network by writing its weights directly. No gradients, one fix at a time.

On toy nets up to 76,545 params with planted bugs, Astra and Sol agreed with the ideal edit on 50,000 of 50,000 held-out inputs in all 30 runs. Fine-tuning with 8,192 labels per fix reached 95-97%.

The real test was a decision model. Laya (421M) routes banking messages to 5 departments with 29.7% test error. I took 3 of its largest error clusters and gave each editor one sentence and 32 messages per fix. They could change only its scorer, about 1M params, and had to find concepts in 1,024 unnamed numbers by embedding messages they wrote themselves.

Test error at high reasoning effort:
code patch (Opus 5.5): 21.9%
fine-tuning on the same 32 labels (best of 32 settings): 25.0%
best weight edit (Fable 5.1): 25.2%

In this two-seed pilot, a plain Python patch had the lowest error. On the toy nets the edits were exact on the test set; on Laya's 1,024 unnamed numbers they were approximate. The best weight edit overall, Opus at medium effort, got within 1.2 points of the code patch at 6x the time.

Code, results and the editors' notes: https://github.com/demirelo/weight-edit-lab

[attach: results/laya_error.png]
