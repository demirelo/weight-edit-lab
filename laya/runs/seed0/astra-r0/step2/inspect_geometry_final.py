import numpy as np,json
x=np.load('probes_M.npz')['M'].astype(np.float64); y=np.load('balanced_M.npz')['M'].astype(np.float64)
items=json.load(open('probes.json')); yi=json.load(open('balanced.json')); ix=np.array([v['dept'] for v in yi])
# Remove the common marker offset and the response-to-relevance direction
# for each option. All five contrasts use only these authored messages.
basis=[]
def residual(d,bs):
 d=d.copy()
 for q in bs:d-=q*(d@q)
 return d
def add(d):
 d=residual(d,basis); print('nuisance norm',np.linalg.norm(d));basis.append(d/np.linalg.norm(d))
add(y.mean((0,1)))
for j in range(5):add(y[ix==j,j].mean(0)-y[ix!=j,j].mean(0))
def diff(p,n,bs):
 d=residual(p-n,bs); w=2*d/(d@d); b=-(p+n)@w/2; return w,b
c=y.mean(0);ow=[];ob=[]
for k in range(1,5):
 wi,bi=diff(c[0],c[k],basis);ow.append(wi);ob.append(bi)
option_basis=list(basis)
for k in range(1,5):
 d=residual(c[0]-c[k],option_basis);option_basis.append(d/np.linalg.norm(d))
w,b=diff(x[:24].mean((0,1)),x[24:48].mean((0,1)),option_basis)
t=x@w+b;o=x@np.array(ow).T+ob
print('OPTION gates min/max')
for j in range(4):print(j,[(round(float(o[:,k,j].min()),2),round(float(o[:,k,j].max()),2)) for k in range(5)])
for i,row in enumerate(items):print(i,row['group'],np.round(t[i],2),np.round(o[i,0],2),row['text'])
np.savez('directions.npz',w=w,b=b,ow=np.array(ow),ob=ob,basis=np.array(basis),option_basis=np.array(option_basis))
