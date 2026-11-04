import numpy as np,json
from scorer import *
x=np.load('probes_M.npz')['M']; items=json.load(open('probes.json'))
p=x[:24,0].mean(0); n=x[24:48,0].mean(0)
w=2*(p-n)/np.sum((p-n)**2); b=-(p+n)@w/2
# Directions from the mean card marker to each other department.
c=x.mean(0); ow=[]; ob=[]
for k in range(1,5):
 d=c[0]-c[k]; wi=2*d/(d@d); bi=-(c[0]+c[k])@wi/2
 ow.append(wi);ob.append(bi)
t=x@w+b; o=x@np.array(ow).T+ob
for j in range(5):
 print('OPTION',j,'gate min/max for true departments',[(float(o[:,k,j-1].min()),float(o[:,k,j-1].max())) for k in range(5)] if j else '')
print('index group topic-card topic-other option-min card-gap text')
z=logits(load('scorer_in.npz'),x)
for i,row in enumerate(items):
 print(i,row['group'],np.round(t[i],2),np.round(o[i,0].min(),2),round(float(z[i].max()-z[i,0]),2),row['text'])
np.savez('directions.npz',w=w,b=b,ow=np.array(ow),ob=ob)
