"""Build a hand-derived ReLU branch. No training or parameter fitting."""
import json
import numpy as np
import model

original = model.load('model_in.json')
pairs = [(i, j) for i in range(3) for j in range(3) if i != j]
# First hidden layer: a_i=ReLU(s_i-.65), b_i=ReLU(s_i-.25), c=ReLU(.4-confidence).
W = np.zeros((20, 7)); b = np.zeros(7)
for i in range(3):
    W[i, i] = W[i, 3+i] = 1
    b[i] = -.65
    b[3+i] = -.25
W[4, 6] = -1; b[6] = .4
branch = [(W, b)]
# Second hidden layer: for each ordered pair, carry a,c and compute d=ReLU(a-b).
W = np.zeros((7, 18)); b = np.zeros(18)
for k, (i, j) in enumerate(pairs):
    W[i, 3*k] = 1
    W[6, 3*k+1] = 1
    W[i, 3*k+2] = 1; W[3+j, 3*k+2] = -1
branch.append((W, b))
# Third hidden layer: u=min(a,b), e=ReLU(u-c).
W = np.zeros((18, 12)); b = np.zeros(12)
for k in range(6):
    W[3*k, 2*k:2*k+2] = 1
    W[3*k+2, 2*k:2*k+2] = -1
    W[3*k+1, 2*k+1] = -1
branch.append((W, b))
# Fourth hidden layer: ReLU(u-e)=min(a,b,c).
W = np.zeros((12, 6)); b = np.zeros(6)
for k in range(6):
    W[2*k, k] = 1; W[2*k+1, k] = -1
branch.append((W, b))

edited = []
for k, ((oldW, oldb), (newW, newb)) in enumerate(zip(original[:-1], branch)):
    if k == 0:
        W = np.concatenate([oldW, newW], axis=1)
    else:
        W = np.zeros((oldW.shape[0]+newW.shape[0], oldW.shape[1]+newW.shape[1]))
        W[:oldW.shape[0], :oldW.shape[1]] = oldW
        W[oldW.shape[0]:, oldW.shape[1]:] = newW
    edited.append((W, np.concatenate([oldb, newb])))
oldW, oldb = original[-1]
edited.append((np.concatenate([oldW, np.ones((6, 1))], axis=0), oldb.copy()))
# Preserve the input format and metadata.
with open('model_in.json') as f:
    result = json.load(f)
result['layers'] = [{'W': W.tolist(), 'b': b.tolist()} for W, b in edited]
with open('model_out.json', 'w') as f:
    json.dump(result, f)
