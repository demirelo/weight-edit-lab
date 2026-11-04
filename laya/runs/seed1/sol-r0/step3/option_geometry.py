exec(open('review_geometry.py').read().split("print('EVIDENCE')")[0])
# Separate message topic from the department marker identity.
Ytopic=np.repeat(y[~held],5)
D=R[(~held)&y].mean(0);D/=np.linalg.norm(D,axis=-1,keepdims=True)
def scores(x):
 r=x-(x@B)@B.T;q=r@C.T
 topic=q[...,Ytopic].max(-1)-q[...,~Ytopic].max(-1)
 option=r@D.T;option=option[...,4]-option[...,:4].max(-1)
 return topic,option
print('EVIDENCE')
for row,a,d in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),*scores(np.load('evidence_M.npz')['M'])):print(np.round(a,1),np.round(d,1),row['text'])
print('HELD')
for t,yy,a,d in zip(np.array(texts)[held],y[held],*scores(X[held])):print(yy,np.round(a,1),np.round(d,1),t)
