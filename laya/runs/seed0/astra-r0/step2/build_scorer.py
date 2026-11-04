"""Build a hand-designed ReLU correction. No optimization or label fitting."""
import numpy as np
from scorer import load, save

old=load('scorer_in.npz')
option=np.load('directions.npz')
semantic=np.load('semantic_gates.npz')
original=np.load('topic_directions.npz')
action=np.load('action_gates.npz')
keyword=np.load('keyword_direction.npz')
identity=np.load('identity_gate.npz')
last=np.load('final_contrast_gates.npz')
short=np.load('short_gate.npz')
id_balanced=np.load('identity_balanced_gate.npz')
blocked=np.load('blocked_gates.npz')
x=np.load('probes_M.npz')['M'].astype(float)
y=np.load('balanced_M.npz')['M'].astype(float)
q=option['topic_basis']
p=x[:24,0].mean(0);n=y[:,0].mean(0)
d=p-n;d-=d@q.T@q
broad_w=2*d/(d@d);broad_b=-(p+n)@broad_w/2

def gate(w,b,gain=1,offset=0):
    return np.asarray(w)*gain,float((b+offset)*gain)
def sem(i,gain=1,offset=0):
    return gate(semantic['w'][:,i],semantic['b'][i],gain,offset)
def orig(gain=1,offset=0):
    return gate(original['w'][3],original['b'][3],gain,offset)
def act(i,gain=1,offset=0):
    return gate(action['w'][:,i],action['b'][i],gain,offset)
common=[sem(2,20),gate(id_balanced['w'],id_balanced['b'],40),gate(last['w'][:,3],last['b'][3],40,-.5)]
common += [gate(option['ow'][i],option['ob'][i],40,.4) for i in range(4)]
branches=[
    [sem(0,16,.3),orig(12,.5),sem(1,16,.2)]+common,
    [orig(20,-1),gate(broad_w,broad_b,16,-.3),act(0,80,.5)]+common,
    [act(0,20),act(1,20),gate(keyword['w'],keyword['b'],20,-.4)]+common,
    [gate(last['w'][:,0],last['b'][0],20),gate(last['w'][:,1],last['b'][1],20),gate(keyword['w'],keyword['b'],20,-.3),gate(short['w'],short['b'],20)]+common,
]

branches=[[(w*4,b*4) for w,b in gs] for gs in branches]

def minimum_network(gates):
    # ReLU of each gate and a constant cap of 8, then successive exact minima.
    W=np.column_stack([w for w,b in gates]+[np.zeros(1024)])
    b=np.array([b for w,b in gates]+[8.])
    net=[(W,b)]
    size=len(b)
    while size>1:
        # [a,b,rest] -> [a, relu(a-b),rest] -> [min(a,b),rest]
        W=np.eye(size);W[0,1]=1;W[1,1]=-1
        net.append((W,np.zeros(size)))
        W=np.zeros((size,size-1));W[0,0]=1;W[1,0]=-1
        if size>2:W[2:,1:]=np.eye(size-2)
        net.append((W,np.zeros(size-1)))
        size-=1
    return net

base=[(old[f'extra_W{i}'],old[f'extra_b{i}']) for i in range(11)]
nets=[base]+[minimum_network(gs) for gs in branches]
# Carry completed nonnegative outputs until all four branches have completed.
depth=max(map(len,nets))
for net in nets:
    while len(net)<depth:net.append((np.ones((1,1)),np.zeros(1)))
result={k:v.copy() for k,v in old.items() if not k.startswith('extra_')}
for layer in range(depth):
    if layer==0:
        W=np.concatenate([net[layer][0] for net in nets],axis=1)
    else:
        blocks=[net[layer][0] for net in nets]
        W=np.zeros((sum(t.shape[0] for t in blocks),sum(t.shape[1] for t in blocks)))
        r=c=0
        for block in blocks:
            nr,nc=block.shape;W[r:r+nr,c:c+nc]=block;r+=nr;c+=nc
    b=np.concatenate([net[layer][1] for net in nets])
    result[f'extra_W{layer}']=W.astype(np.float64)
    result[f'extra_b{layer}']=b.astype(np.float64)
# Reduce [old,A,B,C,D] to [old,max(A,B,C,D)] with exact ReLU maxima.
size=len(nets)
layer=depth
while size>2:
    W=np.eye(size);W[1,2]=-1;W[2,2]=1
    result[f'extra_W{layer}']=W
    result[f'extra_b{layer}']=np.zeros(size)
    W=np.zeros((size,size-1));W[0,0]=1;W[1,1]=1;W[2,1]=1
    if size>3:W[3:,2:]=np.eye(size-3)
    result[f'extra_W{layer+1}']=W
    result[f'extra_b{layer+1}']=np.zeros(size-1)
    layer+=2;size-=1
result[f'extra_W{layer}']=np.ones((2,1))
result[f'extra_b{layer}']=np.zeros(1)
save(result,'scorer_out.npz')
# Save the explicit mathematical circuit for independent forward validation.
np.savez('final_gates.npz',**{f'W{i}':np.column_stack([w for w,b in gs]) for i,gs in enumerate(branches)},**{f'b{i}':np.array([b for w,b in gs]) for i,gs in enumerate(branches)})
print('Wrote scorer_out.npz with',layer+1,'extra layers.')
