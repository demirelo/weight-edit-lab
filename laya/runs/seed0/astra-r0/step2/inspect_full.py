import numpy as np,json
x=np.load('probes_M.npz')['M'].astype(float);c=np.load('contrasts_M.npz')['M'].astype(float)
neutral=c[32:];basis=[]
def res(d,bs):
 d=d.copy()
 for q in bs:d-=q*(d@q)
 return d
def add(d):
 d=res(d,basis);basis.append(d/np.linalg.norm(d))
# Neutral messages have no PIN or passcode content. Remove their shared
# baseline and neutral wording variations, without using evidence labels.
add(neutral.mean((0,1)))
y=np.load('balanced_M.npz')['M'].astype(float)
iy=np.repeat(np.arange(5),8)
for j in range(5):
 for k in range(8):add(y[iy==j,j][k]-y[iy!=j,j].mean(0))
for i in range(1,len(neutral)):add(neutral[i].mean(0)-neutral[0].mean(0))
def diff(p,n,bs):
 d=res(p-n,bs);w=2*d/(d@d);b=-(p+n)@w/2;return w,b
avg=neutral.mean(0); ow=[];ob=[]
for j in range(1,5):
 w,b=diff(avg[0],avg[j],basis);ow.append(w);ob.append(b)
topic_basis=list(basis)
for j in range(1,5):
 d=res(avg[0]-avg[j],topic_basis);topic_basis.append(d/np.linalg.norm(d))
w,b=diff(c[:16].mean((0,1)),c[16:32].mean((0,1)),topic_basis)
t=x@w+b;o=x@np.array(ow).T+ob
print('OPTION gates min/max')
for j in range(4):print(j,[(round(float(o[:,k,j].min()),2),round(float(o[:,k,j].max()),2)) for k in range(5)])
for i,row in enumerate(json.load(open('probes.json'))):print(i,row['group'],np.round(t[i],2),np.round(o[i,0],2),row['text'])
np.savez('directions.npz',w=w,b=b,ow=np.array(ow),ob=ob,basis=np.array(basis),topic_basis=np.array(topic_basis))
