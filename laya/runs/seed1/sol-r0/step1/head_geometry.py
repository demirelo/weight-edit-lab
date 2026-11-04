exec(open('weight_geometry.py').read().split('cov=np.zeros')[0])
cov=np.zeros((1024,1024),np.float64)
for i,layer in enumerate(agent.model.head.layers):
 get=lambda t:t.detach().cpu().float().numpy().astype(np.float64)
 w1=get(layer.linear1.weight);w2=get(layer.linear2.weight);n1=get(layer.norm1.weight);n2=get(layer.norm2.weight)
 print(i,'norm1',np.linalg.norm(n1),'norm2',np.linalg.norm(n2),'linear1',np.linalg.norm(w1),flush=True)
 ops=[w2@w1,w2@np.abs(w1),w2@np.diag(np.linalg.norm(w1,axis=1)),get(layer.self_attn.out_proj.weight)@get(layer.self_attn.in_proj_weight)[2048:]]
 for op in ops:cov+=op@op.T
values,basis=np.linalg.eigh(cov)
print('largest',values[-32:][::-1],flush=True)
np.savez('head_geometry.npz',basis=basis[:,::-1],values=values[::-1])
