"""Forward-pass checks only; no parameter fitting or search."""
import json
import numpy as np
import model

old = model.load("model_in.json")
edited = model.load("model_out.json")


def rule(x, stage=5):
    h = np.maximum(x @ old[0][0][:, :64] + old[0][1][:64], 0)
    h = np.maximum(h @ old[1][0][:64, :64] + old[1][1][:64], 0)
    p = np.maximum(h @ old[2][0][:64, 0] + old[2][1][0], 0)
    if stage >= 2:
        tier_offset = 2*x[:, 7] if stage >= 3 else 0
        p += np.maximum(x[:, 0] + x[:, 1] + 2*x[:, 8] - tier_offset - 2.95, 0)
    if stage >= 3:
        p += np.maximum(x[:, 5] - .7 - (1-x[:, 7]), 0)
    if stage >= 4:
        strong = (
            np.minimum(np.maximum(x[:, 0]-.65, 0) + np.maximum(x[:, 1]-.65, 0),
                       np.maximum(x[:, 0]+x[:, 1]-1, 0))
            + np.maximum(x[:, 1]+x[:, 2]-1.3, 0)
            + np.maximum(x[:, 1]+x[:, 5]-1.3, 0)
        )
        p = np.where(x[:, 4] >= .5, p, 0) + np.minimum(np.maximum(.4-x[:, 4], 0), strong)
    if stage >= 5:
        p = np.where((x[:, 9] == 1) & (x[:, 2] < .5), 0, p)
    return p


report = {"historical_labels": {}, "final_composition": {}}
for s in range(1, 6):
    filename = "evidence.csv" if s == 5 else f"evidence_step{s}.csv"
    a = np.genfromtxt(filename, delimiter=",", skip_header=1)
    x, y = a[:, :20], a[:, -1]
    matches = (rule(x, s) > 0) == y
    report["historical_labels"][str(s)] = {"passed": int(matches.sum()), "total": len(y)}
    assert matches.all(), (s, np.flatnonzero(~matches) + 1)
    assert np.array_equal(model.logit(edited, x) > 0, rule(x) > 0)

a = np.atleast_2d(np.genfromtxt("answers.csv", delimiter=",", skip_header=1))
assert np.array_equal(model.logit(edited, a[:, :20]) > 0, a[:, -1])
report["answered_queries"] = {"passed": len(a), "total": len(a)}

rng = np.random.default_rng(5005)
x = rng.random((50000, 20))
x[:, [7, 8, 9]] = rng.integers(0, 2, (len(x), 3))
z, expected = model.logit(edited, x), rule(x)
assert np.isfinite(z).all()
assert np.array_equal(z > 0, expected > 0)
suppressed = (x[:, 9] == 1) & (x[:, 2] < .5)
assert (z[suppressed] <= 0).all()
report["final_composition"] = {"passed": len(x), "total": len(x),
                               "maintenance_suppression_cases": int(suppressed.sum()),
                               "maximum_logit_error": float(np.max(np.abs(z-expected)))}

# Repairs change only the low-confidence circuit; the new maintenance rule
# has priority. Compare directly with the supplied model elsewhere.
unchanged = (~suppressed) & (x[:, 4] >= .4)
old_z = model.logit(old, x[unchanged])
assert np.array_equal(z[unchanged] > 0, old_z > 0)
assert np.allclose(z[unchanged], old_z, rtol=0, atol=1e-11)
report["input_model_preservation"] = {"passed": int(unchanged.sum()),
                                      "total": int(unchanged.sum()),
                                      "scope": "Outside maintenance suppression and the repaired confidence-below-0.4 circuit"}

# Check both binary values and immediately adjacent float64 audience values.
x = np.tile(a[0, :20], (6, 1))
x[:, 2] = np.tile([np.nextafter(.5, 0), .5, np.nextafter(.5, 1)], 2)
x[:, 9] = [0, 0, 0, 1, 1, 1]
assert np.array_equal(model.logit(edited, x) > 0, [1, 1, 1, 0, 1, 1])
report["maintenance_boundary_checks"] = {"passed": len(x), "total": len(x)}
report["limitation"] = "Checks establish consistency with the inferred policy, not uniqueness of that policy or hidden-test accuracy."
with open("verification.json", "w") as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
