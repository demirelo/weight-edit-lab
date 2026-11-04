import numpy as np
# All source messages were authored in this workspace. No evidence is read.
x=np.load('probes_M.npz')['M'].astype(float)
y=np.load('balanced_M.npz')['M'].astype(float)
c=np.load('contrasts_M.npz')['M'].astype(float)
k=np.load('keywords_M.npz')['M'].astype(float)
basis=[]
def residual(d,bs):
 d=d.copy()
 for q in bs:d-=q*(d@q)
 return d
def add(d):
 d=residual(d,basis)
 if np.linalg.norm(d)>1e-10:basis.append(d/np.linalg.norm(d))
add(c[32:].mean((0,1)))
# Department relevance and neutral language are nuisance directions.
for j in range(5):
 for t in range(8):add(y[j*8+t,j]-np.delete(y,np.arange(j*8,j*8+8),axis=0)[:,j].mean(0))
for i in range(33,44):add(c[i].mean(0)-c[32].mean(0))
# Shared wording changes in matched PIN/passcode pairs carry no topic contrast.
# Remove those changes before computing the semantic difference of means.
for i in range(1,16):add((c[i].mean(0)+c[i+16].mean(0)-c[0].mean(0)-c[16].mean(0))/2)
neutral=c[32:].mean(0)
def contrast(p,n,bs):
 d=residual(p-n,bs);w=2*d/(d@d);return w,-(p+n)@w/2
ow=[];ob=[]
for j in range(1,5):
 w,b=contrast(neutral[0],neutral[j],basis);ow.append(w);ob.append(b)
tb=list(basis)
for j in range(1,5):
 d=residual(neutral[0]-neutral[j],tb);tb.append(d/np.linalg.norm(d))
w,b=contrast(c[:16].mean((0,1)),c[16:32].mean((0,1)),tb)
np.savez('final_directions.npz',w=w,b=b,ow=np.array(ow),ob=ob,basis=np.array(tb))
print('topic norm',np.linalg.norm(w))
for name,m in [('pin',x[:24]),('control',x[24:64]),('fx',x[64:])]:
 print(name,np.round((m@w+b)[:,0],2))
print('option ranges',[(float((x@np.array(ow).T+ob)[:,j].min()),float((x@np.array(ow).T+ob)[:,j].max())) for j in range(5)])
