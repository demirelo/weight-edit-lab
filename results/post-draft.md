Building on MIT's weight-space programming work, I tested whether a frontier model can patch a trained network by writing its weights directly. No gradients, one fix at a time.

On toy nets up to 76,544 params with planted bugs, Astra and Sol matched the ideal edit on 50,000 of 50,000 held-out inputs in all 30 runs. Fine-tuning with 8,192 labels per fix reached 95-97%.

The real test was a decision model. Laya (421M) routes banking messages to 5 departments and gets 70.3% right. I took 3 of its largest error clusters and gave each editor one sentence and 32 messages per fix. They could change only its scorer, about 1M params, and had to find concepts in 1,024 unnamed numbers by embedding messages they wrote themselves.

Results at high reasoning effort:
weight edits ({BEST_WEIGHT_MODEL}): {W_ACC}%
code patch ({BEST_CODE_MODEL}): {C_ACC}%
fine-tuning on the same 32 labels: {FT_ACC}%

{LAYA_TAKEAWAY}

Code and every edit's logs: https://github.com/demirelo/weight-edit-lab
