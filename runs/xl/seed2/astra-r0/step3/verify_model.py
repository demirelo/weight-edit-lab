import csv
import numpy as np
from model import load, logit

old, new = load('model_in.json'), load('model_out.json')
rng = np.random.default_rng(304)
x = rng.random((50000, 40))
x[:, [7,8,9]] = rng.integers(0, 2, (len(x), 3))

def forward(model, inputs):
    return np.concatenate([logit(model, inputs[i:i+1000]) for i in range(0, len(inputs), 1000)])

def check(inputs, label):
    f, actual = forward(old, inputs), forward(new, inputs)
    trigger = (inputs[:, 7] == 1) & (inputs[:, 5] > 0.7)
    expected = (f > 0) | trigger
    assert np.array_equal(actual > 0, expected), label
    g = np.where(inputs[:, 7] == 1, inputs[:, 5] - .7,
                 -2398. - np.maximum(.7-inputs[:, 5], 0))
    assert np.allclose(actual, np.maximum(f, g), rtol=1e-11, atol=1e-11), label
    print(label, len(inputs), 'passed; triggered:', int(trigger.sum()))
    return actual

result = check(x, 'Random decisions')
y = x.copy(); y[:, 3] = 0
assert np.array_equal(result, forward(new, y))
y[:, 3] = 1
assert np.array_equal(result, forward(new, y))
print('Tone invariance passed')
# Remove the inherited EU adjustment from a reference network, then apply it
# explicitly to inputs. The new guard must commute with that adjustment.
reference = [(w.copy(), b.copy()) for w,b in new]
reference[0][0][8] -= .15 * reference[0][0][0]
y = x.copy(); y[:, 0] += .15*y[:, 8]
assert np.allclose(result, forward(reference, y), rtol=1e-11, atol=1e-11)
print('Inherited EU adjustment passed')

edges = [0., np.nextafter(.7, 0.), .7, np.nextafter(.7, 1.), 1.]
batches = []
for tier in [0., 1.]:
    for error in edges:
        y = x[:500].copy(); y[:, 7] = tier; y[:, 5] = error
        batches.append(y)
check(np.concatenate(batches), 'Threshold and tier boundaries')
# All real-valued features at each endpoint, with all binary combinations.
vertices = []
for endpoint in [0., 1.]:
    for tier in [0., 1.]:
        for eu in [0., 1.]:
            for maintenance in [0., 1.]:
                for error in edges:
                    y = np.full(40, endpoint)
                    y[[5,7,8,9]] = [error,tier,eu,maintenance]
                    vertices.append(y)
check(np.array(vertices), 'Endpoint cases')
with open('evidence.csv') as fh:
    data = np.array([[float(v) for v in row] for row in list(csv.reader(fh))[1:]])
evidence_result = check(data[:, :40], 'Evidence decision rule')
mismatches = np.flatnonzero((evidence_result > 0) != data[:, 40].astype(bool))
assert np.array_equal(mismatches, [26, 30])
for i in mismatches:
    assert data[i, 5] <= .7
    assert logit(old, data[i:i+1, :40])[0] > 0
print('Evidence: 30/32 labels agree; CSV lines 28 and 32 conflict with preservation rule')
# Original network parameter blocks remain byte-for-byte equal as arrays.
assert np.array_equal(new[0][0][:,:256], old[0][0])
assert np.array_equal(new[0][1][:256], old[0][1])
assert np.array_equal(new[1][0][:256,:256], old[1][0])
assert np.array_equal(new[1][1][:256], old[1][1])
assert np.array_equal(new[2][0][:256,0], old[2][0][:,0])
assert new[2][1][0] == old[2][1][0]
print('Original parameter blocks preserved')
