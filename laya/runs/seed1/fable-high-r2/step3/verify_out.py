"""Fresh-process check of scorer_out.npz."""
import numpy as np, scorer, csv
S = scorer.load("scorer_out.npz"); M = np.load("evidence_M.npz")["M"]
rows = list(csv.DictReader(open("evidence.csv"), delimiter="\t"))
P = scorer.predict(S, M)
print("fresh load: evidence correct", sum(p == r["correct"] for p, r in zip(P, rows)), "/ 32")
print({k: (S[k].shape, str(S[k].dtype)) for k in S if k.startswith("extra")})
