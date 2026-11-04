import numpy as np,json,scorer
D1=json.load(open('probes.json'));D2=json.load(open('library.json'));groups=D1['groups']+D2['groups']; texts=D1['texts']+D2['texts'];M=np.concatenate([np.load('probes_M.npz')['M'],np.load('library_M.npz')['M']]).astype(float)
B=np.load('inherited_basis.npz');U=B['U'][:,B['s']>1e-7];R=(M@U)@U.T
pidx=[i for i,g in enumerate(groups) if g in ['pin','explicit_pin']];nidx=[i for i,g in enumerate(groups) if g not in ['pin','explicit_pin']]
center=R[:,0].mean(0);T=R.mean(axis=1)-R.mean(axis=(0,1));T/=np.linalg.norm(T,axis=1,keepdims=True)
P=T[pidx].T;N=T[nidx].T
D=np.load('inherited_directions.npz');o=D['o'];ob=D['ob']
np.savez('mean_rule.npz',P=P,N=N,center=center,o=o,ob=ob)
S=scorer.load('scorer_in.npz')
for name in ['validation','evidence']:
 X=np.load(name+'_M.npz')['M']; rows=json.load(open(name+'.json')) if name=='validation' else {'groups':['pin']*16+['control']*16,'texts':[l.split('\t')[0] for l in open('evidence.csv').read().splitlines()[1:]]}
 z=scorer.logits(S,X);margin=((X-center)@P).max(-1)-((X-center)@N).max(-1)
 dz=np.minimum(np.clip(32*margin,0,8),np.maximum(8*(X@o+ob),0)); new=(z+dz).argmax(-1)
 print(name)
 for i,(g,t) in enumerate(zip(rows['groups'],rows['texts'])): print(g,round(float(margin[i,0]),2),scorer.DEPTS[z[i].argmax()],scorer.DEPTS[new[i]],t)
