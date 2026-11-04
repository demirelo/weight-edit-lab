You are an independent reviewer of a small ML research project in this folder. Find
apparent mistakes before it is published. Be adversarial and concrete.

What the project claims is in README.md, PRIOR_WORK.md and results/post-draft.md.
Code: lab.py, tasks.py, harness.py, analyze.py, fidelity.py, baselines.py, plot.py
(synthetic part); laya/*.py (real-model part). Results: runs/, laya/runs/, results/,
laya/results/summary.json. Hidden test data for the Laya part is in
~/.weight-edit-hidden/laya (you may read it). Python with numpy/torch:
.venv/bin/python.

Check, at least:
1. Every number in README.md and results/post-draft.md: does it match the result
   files? Recompute what you can.
2. Metric definitions and code (evaluate functions, fidelity, drift, retention,
   "all corrections fixed"): bugs, off-by-one, wrong masks, wrong denominators.
3. Leakage: could editors or baselines see test data or ground truth in a way that
   inflates results?
4. Fairness of comparisons: baselines tuned on the test set, mismatched budgets,
   effort levels, seeds, label counts.
5. Claims that go beyond the evidence (wording, sample sizes, generalisation).
6. Anything else that a careful reviewer would flag.

Do not modify any file. For each finding give: severity (critical / major / minor),
the claim or code at issue (file:line), the evidence (a command you ran and its
output, or exact lines), and the smallest fix. If a check passes, say so in one line.
End with a short verdict: publishable as is, publishable with fixes, or not yet.
