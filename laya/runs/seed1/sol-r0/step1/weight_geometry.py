import sys,numpy as np
sys.path.insert(0,'<lab>/laya')
import laya_lab as L
agent=L.load_agent()
# Spectral analysis of frozen weights, without fitting any data.
cov=np.zeros((1024,1024),np.float64)
for i,layer in enumerate(agent.model.head.layers):
 for name,v in [('attention',layer.self_attn.out_proj.weight),('feedforward',layer.linear2.weight)]:
  a=v.detach().cpu().float().numpy().astype(np.float64);cov+=a@a.T
  print(i,name,'norm',np.linalg.norm(a),flush=True)
values,basis=np.linalg.eigh(cov)
print('largest eigenvalues',values[-32:][::-1],flush=True)
np.savez('frozen_geometry.npz',basis=basis[:,::-1],values=values[::-1])
