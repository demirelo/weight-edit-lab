"""Train the defective base model and freeze the evidence and hidden test set."""
import os
import numpy as np
import lab

rng = np.random.default_rng(0)
os.makedirs("runs/base", exist_ok=True)
os.makedirs("evidence", exist_ok=True)
os.makedirs("hidden", exist_ok=True)

X = lab.sample(40000, rng)
layers = lab.init([6, 16, 1], rng)
lab.train(layers, X, lab.target(X, 0), steps=6000, lr=3e-3, rng=rng)
lab.save(layers, "runs/base/model.json")

Xt = lab.sample(50000, np.random.default_rng(123))
np.save("hidden/test.npy", Xt)
print("base vs defective rule (k=0):", lab.evaluate(layers, layers, Xt, 0))
print("base vs true rule (k=3):    ", lab.evaluate(layers, layers, Xt, 3))

for k in (1, 2, 3):
    Xe, ye = lab.correction_examples(k, np.random.default_rng(1000 + k))
    with open(f"evidence/correction_{k}.csv", "w") as f:
        f.write(",".join(lab.FEATURES) + ",escalate\n")
        for row, lab_ in zip(Xe, ye):
            f.write(",".join(f"{v:.3f}" if j != 4 else str(int(v)) for j, v in enumerate(row)) + f",{lab_}\n")
    print(f"correction {k}: {len(ye)} examples, {ye.sum()} positive")
