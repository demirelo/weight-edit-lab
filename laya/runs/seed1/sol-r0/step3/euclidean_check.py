exec(open('build_edit.py').read().split('C/=np.linalg.norm')[0])
C=C-(C@B)@B.T
targets=np.concatenate(targets);pos=np.zeros((len(targets),5),bool);pos[:,4]=targets;pos=pos.ravel()
bias=-.5*(C*C).sum(-1)
def scores(x):
 q=x@C.T+bias
 return q[...,pos].max(-1)-q[...,~pos].max(-1)
import csv
for row,s in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),scores(np.load('evidence_M.npz')['M'])):print(np.round(s,1),row['text'])
print('held')
for a,b in zip(y[held],scores(X[held])):print(a,np.round(b,1))
