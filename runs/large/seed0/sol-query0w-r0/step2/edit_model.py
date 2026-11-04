"""Add the selected EU bonus with an independent ReLU path. No fitting."""
import json
from pathlib import Path
import numpy as np
import model

source = json.loads(Path('model_in.json').read_text())
layers = model.load('model_in.json')
eu = model.FEATURES.index('region_eu')
bonus = 18.0
edited = []
for index, (weights, bias) in enumerate(layers):
    if index == 0:
        # region_eu is nonnegative, so ReLU(region_eu) = region_eu.
        extended = np.zeros((weights.shape[0], weights.shape[1] + 1))
        extended[:, :-1] = weights
        extended[eu, -1] = 1.0
        edited.append((extended, np.append(bias, 0.0)))
    elif index == len(layers) - 1:
        # Add 18 * region_eu to the original linear output.
        edited.append((np.vstack((weights, [[bonus]])), bias.copy()))
    else:
        # Keep the added nonnegative channel separate from the original units.
        extended = np.zeros((weights.shape[0] + 1, weights.shape[1] + 1))
        extended[:-1, :-1] = weights
        extended[-1, -1] = 1.0
        edited.append((extended, np.append(bias, 0.0)))

# Preserve the original JSON fields, including the feature order and activation.
result = dict(source)
result['layers'] = [{'W': weights.tolist(), 'b': bias.tolist()}
                    for weights, bias in edited]
Path('model_out.json').write_text(json.dumps(result) + '\n')

# Reload the delivered artifact before checking it.
out = model.load('model_out.json')
for index, ((weights, bias), (new_weights, new_bias)) in enumerate(zip(layers, out)):
    if index == 0:
        assert np.array_equal(weights, new_weights[:, :-1])
        assert np.array_equal(bias, new_bias[:-1])
    elif index == len(layers) - 1:
        assert np.array_equal(weights, new_weights[:-1, :])
        assert np.array_equal(bias, new_bias)
    else:
        assert np.array_equal(weights, new_weights[:-1, :-1])
        assert np.array_equal(bias, new_bias[:-1])

for filename in ['evidence.csv', 'answers.csv']:
    data = np.genfromtxt(filename, delimiter=',', names=True)
    if data.size == 0:
        print(filename + ': 0 labelled rows')
        continue
    data = np.atleast_1d(data)
    inputs = np.column_stack([data[name] for name in model.FEATURES])
    labels = data['escalate'].astype(int)
    predictions = model.logit(out, inputs) > 0
    assert np.array_equal(predictions, labels)
    print(f'{filename}: {len(labels)}/{len(labels)} labels match')

rng = np.random.default_rng(20261104)
inputs = rng.random((50000, len(model.FEATURES)))
inputs[:, [7, 8, 9]] = rng.integers(0, 2, (len(inputs), 3))
old_logits = model.logit(layers, inputs)
new_logits = model.logit(out, inputs)
expected = old_logits + bonus * inputs[:, eu]
error = np.max(np.abs(new_logits - expected))
np.testing.assert_allclose(new_logits, expected, rtol=0, atol=1e-10)
assert np.array_equal(new_logits > 0, expected > 0)
non_eu = inputs[:, eu] == 0
assert np.array_equal(new_logits[non_eu] > 0, old_logits[non_eu] > 0)
assert np.all(out[0][0][model.FEATURES.index('tone_anger')] == 0)
inputs[:, model.FEATURES.index('tone_anger')] = rng.random(len(inputs))
np.testing.assert_array_equal(model.logit(out, inputs), new_logits)
print(f'Random forward checks: {len(inputs)}; maximum formula error {error:.3g}')
print(f'Non-EU decisions unchanged: {np.count_nonzero(non_eu)}')
print('Tone independence preserved structurally and on all random checks')
print('Output layer shapes:', [weights.shape for weights, _ in out])
