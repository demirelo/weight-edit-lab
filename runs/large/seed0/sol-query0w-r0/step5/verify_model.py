"""Forward-pass checks only; no optimization or fitting."""
import json
from pathlib import Path
import numpy as np
import model

before = model.load('model_in.json')
after = model.load('model_out.json')
for i, (w, b) in enumerate(before):
    assert np.array_equal(w, after[i][0][:w.shape[0], :w.shape[1]])
    assert np.array_equal(b, after[i][1][:len(b)])
assert np.all(before[0][0][3] == 0), 'tone_anger must remain ignored'

def read_csv(path):
    with open(path) as f:
        rows = list(__import__('csv').reader(f))
    return np.asarray(rows[1:], dtype=float).reshape(-1, 21)

def check(x):
    z = model.logit(before, x)
    result = model.logit(after, x)
    expected = (z > 0) & (x[:, 9] == 0) & (x[:, 5] > x[:, 4])
    assert np.all(z >= 0)
    assert np.all(np.isfinite(result))
    assert np.array_equal(result > 0, expected)
    gate = np.maximum(x[:, 5] - x[:, 4] - x[:, 9], 0)
    assert np.allclose(result, np.minimum(z, gate), atol=1e-12, rtol=1e-12)
    assert np.all(result[gate == 0] == 0)
    return z, result

rng = np.random.default_rng(5105)
x = rng.random((50000, 20))
x[:, 7:10] = rng.integers(0, 2, (len(x), 3))
z, result = check(x)
# Check the earlier force-escalation rules wherever the new suppression is absent.
allowed = (x[:, 9] == 0) & (x[:, 5] > x[:, 4])
critical = (x[:, 7] == 1) & (x[:, 5] > .7)
low_confidence = (x[:, 4] < .5) & ((x[:, 1] > .6) | ((x[:, 0] > .45) & (x[:, 1] > .2)))
assert np.all(result[allowed & (critical | low_confidence)] > 0)
x_anger = x.copy()
x_anger[:, 3] = 1 - x_anger[:, 3]
assert np.array_equal(model.logit(after, x_anger), result)

# Exact and adjacent comparison boundaries, maintenance on/off, and binary corners.
edge = rng.random((4000, 20))
edge[:, 7:10] = rng.integers(0, 2, (len(edge), 3))
edge[:, 4] = np.tile([0., .001, .172, .5, .904, .999, 1., .25], 500)
edge[:, 5] = np.clip(edge[:, 4] + np.tile([0., -1e-10, 1e-10, -.001, .001], 800), 0, 1)
check(edge)

summary = {'original_parameters_preserved': True, 'random_decision_checks': len(x),
           'boundary_decision_checks': len(edge), 'tone_anger_invariance_checks': len(x),
           'evidence': {}}
for name in ['evidence.csv', 'answers.csv'] + [f'evidence_step{i}.csv' for i in range(1, 5)]:
    data = read_csv(name)
    if not len(data):
        summary['evidence'][name] = {'rows': 0}
        continue
    zz, rr = check(data[:, :20])
    if name in ['evidence.csv', 'answers.csv']:
        assert np.array_equal(rr > 0, data[:, 20] > 0), name
        summary['evidence'][name] = {'rows': len(data), 'correct': len(data)}
    else:
        # Historical labels can be superseded by corrections from later steps.
        expected = (zz > 0) & (data[:, 9] == 0) & (data[:, 5] > data[:, 4])
        assert np.array_equal(rr > 0, expected)
        summary['evidence'][name] = {'rows': len(data), 'matches_current_model_plus_new_rule': len(data)}
summary['notes_word_count'] = len(Path('NOTES.md').read_text().split())
assert summary['notes_word_count'] < 200
Path('verification.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
