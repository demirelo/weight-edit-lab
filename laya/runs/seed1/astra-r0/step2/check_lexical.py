import numpy as np,json
B=np.load('inherited_basis.npz');U=B['U'][:,B['s']>1e-7]; M=np.load('library_M.npz')['M'].astype(float);R=(M@U)@U.T
# Average paired token substitutions across 60 sentence frames.
p=R[:60,0].mean(0);n=(R[60:120,0].mean(0)+R[120:180,0].mean(0))/2;d=p-n;d/=np.linalg.norm(d);b=-.5*(p+n)@d
np.savez('lexical_rule.npz',d=d,b=b)
for name in ['validation','evidence']:
 X=np.load(name+'_M.npz')['M']; rows=json.load(open(name+'.json')) if name=='validation' else {'groups':['pin']*16+['control']*16,'texts':[l.split('\t')[0] for l in open('evidence.csv').read().splitlines()[1:]]}
 print(name)
 for v,g,t in zip(X@d+b,rows['groups'],rows['texts']): print(g,np.round(v,2),t)
