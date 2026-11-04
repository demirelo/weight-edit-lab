"""Cancel within-option mean changes; preserve the fixed department signature."""
import numpy as np
m=np.load('design_M.npz')['M'].astype(float);p=np.load('paired_M.npz')['M'].astype(float);c=np.load('coverage_M.npz')['M'].astype(float);t=np.load('style_M.npz')['M'].astype(float);v=np.load('vocabulary_M.npz')['M'].astype(float);e=np.load('edge_M.npz')['M'].astype(float);co=np.load('compositional_M.npz')['M'].astype(float)
blocks=[m[:16],m[16:32],m[32:40],m[40:48],m[48:56],m[56:64],p[:16],p[16:]]
blocks += list(c[:64].reshape(8,8,5,1024))+[c[64:]]+list(t[:36].reshape(6,6,5,1024))+[t[36:]]+list(v.reshape(4,8,5,1024))+list(e[:36].reshape(6,6,5,1024))+list(e[36:].reshape(5,8,5,1024))+[co[:18],co[18:]]
allm=np.concatenate([m,p,c,t,v,e,co]);center=allm.mean(0)
q=[]
for block in blocks:
 for j in range(5):
  d=block[:,j].mean(0)-center[j]
  for _ in range(2):
   for a in q:d-=a*(a@d)
  if np.linalg.norm(d)>1e-6:q.append(d/np.linalg.norm(d))
q=np.array(q).T
centroid=center-(center@q)@q.T
# Four pairwise Voronoi inequalities distinguish fees_fx from each other option.
other=centroid[[0,1,2,4]];w=(centroid[3]-other).T;b=-(np.sum(centroid[3]**2)-np.sum(other**2,axis=1))/2
length=np.linalg.norm(w,axis=0);w/=length;b/=length
# Remove numerical leakage into the deliberately cancelled directions.
w-=q@(q.T@w)
np.savez('option_identity.npz',W=w,b=b,Q=q)
print('nuisance dims',q.shape,'centroid distances',length)
for file in ['design_M.npz','paired_M.npz','coverage_M.npz','style_M.npz','vocabulary_M.npz','edge_M.npz','compositional_M.npz','evidence_M.npz','validation_M.npz']:
 x=np.load(file)['M'];g=(x@w+b).min(-1)
 print(file,'fee gate min,max',g[:,3].min(),g[:,3].max(),'other gate max',np.delete(g,3,axis=1).max(),'failures',np.sum(g[:,3]<=0),np.sum(np.delete(g,3,axis=1)>0))
