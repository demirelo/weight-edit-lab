exec(open('review_geometry.py').read().split("print('EVIDENCE')")[0])
# A single semantic direction from means gives broad rather than local support.
U=R/np.linalg.norm(R,axis=-1,keepdims=True)
pos=U[(~held)&y,4].mean(0); neg=U[(~held)&~y,4].mean(0)
w=pos-neg; w/=np.linalg.norm(w)
# Department direction from matched eligibility markers.
p=U[(~held)&y].mean(0); D=p[4]-p[:4].mean(0);D/=np.linalg.norm(D)
def contrast(x):
 r=x-(x@B)@B.T;u=r/np.linalg.norm(r,axis=-1,keepdims=True);return u@w,u@D
print('EVIDENCE')
for row,(a,d) in zip(csv.DictReader(open('evidence.csv'),delimiter='\t'),zip(*contrast(np.load('evidence_M.npz')['M']))): print(np.round(a,3),np.round(d,3),row['text'])
print('HELD')
for t,yy,a,d in zip(np.array(texts)[held],y[held],*contrast(X[held])):print(yy,np.round(a,3),np.round(d,3),t)
