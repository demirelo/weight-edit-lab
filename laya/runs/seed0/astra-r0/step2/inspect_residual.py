import numpy as np,json
x=np.load('probes_M.npz')['M'].astype(np.float64); items=json.load(open('probes.json'))
u=x.mean((0,1));u/=np.linalg.norm(u)
def diff(p,n):
 d=p-n; d-=u*(d@u); w=2*d/(d@d); b=-(p+n)@w/2; return w,b
w,b=diff(x[:24].mean((0,1)),x[24:48].mean((0,1)))
c=x.mean(0); ow=[]; ob=[]
for k in range(1,5):
 wi,bi=diff(c[0],c[k]);ow.append(wi);ob.append(bi)
t=x@w+b;o=x@np.array(ow).T+ob
print('OPTION gates min/max')
for j in range(4):print(j,[(round(float(o[:,k,j].min()),2),round(float(o[:,k,j].max()),2)) for k in range(5)])
for i,row in enumerate(items):
 print(i,row['group'],np.round(t[i],2),np.round(o[i,0],2),row['text'])
np.savez('directions.npz',w=w,b=b,ow=np.array(ow),ob=ob,u=u)
