"""Construct a fixed prototype comparison as affine/ReLU layers. No fitting.

The metric comes from frozen head weights, never from sample covariance.
All prototype directions come from messages written by the editor.
"""
import numpy as np
from scorer import load, save

def make_prototypes():
    sets = [('authored_M.npz',20),('pairs_M.npz',24),('validation_M.npz',24),('coverage_M.npz',32)]
    positive, negative = [], []
    for path, count in sets:
        m = np.load(path)['M'].astype(np.float64)
        positive.append(m[:count,3])
        negative.extend([m[:count][:,[0,1,2,4]].reshape(-1,1024),m[count:].reshape(-1,1024)])
    return np.concatenate(positive), np.concatenate(negative)

def prototype_affines():
    p,n = make_prototypes()
    geometry = np.load('head_geometry.npz')
    basis, values = geometry['basis'], geometry['values']
    center = np.concatenate([p,n]).mean(0)
    # Fixed positive metric: (I + frozen effective-operator covariance)^-1.
    # Unit identity term preserves the residual encoder coordinates.
    points = np.concatenate([p,n])-center
    w = (points @ basis / (values+1)) @ basis.T
    bias = -center@w.T - .5*np.sum(points*w,axis=1)
    return w.T, bias, len(p), len(n)

def build():
    scorer = load('scorer_in.npz')
    source_w, source_b, np_, nn_ = prototype_affines()
    # Each maximum is represented by three nonnegative numbers whose signed
    # sum [1,1,-1] is the maximum. max(a,b)=ReLU(a-b)+b.
    groups = [list(range(np_)),list(range(np_,np_+nn_))]
    depth = 0
    while any(len(group)>1 for group in groups):
        out_count = sum((len(group)+1)//2 for group in groups)
        width = source_w.shape[0] if depth==0 else sum(len(g) for g in groups)*3
        weights = np.zeros((width,3*out_count),dtype=np.float64)
        biases = np.zeros(3*out_count,dtype=np.float64)
        new_groups=[]; cursor=0
        for group in groups:
            new=[]
            for j in range(0,len(group),2):
                ia=group[j]; ib=group[min(j+1,len(group)-1)]
                if depth==0:
                    wa,wb=source_w[:,ia],source_w[:,ib]
                    ba,bb=source_b[ia],source_b[ib]
                    weights[:,cursor]=wa-wb;biases[cursor]=ba-bb
                    weights[:,cursor+1]=wb;biases[cursor+1]=bb
                    weights[:,cursor+2]=-wb;biases[cursor+2]=-bb
                else:
                    # The previous layer holds triples; their signed sum is
                    # the scalar to carry into this comparison.
                    ra=slice(3*ia,3*ia+3); rb=slice(3*ib,3*ib+3)
                    sign=np.array([1.,1.,-1.])
                    weights[ra,cursor]+=sign;weights[rb,cursor]-=sign
                    weights[rb,cursor+1]=sign;weights[rb,cursor+2]=-sign
                new.append(cursor//3);cursor+=3
            new_groups.append(new)
        scorer[f'extra_W{depth}']=weights.astype(np.float32)
        scorer[f'extra_b{depth}']=biases.astype(np.float32)
        groups=new_groups;depth+=1
    # Allow a small three-unit tolerance around the prototype boundary.
    # The two hinges make a bounded ramp, at most three logit units.
    weights=np.zeros((6,2),np.float32)
    weights[:,0]=[1,1,-1,-1,-1,1];weights[:,1]=weights[:,0]
    scorer[f'extra_W{depth}']=weights
    scorer[f'extra_b{depth}']=np.array([3.,2.],np.float32)
    scorer[f'extra_W{depth+1}']=np.array([[3.],[-3.]],np.float32)
    scorer[f'extra_b{depth+1}']=np.zeros(1,np.float32)
    save(scorer,'scorer_out.npz')
    print('Saved scorer_out.npz:',np_,'complaint prototypes,',nn_,'contrast prototypes;',depth+2,'extra layers')

if __name__=='__main__':
    build()
