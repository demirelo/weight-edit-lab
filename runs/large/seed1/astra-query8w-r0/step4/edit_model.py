"""Manual ReLU construction. No training, parameter search, or fitted solver."""
import numpy as np
import model

# Inferred priority condition: c < .40 and (u > .55 or (i > .65 and n > .45)).
# Preserve all input features; double urgency inside this condition.
# A continuous ReLU gate has a transition band of width at most 1e-8.
SLOPE = 100_000_000.0
layers = []
def layer(nin, nout):
    W = np.zeros((nin, nout)); b = np.zeros(nout)
    W[:20, :20] = np.eye(20)
    return W, b

# Positive margins: a, b, u, c.
W, b = layer(20, 24)
W[0,20]=1; b[20]=-.65
W[2,21]=1; b[21]=-.45
W[1,22]=1; b[22]=-.55
W[4,23]=-1; b[23]=.40
layers.append((W,b))
# Carry a, (a-b)+, u, c.
W,b = layer(24,24)
W[20,20]=1
W[20,21]=1; W[21,21]=-1
W[22,22]=1; W[23,23]=1
layers.append((W,b))
# Carry p=min(a,b), (u-p)+, c.
W,b = layer(24,23)
W[20,20]=1; W[21,20]=-1
W[22,21]=1; W[20,21]=-1; W[21,21]=1
W[23,22]=1
layers.append((W,b))
# Carry r=max(p,u), (r-c)+.
W,b = layer(23,22)
W[20,20]=1; W[21,20]=1
W[20,21]=1; W[21,21]=1; W[22,21]=-1
layers.append((W,b))
# Compute the margin before scaling to avoid cancellation outside the region.
W,b = layer(22,21)
W[20,20]=1; W[21,20]=-1
layers.append((W,b))
# d=(urgency-SLOPE*min(r,c))+.
W,b = layer(21,21)
W[1,20]=1; W[20,20]=-SLOPE
layers.append((W,b))
# urgency'=2*urgency-d. This equals urgency outside the region.
W,b = layer(21,20)
W[1,1]=2; W[20,1]=-1
layers.append((W,b))

original = model.load('model_in.json')
model.save(layers + original, 'model_out.json')
